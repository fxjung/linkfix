import re
import logging
import urllib.parse
from urllib.parse import ParseResult

log = logging.getLogger(__name__)


def handle_url(parsed: ParseResult) -> str | None:
    log.debug("URL detected")
    hostname = parsed.hostname
    url = parsed.geturl()

    if "amazon" in hostname:
        match = re.search(
            r"/[dg]p/(?!video/)(?:product/)?([0-9a-zA-Z]+)/?", parsed.path
        )
        if match is not None:
            asin = match[1]
            new_url = f"https://{hostname}/dp/{asin}"
            log.debug(f"Detected Amazon URL: {new_url}")
            return new_url

    elif "ebay-kleinanzeigen" in hostname:
        match = re.search(r"/s-anzeige/.*/([0-9-]+)", parsed.path)
        if match is not None:
            new_url = f"https://{hostname}/s-anzeige/{match[1]}"
            log.debug(f"Detected ebay-kleinanzeigen URL: {new_url}")
            return new_url
