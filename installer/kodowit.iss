[Setup]
AppId=KODOWIT.Studio.Desktop
AppName=KODOWIT Studio
AppVersion=1.0.1
DefaultDirName={localappdata}\Programs\KODOWIT Studio
DefaultGroupName=KODOWIT Studio
PrivilegesRequired=lowest
OutputDir=..\dist
OutputBaseFilename=KODOWIT-1.0.1-Setup
UninstallDisplayIcon={app}\KODOWIT-Studio.exe
Compression=lzma2
SolidCompression=yes
[Languages]
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"
[Files]
Source: "..\dist\KODOWIT-Studio\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"
[Icons]
Name: "{group}\KODOWIT Studio"; Filename: "{app}\KODOWIT-Studio.exe"
[Run]
Filename: "{app}\KODOWIT-Studio.exe"; Description: "Uruchom KODOWIT Studio"; Flags: postinstall nowait skipifsilent
