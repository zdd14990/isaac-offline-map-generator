param(
    [Parameter(Mandatory = $true)]
    [string]$TargetAddress,
    [Parameter(Mandatory = $true)]
    [string]$OutputDirectory
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$env:JAVA_HOME = (Resolve-Path (Join-Path $projectRoot "tools\jdk-21.0.12+8")).Path
$ghidra = (Resolve-Path (
    Join-Path $projectRoot "tools\ghidra_12.1.2_PUBLIC\support\analyzeHeadless.bat"
)).Path
$ghidraUser = Join-Path $projectRoot "research\ghidra-user"
$projectDirectory = Join-Path $projectRoot "research\ghidra-project"
$scriptDirectory = Join-Path $projectRoot "scripts\ghidra"
$resolvedOutput = Join-Path $projectRoot $OutputDirectory

New-Item -ItemType Directory -Force -Path `
    $ghidraUser, `
    $resolvedOutput, `
    (Join-Path $ghidraUser "settings"), `
    (Join-Path $ghidraUser "cache"), `
    (Join-Path $ghidraUser "temp"), `
    (Join-Path $ghidraUser "roaming"), `
    (Join-Path $ghidraUser "local") | Out-Null
$env:USERPROFILE = $ghidraUser
$env:APPDATA = Join-Path $ghidraUser "roaming"
$env:LOCALAPPDATA = Join-Path $ghidraUser "local"
$env:GHIDRA_HEADLESS_JAVA_OPTIONS = "-Dapplication.settingsdir=$ghidraUser\settings -Dapplication.cachedir=$ghidraUser\cache -Dapplication.tempdir=$ghidraUser\temp"

& $ghidra $projectDirectory "isaac_static" `
    -process "isaac-ng.exe" `
    -noanalysis `
    -scriptPath $scriptDirectory `
    -postScript "ExportAddressReferences.java" $TargetAddress $resolvedOutput
if ($LASTEXITCODE -ne 0) {
    throw "Ghidra reference export failed with exit code $LASTEXITCODE"
}
