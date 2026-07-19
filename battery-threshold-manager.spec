Name:           battery-threshold-manager
Version:        1.0.0
Release:        1%{?dist}
Summary:        Battery Threshold Manager

License:        MIT
URL:            https://github.com/KhuramMurad/laptop-battery-manager

BuildArch:      noarch
Requires:       python3, python3-tkinter, polkit

%description
A graphical utility to manage battery charge threshold limits safely and securely.

%prep
# Nothing to prep, installing from source dir

%build
# Nothing to build (python script)

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/polkit-1/actions

install -m 755 %{_sourcedir}/usr/bin/battery-threshold-manager %{buildroot}%{_bindir}/battery-threshold-manager
install -m 644 %{_sourcedir}/usr/share/applications/battery-threshold-manager.desktop %{buildroot}%{_datadir}/applications/battery-threshold-manager.desktop
install -m 644 %{_sourcedir}/usr/share/polkit-1/actions/org.battery-threshold-manager.policy %{buildroot}%{_datadir}/polkit-1/actions/org.battery-threshold-manager.policy

%files
%{_bindir}/battery-threshold-manager
%{_datadir}/applications/battery-threshold-manager.desktop
%{_datadir}/polkit-1/actions/org.battery-threshold-manager.policy

%changelog
* Sun Jul 19 2026 Ubuntu User <user@ubuntu.com> - 1.0.0-1
- Initial RPM package release
