; ============================================================
;  PDV - Ponto de Venda
;  Script de instalação — Inno Setup
; ============================================================

#define AppName    "PDV - Caixa"
#define AppVersion "1.0.18"
#define AppPublisher "PaoCariocaPdv"
#define AppExeName "PDV.exe"
#define AppURL "https://github.com/PaoCariocaPdv/pdv-app"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}/releases
DefaultDirName={localappdata}\Programs\PDV
UsePreviousAppDir=no
DefaultGroupName={#AppName}
AllowNoIcons=no
LicenseFile=
OutputDir=installer
OutputBaseFilename=PDV_Setup_v{#AppVersion}
SetupIconFile=icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
WizardResizable=no
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=commandline
UninstallDisplayIcon={app}\{#AppExeName}
UninstallDisplayName={#AppName}
VersionInfoVersion={#AppVersion}
VersionInfoCompany={#AppPublisher}
VersionInfoDescription={#AppName} Setup

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Atalhos:"; Flags: checkedonce
Name: "startmenuicon"; Description: "Criar atalho no Menu Iniciar"; GroupDescription: "Atalhos:"; Flags: checkedonce

[Files]
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\icon.ico"
Name: "{group}\Desinstalar {#AppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon; IconFilename: "{app}\icon.ico"
Name: "{userstartmenu}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: startmenuicon; IconFilename: "{app}\icon.ico"

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Executar {#AppName} agora"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Messages]
WelcomeLabel1=Bem-vindo ao instalador do [name]
WelcomeLabel2=Este assistente irá instalar o [name/ver] no seu computador.%n%nRecomendamos fechar todos os outros aplicativos antes de continuar.%n%nClique em Avançar para continuar.
FinishedHeadingLabel=Instalação Concluída!
FinishedLabelNoIcons=O [name] foi instalado com sucesso no seu computador.
FinishedLabel=O [name] foi instalado com sucesso. Clique em Concluir para fechar o assistente.
ClickFinish=Clique em Concluir para fechar o assistente de instalação.
