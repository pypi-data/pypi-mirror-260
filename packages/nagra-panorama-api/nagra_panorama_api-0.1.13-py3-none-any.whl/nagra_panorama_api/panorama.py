from panos import panorama

from .utils import clean_url_host


class Panorama(panorama.Panorama):
    def __init__(
        self,
        hostname,
        api_username=None,
        api_password=None,
        api_key=None,
        port=None,
        *args,
        **kwargs,
    ):
        _, hostname, _port = clean_url_host(hostname)
        port = port or _port or 443
        return super().__init__(
            hostname, api_username, api_password, api_key, port, *args, **kwargs
        )
