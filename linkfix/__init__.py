import pyperclip
import re
from urllib import parse as urlparse

def fix_url(parsed):
    hostname = parsed.hostname
    url = parsed.geturl()

    if 'amazon' in hostname:
        path = parsed.path
        match = re.search(r"/[dg]p/(product/)?([0-9a-zA-Z]+)/?", path)
        if match is not None:
            asin = match[2]
            new_url = f"https://{hostname}/dp/{asin}"
        else:
            new_url = url

    else:
        new_url = url

    return new_url

pyperclip.set_clipboard('xsel')
primary = pyperclip.paste(primary=True)
clipboard = pyperclip.paste(primary=False)

url_clipboard = urlparse.urlparse(clipboard)
url_primary = urlparse.urlparse(primary)

if url_primary.scheme:
    pyperclip.copy(fix_url(url_primary), primary=True)
if url_clipboard.scheme:
    pyperclip.copy(fix_url(url_clipboard), primary=False)
