import subprocess
import sys
from pathlib import Path

import typer
import logging
import asyncio
import pyperclip
import platform

from urllib import parse as urlparse

from linkfix.handle_urls import handle_url
from linkfix.config import config

# from linkfix import config

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")

ch = logging.StreamHandler()

ch.setFormatter(formatter)

logging.getLogger("").setLevel(logging.WARN)
logging.getLogger("").addHandler(ch)

log = logging.getLogger(__name__)

app = typer.Typer()


def handle_clipboard_content(content: str) -> str | None:
    content = content.strip()
    url = urlparse.urlparse(content)
    if url.scheme:
        return handle_url(url)
    else:
        return None


def handle_clipboard_X11(primary: bool):
    content = pyperclip.paste(primary=primary)
    new_content = handle_clipboard_content(content)
    if new_content is not None:
        pyperclip.copy(new_content, primary=primary)


def handle_clipboard():
    content = pyperclip.paste()
    new_content = handle_clipboard_content(content)
    if new_content is not None:
        pyperclip.copy(new_content)


async def main():
    if (platform_ := platform.system()) == "Linux":
        pyperclip.set_clipboard("xsel")

    while True:
        proc = await asyncio.create_subprocess_exec("clipnotify")
        await proc.wait()
        log.debug("Clipboard change detected")
        try:
            if platform_ == "Linux":
                handle_clipboard_X11(primary=False)
            else:
                handle_clipboard()
        except Exception as e:
            log.error(f"{e} was raised.")


service_app = typer.Typer()
app.add_typer(service_app, name="service")


@service_app.command()
def install(debug: bool = typer.Option(False, help="Set log level to DEBUG")):
    """
    Install linkfix as a systemd user service.
    """
    service_unit = (Path(__file__).parents[1] / config.unit_fname).read_text()
    service_unit = service_unit.format(
        python_path=sys.executable,
        linkfix_path=Path(__file__).parent,
        args=" --debug" if debug else "",
    )
    target_path = Path("~/.config/systemd/user").expanduser() / config.unit_fname
    target_path.write_text(service_unit)
    typer.echo(f"Created systemd unit file at {target_path}")

    subprocess.run(["systemctl", "--user", "daemon-reload"])
    subprocess.run(["systemctl", "--user", "restart", config.unit_fname.split(".")[0]])
    typer.echo(f"Told systemd to run the service")


@service_app.command()
def remove():
    """
    Remove linkfix systemd user service.
    """
    target_path = Path("~/.config/systemd/user").expanduser() / config.unit_fname
    delete = typer.confirm(f"Will delete {target_path}. Are you sure?")
    if not delete:
        typer.echo("Service not removed.")
        raise typer.Abort()
    subprocess.run(["systemctl", "--user", "stop", config.unit_fname.split(".")[0]])
    typer.echo(f"Told systemd to stop the service")

    target_path.unlink()
    typer.echo(f"Deleted systemd unit file at {target_path}")

    subprocess.run(["systemctl", "--user", "daemon-reload"])


@app.callback(invoke_without_command=True)
def cli_main(
    ctx: typer.Context, debug: bool = typer.Option(False, help="Set log level to DEBUG")
):
    if debug:
        logging.getLogger("").setLevel(logging.DEBUG)

    if ctx.invoked_subcommand is None:
        try:
            if asyncio.get_event_loop().is_closed():
                if platform.system() == "Windows":
                    asyncio.set_event_loop(asyncio.ProactorEventLoop())
                else:
                    asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            loop.run_forever()
        except KeyboardInterrupt:
            print("\nShutting down.")
        finally:
            loop.stop()
            loop.close()


app()
