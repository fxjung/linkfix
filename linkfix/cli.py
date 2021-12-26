import typer
import logging
import asyncio
import pyperclip
import platform

from typing import Optional
from pathlib import Path

from urllib import parse as urlparse

from linkfix.handle_urls import handle_url

# from linkfix import config


formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")

ch = logging.StreamHandler()

ch.setFormatter(formatter)

logging.getLogger("").setLevel(logging.DEBUG)
logging.getLogger("").addHandler(ch)

log = logging.getLogger(__name__)

app = typer.Typer()


def handle_clipboard_X11(primary: bool):
    # cache = None
    clipboard = pyperclip.paste(primary=primary)
    url = urlparse.urlparse(clipboard)
    if url.scheme:
        pyperclip.copy(handle_url(url), primary=primary)


def handle_clipboard():
    clipboard = pyperclip.paste()
    url = urlparse.urlparse(clipboard)
    if url.scheme:
        pyperclip.copy(handle_url(url))


async def main():
    if (platform_ := platform.system()) == "Linux":
        pyperclip.set_clipboard("xsel")

    while True:
        proc = await asyncio.create_subprocess_exec("clipnotify")
        await proc.wait()
        log.debug("clipboard change detected")
        try:
            if platform_ == "Linux":
                # handle_clipboard_X11(primary=True)
                handle_clipboard_X11(primary=False)
            else:
                handle_clipboard()
        except Exception as e:
            log.error(f"{e} was raised.")


@app.callback(invoke_without_command=True)
def cli_main():
    try:
        if asyncio.get_event_loop().is_closed():
            if platform.system() == "Windows":
                asyncio.set_event_loop(asyncio.ProactorEventLoop())
            else:
                asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        results = loop.run_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        loop.stop()
        loop.close()


app()
