!define APPNAME "Battery Threshold Manager"
!define COMPANYNAME "Khuram Murad"
!define DESCRIPTION "Manage battery charge thresholds securely"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0

# These will be displayed in Add/Remove Programs
!define HELPURL "https://github.com/KhuramMurad/laptop-battery-manager"
!define UPDATEURL "https://github.com/KhuramMurad/laptop-battery-manager"
!define ABOUTURL "https://github.com/KhuramMurad/laptop-battery-manager"

RequestExecutionLevel admin

InstallDir "$PROGRAMFILES\${APPNAME}"

# Add Icon
Icon "assets/icon.ico"
UninstallIcon "assets/icon.ico"

# Installer Pages
Page license
Page directory
Page instfiles

# Uninstaller Pages
UninstPage uninstConfirm
UninstPage instfiles

# License Information
LicenseText "License Agreement"
LicenseData "LICENSE.txt"

OutFile "battery-threshold-manager-setup.exe"

Section "Install"
    SetOutPath "$INSTDIR"
    
    # Copy main python script renamed to .pyw so it runs without a console window popup
    File /oname=battery-threshold-manager.pyw "battery-threshold-manager-windows.py"
    File "assets/icon.ico"
    
    # Create shortcut in the start menu
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortcut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "pythonw.exe" '"$INSTDIR\battery-threshold-manager.pyw"' "$INSTDIR\icon.ico" 0
    
    # Write uninstall registry keys
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" '"$INSTDIR\uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayIcon" '"$INSTDIR\icon.ico"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${COMPANYNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
    
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\battery-threshold-manager.pyw"
    Delete "$INSTDIR\icon.ico"
    Delete "$INSTDIR\uninstall.exe"
    RMDir "$INSTDIR"
    
    Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
    RMDir "$SMPROGRAMS\${APPNAME}"
    
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
SectionEnd
