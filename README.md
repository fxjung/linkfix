Fixes weblinks.

## Installation
- Needs Python 3.10
- Running it as a service requires Linux and `systemd`
- Should work on Windows, so far this hasn't been tested, though.

```bash
git clone https://github.com/fxjung/linkfix.git
pip install -e linkfix
linkfix service install
```

- Check service status using `systemctl --user status linkfix`
- Check service logs using `journalctl --user -u linkfix`
- To uninstall the systemd service, run `linkfix service uninstall`