import logging
from itertools import product
from multiprocessing.pool import ThreadPool as Pool

import requests

from . import types
from .constants import SUCCESS_CODE
from .utils import (
    clean_url_host,
    detach,
    diff_patch,
    etree_fromstring,
    etree_tostring,
    extend_element,
    map_dicts,
    wait,
)

log = logging.getLogger(__name__)


def get_tree(host, api_key, /, remove_blank_text=True, verify=False, timeout=None):
    res = requests.get(
        f"{host}/api?type=config&action=show&xpath=/config",
        headers={"X-PAN-KEY": api_key},
        verify=verify,
        timeout=timeout,
    )
    root_tree = etree_fromstring(res.content, remove_blank_text=remove_blank_text)
    try:
        tree = root_tree.xpath("/response/result/config")[0]
    except Exception:
        log.warning("Response doesn't contains the config tag. Response:")
        log.warning(etree_tostring(root_tree, pretty_print=True).decode()[:1000])
        raise Exception("Response doesn't contains the config tag. Check the logs")
    detach(tree)  # Remove the /response/result part
    return tree


def parse_msg_result(result):
    # sometimes, there is <line> elements inside of msg
    msg = "".join(result.xpath("./msg/text()"))
    if not msg:
        msg = "".join(result.xpath("./result/msg/text()"))
    if msg:
        return msg
    return "\n".join(result.xpath("./msg/line/text()"))


def _get_rule_use_cmd(device_group, position, rule_type, start_index, number):
    # positions = ("pre", "post")
    return f"""<show><policy-app>
        <mode>get-all</mode>
        <filter>(rule-state eq 'any')</filter>
        <vsysName>{device_group}</vsysName>
        <position>{position}</position>
        <type>{rule_type}</type>
        <anchor>{start_index}</anchor>
        <nrec>{number}</nrec>
        <pageContext>rule_usage</pageContext>
    </policy-app></show>"""


