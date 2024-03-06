import logging
from dataclasses import dataclass
from datetime import datetime, time


def first(iterable, default=None):
    return next(iter(iterable), default)


DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"


def parse_datetime(d):
    return datetime.strptime(d, DATETIME_FORMAT)


TIME_FORMAT = "%H:%M:%S"


def parse_time(d):
    return datetime.strptime(d, TIME_FORMAT).time()


def parse_tdeq(d):
    if "null" in d:
        return None
    try:
        return parse_time(d)
    except Exception as e:
        logging.debug(e)
    return parse_datetime(d)


def parse_progress(progress):
    try:
        return float(progress)
    except Exception as e:
        logging.debug(f"{e} => Fallback to datetime parsing")

    # When finished, progress becomes the date of the end
    if parse_datetime(progress):
        return 100.0
    return None


def single_xpath(xml, xpath, parser=None, default=None):
    try:
        res = xml.xpath(xpath)
        res = first(res)
    except Exception:
        return default
    if not res:
        return default
    if parser:
        res = parser(res)
    return res


pd = parse_datetime
sx = single_xpath


def mksx(xml):
    def single_xpath(xpath, parser=None, default=None):
        return sx(xml, xpath, parser=parser, default=default)

    return single_xpath


@dataclass
class SoftwareVersion:
    version: str
    filename: str
    released_on: datetime
    downloaded: bool
    current: bool
    latest: bool
    uploaded: bool

    @staticmethod
    def from_xml(xml):
        if isinstance(xml, (list, tuple)):
            xml = first(xml)
        if xml is None:
            return None
        p = mksx(xml)
        return SoftwareVersion(
            p("./version/text()"),
            p("./filename/text()"),
            p("./released-on/text()", parser=pd),
            p("./downloaded/text()") != "no",
            p("./current/text()") != "no",
            p("./latest/text()") != "no",
            p("./uploaded/text()") != "no",
        )

    @property
    def base_minor_version(self):
        major, minor, _ = self.version.split(".")
        return f"{major}.{minor}.0"

    @property
    def base_major_version(self):
        major, _, _ = self.version.split(".")
        return f"{major}.0.0"


@dataclass
class Job:
    tenq: datetime
    tdeq: time
    id: str
    user: str
    type: str
    status: str
    queued: bool
    stoppable: bool
    result: str
    tfin: datetime
    description: str
    position_in_queue: int
    progress: float
    details: str
    warnings: str

    @staticmethod
    def from_xml(xml):
        if isinstance(xml, (list, tuple)):
            xml = first(xml)
        if xml is None:
            return None
        p = mksx(xml)
        return Job(
            p("./tenq/text()", parser=pd),
            p("./tdeq/text()", parser=parse_tdeq),
            p("./id/text()"),
            p("./user/text()"),
            p("./type/text()"),
            p("./status/text()"),
            p("./queued/text()") != "NO",
            p("./stoppable/text()") != "NO",
            p("./result/text()"),
            p("./tfin/text()", parser=pd),
            p("./description/text()"),
            p("./positionInQ/text()", parser=int),
            p("./progress/text()", parser=parse_progress),
            "\n".join(xml.xpath("./details/line/text()")),
            p("./warnings/text()"),
        )
