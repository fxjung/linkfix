Fixes weblinks.

## Installation
- Needs Python 3.10

```bash
git clone https://github.com/fxjung/linkfix.git
pip install -e linkfix
linkfix service install
```

- Check service status using `systemctl --user status linkfix`
- Check service logs using `journalctl --user -u linkfix`
- To uninstall the systemd service, run `linkfix service uninstall`