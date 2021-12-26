import re
import logging

log = logging.getLogger(__name__)


def handle_url(parsed):
    log.debug("url detected")
    hostname = parsed.hostname
    url = parsed.geturl()

    if "amazon" in hostname:
        path = parsed.path
        match = re.search(r"/[dg]p/(product/)?([0-9a-zA-Z]+)/?", path)
        if match is not None:
            asin = match[2]
            new_url = f"https://{hostname}/dp/{asin}"
            log.debug(f"detected amazon url: {new_url}")
        else:
            new_url = url

    else:
        new_url = url

    return new_url