class XMLApi:
    def __init__(self, host, api_key, verify=False):
        if not host:
            raise Exception("Missing Host")
        host, _, _ = clean_url_host(host)

        self._host = host
        self._api_key = api_key
        self._url = f"{host}/api"
        self._verify = verify

    def _request(
        self,
        type,
        method="GET",
        vsys=None,
        params=None,
        remove_blank_text=True,
        verify=None,
    ):
        if verify is None:
            verify = self._verify
        headers = {"X-PAN-KEY": self._api_key}
        query_params = {"type": type}
        if params:
            query_params = {**query_params, **params}
        if vsys is not None:
            query_params["vsys"] = vsys

        res = requests.request(
            method=method,
            url=self._url,
            params=query_params,
            headers=headers,
            verify=verify,
        )
        content = res.content.decode()
        tree = etree_fromstring(content, remove_blank_text=remove_blank_text)
        status = tree.attrib["status"]
        code = int(tree.get("code", SUCCESS_CODE))
        msg = parse_msg_result(tree)
        if status == "error" or code < SUCCESS_CODE:
            log.debug(content[:500])
            raise Exception(msg)
        if msg:
            return msg
        return tree

    def _conf_request(
        self,
        xpath,
        action="get",
        method="GET",
        vsys=None,
        params=None,
        remove_blank_text=True,
        verify=None,
    ):
        if params is None:
            params = {}
        params = {"action": action, "xpath": xpath, **params}
        return self._request(
            "config",
            method=method,
            vsys=vsys,
            params=params,
            remove_blank_text=remove_blank_text,
            verify=verify,
        )

    def _op_request(
        self,
        cmd,
        method="POST",
        vsys=None,
        params=None,
        remove_blank_text=True,
        verify=None,
    ):
        if params is None:
            params = {}
        params = {"cmd": cmd, **params}
        return self._request(
            "op",
            method=method,
            vsys=vsys,
            params=params,
            remove_blank_text=remove_blank_text,
            verify=verify,
        )

    def _commit_request(
        self,
        cmd,
        method="POST",
        params=None,
        remove_blank_text=True,
        verify=None,
    ):
        if params is None:
            params = {}
        params = {"cmd": cmd, **params}
        return self._request(
            "commit",
            method=method,
            params=params,
            remove_blank_text=remove_blank_text,
            verify=verify,
        )

    def configuration(
        self,
        xpath,
        action="get",
        method="GET",
        params=None,
        remove_blank_text=True,
        verify=None,
    ):
        return self._conf_request(
            xpath,
            action=action,
            method=method,
            params=params,
            remove_blank_text=remove_blank_text,
            verify=verify,
        )

    def operation(
        self,
        cmd,
        method="POST",
        params=None,
        remove_blank_text=True,
        verify=None,
    ):
        return self._op_request(
            cmd,
            method=method,
            params=params,
            remove_blank_text=remove_blank_text,
            verify=verify,
        )

    def get_tree(self, extended=False, verify=None):
        if verify is None:
            verify = self._verify
        tree = get_tree(self._host, self._api_key, verify=verify)
        if extended:
            self._extend_tree_information(tree, verify=verify)
        return tree

    def _get_rule_use(self, device_group, position, rule_type, number=200, verify=None):
        results = []
        for i in range(100):
            cmd = _get_rule_use_cmd(
                device_group,
                position,
                rule_type,
                i * number,
                number,
            )
            res = self._op_request(cmd, verify=verify).xpath("result")[0]
            total_count = int(res.attrib["total-count"])
            results.extend(res.xpath("entry"))
            if len(results) >= total_count:
                break
        return results

    def get_rule_use(self, tree=None, max_threads=None, verify=None):
        if tree is None:
            tree = self.get_tree(verify=verify)
        device_groups = tree.xpath("devices/*/device-group/*/@name")
        positions = ("pre", "post")
        # rule_types = tuple({x.tag for x in tree.xpath(
        # "devices/*/device-group/*"
        # "/*[self::post-rulebase or self::pre-rulebase]/*")})
        rule_types = ("security", "pbf", "nat", "application-override")
        args_list = list(product(device_groups, positions, rule_types))

        def func(args):
            return self._get_rule_use(*args, verify=verify)

        threads = len(args_list)
        threads = min(max_threads or threads, threads)
        with Pool(len(args_list)) as pool:
            data = pool.map(func, args_list)
        return [entry for entry_list in data for entry in entry_list]

    def _get_rule_hit_count(self, device_group, rulebase, rule_type, verify=None):
        cmd = (
            "<show><rule-hit-count><device-group>"
            f"<entry name='{device_group}'><{rulebase}><entry name='{rule_type}'>"
            f"<rules><all/></rules></entry></{rulebase}></entry>"
            "</device-group></rule-hit-count></show>"
        )
        res = self._op_request(cmd, verify=verify)
        entries = res.xpath(".//rules/entry") or []
        # return entries
        return [(device_group, rulebase, rule_type, e) for e in entries]

    def get_rule_hit_count(self, tree=None, max_threads=None, verify=None):
        if tree is None:
            tree = self.get_tree(verify=verify)
        device_groups = tree.xpath("devices/*/device-group/*/@name")
        # rulebases = tuple({x.tag for x in tree.xpath(
        # "devices/*/device-group/*/*")})
        rulebases = ("pre-rulebase", "post-rulebase")
        # rule_types = tuple({x.tag for x in tree.xpath(
        # "devices/*/device-group/*"
        # "/*[self::post-rulebase or self::pre-rulebase]/*")})
        rule_types = ("security", "pbf", "nat", "application-override")
        args_list = list(product(device_groups, rulebases, rule_types))

        def func(args):
            return self._get_rule_hit_count(*args, verify=verify)

        threads = len(args_list)
        threads = min(max_threads or threads, threads)
        with Pool(len(args_list)) as pool:
            data = pool.map(func, args_list)
        return [entry for entry_list in data for entry in entry_list]

    def _extend_tree_information(
        self,
        tree,
        extended=None,
        max_threads=None,
        verify=None,
    ):
        if extended is None:
            extended = self.get_rule_use(tree, max_threads=max_threads, verify=verify)
        rules = tree.xpath(
            ".//device-group/entry/"
            "*[self::pre-rulebase or self::post-rulebase]/*/rules/entry[@uuid]",
        )
        ext_dict = {x.attrib.get("uuid"): x for x in extended}
        rules_dict = {x.attrib["uuid"]: x for x in rules}
        for ext, rule in map_dicts(ext_dict, rules_dict):
            extend_element(rule, ext)
            # rule.extend(ext) # This is causing duplicates entries
        return tree, extended

    def get(self, xpath, verify=None):
        """
        This will retrieve the xml definition based on the xpath
        The xpath doesn't need to be exact
        and can select multiple values at once.
        Still, it must at least speciy /config at is begining
        """
        return self._conf_request(xpath, action="show", method="GET", verify=verify)

    def delete(self, xpath, verify=None):
        """
        This will REMOVE the xml definition at the provided xpath.
        The xpath must be exact.
        """
        return self._conf_request(
            xpath,
            action="delete",
            method="DELETE",
            verify=verify,
        )

    def create(self, xpath, xml_definition, verify=None):
        """
        This will ADD the xml definition
        INSIDE the element at the provided xpath.
        The xpath must be exact.
        """
        # https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api/set-configuration
        params = {"element": xml_definition}
        return self._conf_request(
            xpath,
            action="set",
            method="POST",
            params=params,
            verify=verify,
        )

    def update(self, xpath, xml_definition, verify=None):
        """
        This will REPLACE the xml definition
        INSTEAD of the element at the provided xpath
        The xpath must be exact.
        Nb: We can pull the whole config, update it locally,
        and push the final result
        """
        # https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api/set-configuration
        params = {"element": xml_definition}
        return self._conf_request(
            xpath,
            action="edit",
            method="POST",
            params=params,
            verify=verify,
        )

    def revert_changes(self, skip_validated=False, verify=None):
        skip = "<skip-validate>yes</skip-validate>" if skip_validated else ""
        cmd = f"<revert><config>{skip}</config></revert>"
        return self._op_request(cmd, verify=verify)

    def validate_changes(self, verify=None):
        cmd = "<validate><full></full></validate>"
        return self._op_request(cmd, verify=verify)

    def uncommited_changes(self, verify=None):
        """
        Gives detailed information about pending changes
        (e.g. xpath, owner, action, ...)
        """
        cmd = "<show><config><list><changes></changes></list></config></show>"
        return self._op_request(cmd, verify=verify)

    def uncommited_changes_patch(self, verify=None):
        """
        Gives detailed information about pending changes
        (e.g. xpath, owner, action, ...)
        """
        candidate = self.candidate_config(verify=verify)
        running = self.running_config(verify=verify)
        return diff_patch(running, candidate)

    def uncommited_changes_summary(self, admin=None, verify=None):
        """
        Only gives the concern device groups
        """
        admin = (
            f"<partial><admin><member>{admin}</member></admin></partial>"
            if admin
            else ""
        )
        cmd = f"<show><config><list><change-summary>{admin}</change-summary></list></config></show>"
        return self._op_request(cmd, verify=verify)

    def pending_changes(self, verify=None):
        """
        Result content is either 'yes' or 'no'
        """
        cmd = "<check><pending-changes></pending-changes></check>"
        return self._op_request(cmd, verify=verify)

    def candidate_config(self, verify=None):
        """
        Get the confirmation with pending changes
        """
        cmd = "<show><config><candidate></candidate></config></show>"
        return self._op_request(cmd, remove_blank_text=False, verify=verify)

    def running_config(self, verify=None):
        """
        Get the running configuration
        """
        cmd = "<show><config><running></running></config></show>"
        return self._op_request(cmd, remove_blank_text=False, verify=verify)

    def raw_get_jobs(self, job_id=None, verify=None):
        cmd = "<show><jobs>{}</jobs></show>".format(
            f"<id>{job_id}</id>" if job_id else "<all></all>",
        )
        return self._op_request(cmd, verify=verify)

    def get_versions(self):
        res = self.check_software_version()
        return [
            types.SoftwareVersion.from_xml(entry)
            for entry in res.xpath(".//sw-updates/versions/entry")
        ]

    def get_jobs(self, job_id=None, verify=None):
        job_xmls = self.raw_get_jobs(job_id, verify=verify).xpath(".//job")
        res = [types.Job.from_xml(x) for x in job_xmls]
        if job_id:  # We want one specific ID
            return res[0]
        return res

    def wait_job_completion(self, job_id, waiter=None):
        if not waiter:
            waiter = wait()
        for _ in waiter:
            job = self.get_jobs(job_id)
            if job.progress >= 100:
                return job
            log.info(f"Job {job_id} progress: {job.progress}")
        raise Exception("Timeout while waiting for job completion")

    def get_pending_jobs(self, verify=None):
        cmd = "<show><jobs><pending></pending></jobs></show>"
        return self._op_request(cmd, verify=verify)

    def commit_changes(self, force=False, verify=None):
        # force = "<force></force>"  # We don't want to support force option
        cmd = "<commit>{}</commit>".format("<force></force>" if force else "")
        return self._commit_request(cmd, verify=verify)

    def _lock_cmd(self, cmd, vsys, no_exception=False, verify=None):
        try:
            result = "".join(self._op_request(cmd, vsys=vsys, verify=verify).itertext())
            log.debug(result)
        except Exception as e:
            if no_exception:
                log.error(e)
                return False
            raise
        return True

    # https://github.com/PaloAltoNetworks/pan-os-python/blob/a6b018e3864ff313fed36c3804394e2c92ca87b3/panos/base.py#L4459
    def add_config_lock(
        self, comment=None, vsys="shared", no_exception=False, verify=None
    ):
        comment = f"<comment>{comment}</comment>" if comment else ""
        cmd = f"<request><config-lock><add>{comment}</add></config-lock></request>"
        return self._lock_cmd(cmd, vsys=vsys, no_exception=no_exception, verify=verify)

    def remove_config_lock(self, vsys="shared", no_exception=False, verify=None):
        cmd = "<request><config-lock><remove></remove></config-lock></request>"
        return self._lock_cmd(cmd, vsys=vsys, no_exception=no_exception, verify=verify)

    def add_commit_lock(
        self, comment=None, vsys="shared", no_exception=False, verify=None
    ):
        comment = f"<comment>{comment}</comment>" if comment else ""
        cmd = f"<request><commit-lock><add>{comment}</add></commit-lock></request>"
        return self._lock_cmd(cmd, vsys=vsys, no_exception=no_exception, verify=verify)

    def remove_commit_lock(self, vsys="shared", no_exception=False, verify=None):
        cmd = "<request><commit-lock><remove></remove></commit-lock></request>"
        return self._lock_cmd(cmd, vsys=vsys, no_exception=no_exception, verify=verify)

    def connected_devices(self, verify=None):
        cmd = "<show><devices><connected></connected></devices></show>"
        return self.operation(cmd, verify=verify)

    def system_info(self, verify=None):
        cmd = "<show><system><info></info></system></show>"
        return self.operation(cmd, verify=verify)

    def check_software_version(self, verify=None):
        cmd = "<request><system><software><check></check></software></system></request>"
        return self.operation(cmd, verify=verify)

    def raw_download_software(self, version, verify=None):
        """
        version is the software version to download
        """
        cmd = f"<request><system><software><download><version>{version}</version></download></software></system></request>"
        return self.operation(cmd, verify=verify)

    def download_software(self, version, verify=None):
        """
        version is the software version to download
        """
        res = self.raw_download_software(version, verify=verify)
        try:
            return res.xpath(".//job/text()")[0]
        except Exception:
            log.debug("Download has not started")
        return None

    def raw_install_software(self, version, verify=None):
        """
        version is the software version to install
        """
        cmd = f"<request><system><software><install><version>{version}</version></install></software></system></request>"
        return self.operation(cmd, verify=verify)

    def install_software(self, version, verify=None):
        """
        version is the software version to install
        """
        res = self.raw_install_software(version, verify=verify)
        try:
            return res.xpath(".//job/text()")[0]
        except Exception:
            log.debug("Download has not started")
        return None

    def restart(self, verify=None):
        cmd = "<request><restart><system></system></restart></request>"
        return self.operation(cmd, verify=verify)
