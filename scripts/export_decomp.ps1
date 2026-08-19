param()

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$env:JAVA_HOME = (Resolve-Path (Join-Path $projectRoot "tools\jdk-21.0.12+8")).Path
$ghidra = (Resolve-Path (Join-Path $projectRoot "tools\ghidra_12.1.2_PUBLIC\support\analyzeHeadless.bat")).Path
$ghidraUser = Join-Path $projectRoot "research\ghidra-user"
$projectDirectory = Join-Path $projectRoot "research\ghidra-project"
$scriptDirectory = Join-Path $projectRoot "scripts\ghidra"
$outputDirectory = Join-Path $projectRoot "research\decomp\ghidra"
New-Item -ItemType Directory -Force -Path `
    $ghidraUser, `
    $outputDirectory, `
    (Join-Path $ghidraUser "settings"), `
    (Join-Path $ghidraUser "cache"), `
    (Join-Path $ghidraUser "temp"), `
    (Join-Path $ghidraUser "roaming"), `
    (Join-Path $ghidraUser "local") | Out-Null
$env:USERPROFILE = $ghidraUser
$env:APPDATA = Join-Path $ghidraUser "roaming"
$env:LOCALAPPDATA = Join-Path $ghidraUser "local"
$env:GHIDRA_HEADLESS_JAVA_OPTIONS = "-Dapplication.settingsdir=$ghidraUser\settings -Dapplication.cachedir=$ghidraUser\cache -Dapplication.tempdir=$ghidraUser\temp"
$started = Get-Date

& $ghidra $projectDirectory "isaac_static" `
    -process "isaac-ng.exe" `
    -noanalysis `
    -scriptPath $scriptDirectory `
    -postScript "ExportIsaacFunctions.java" $outputDirectory
if ($LASTEXITCODE -ne 0) {
    throw "Ghidra decompilation export failed with exit code $LASTEXITCODE"
}
$index = Join-Path $outputDirectory "index.tsv"
if (-not (Test-Path -LiteralPath $index) -or (Get-Item -LiteralPath $index).LastWriteTime -lt $started) {
    throw "Ghidra did not refresh the decompilation index; inspect the headless log"
}
