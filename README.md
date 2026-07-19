# Battery Threshold Manager

<p align="center">
  <img src="assets/icon.svg" width="160" height="160" alt="Battery Threshold Manager Icon">
</p>

Battery Threshold Manager is a clean and lightweight graphical user interface (GUI) written in Python 3 using Tkinter for Ubuntu/Debian-based systems. It allows users to manage battery charge threshold limits safely and securely.

## Features

- **Dynamic Compatibility Check**: Scans `/sys/class/power_supply` on startup for battery control threshold compatibility, dynamically using the correct interface (e.g. `BAT0`, `BAT1`), and displays detailed diagnostic reports if unsupported.
- **Predefined Limits**: Quickly toggle between an 80% limit (to maximize battery health when plugged in) and a 100% limit (for full capacity).
- **Secure Elevation**: Uses `pkexec` (Polkit/PolicyKit) natively for root operations, meaning only write actions require password authorization, while the rest of the GUI runs under standard user privileges.

## Directory Structure

This project is laid out in the standard Debian package source format:

- `DEBIAN/` - Package metadata (e.g. `control`)
- `usr/bin/` - Main executable Python Tkinter application (Linux version)
- `usr/share/applications/` - Desktop launcher configuration (`.desktop`)
- `usr/share/polkit-1/actions/` - Polkit policy configuration XML for secure root access
- `battery-threshold-manager-windows.py` - Separate executable Python Tkinter application (Windows version using native WMI/PowerShell)

## How to Build the Packages

### Debian/Ubuntu (.deb)
To compile this project into a `.deb` package:
```bash
dpkg-deb --build . ../battery-threshold-manager_1.0.0_all.deb
```

### Fedora/RHEL (.rpm)
To compile this project into an `.rpm` package:
```bash
mkdir -p rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
rpmbuild --define "_topdir $PWD/rpmbuild" --define "_sourcedir $PWD" -bb battery-threshold-manager.spec
```

### Windows (.exe installer)
To compile the Windows installer (requires `nsis` / `makensis`):
```bash
convert -background none -resize 256x256 assets/icon.svg assets/icon.ico
makensis installer.nsi
```

## How to Install the Packages

### Debian/Ubuntu (.deb)
Install the generated `.deb` package using `apt`:
```bash
sudo apt update
sudo apt install ../battery-threshold-manager_1.0.0_all.deb
```

### Fedora/RHEL (.rpm)
Install the generated `.rpm` package using `dnf` or `rpm`:
```bash
sudo dnf localinstall rpmbuild/RPMS/noarch/battery-threshold-manager-1.0.0-1.noarch.rpm
```

### Windows (.exe installer)
Run the generated `battery-threshold-manager-setup.exe` installer and follow the wizard. The installer runs natively and configures battery limits via WMI / PowerShell for supported vendors (Lenovo, ASUS, Dell). UAC admin privileges are requested on launch to configure the threshold parameters.

## License

This project is licensed under the MIT License.
