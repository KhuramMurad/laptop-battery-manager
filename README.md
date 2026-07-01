# Battery Threshold Manager

Battery Threshold Manager is a clean and lightweight graphical user interface (GUI) written in Python 3 using Tkinter for Ubuntu/Debian-based systems. It allows users to manage battery charge threshold limits safely and securely.

## Features

- **Real-time Status**: Reads and displays the current charge end threshold from `/sys/class/power_supply/BAT1/charge_control_end_threshold`.
- **Predefined Limits**: Quickly toggle between a 70% limit (to maximize battery health when plugged in) and a 100% limit (for full capacity).
- **Secure Elevation**: Uses `pkexec` (Polkit/PolicyKit) natively for root operations, meaning only write actions require password authorization, while the rest of the GUI runs under standard user privileges.

## Directory Structure

This project is laid out in the standard Debian package source format:

- `DEBIAN/` - Package metadata (e.g. `control`)
- `usr/bin/` - Main executable Python Tkinter application
- `usr/share/applications/` - Desktop launcher configuration (`.desktop`)
- `usr/share/polkit-1/actions/` - Polkit policy configuration XML for secure root access

## How to Build the Package

To compile this project into a `.deb` package:

```bash
dpkg-deb --build . ../battery-threshold-manager_1.0.0_all.deb
```

## How to Install the Package

Install the generated `.deb` package using `apt`:

```bash
sudo apt update
sudo apt install ../battery-threshold-manager_1.0.0_all.deb
```

## License

This project is licensed under the MIT License.
