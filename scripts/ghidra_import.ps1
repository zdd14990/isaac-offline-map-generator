param(
    [string]$PeCopy = "research\input\isaac-ng.exe"
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$resolvedPe = (Resolve-Path (Join-Path $projectRoot $PeCopy)).Path
$expectedPe = (Resolve-Path (Join-Path $projectRoot "research\input\isaac-ng.exe")).Path
if ($resolvedPe -ne $expectedPe) {
    throw "Safety guard: only the copied research/input/isaac-ng.exe may be imported"
}

$actualHash = (Get-FileHash -LiteralPath $resolvedPe -Algorithm SHA256).Hash.ToLowerInvariant()
$expectedHash = "3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b"
if ($actualHash -ne $expectedHash) {
    throw "Unsupported copied executable hash: $actualHash"
}

$env:JAVA_HOME = (Resolve-Path (Join-Path $projectRoot "tools\jdk-21.0.12+8")).Path
$ghidra = (Resolve-Path (Join-Path $projectRoot "tools\ghidra_12.1.2_PUBLIC\support\analyzeHeadless.bat")).Path
$ghidraUser = Join-Path $projectRoot "research\ghidra-user"
$projectDirectory = Join-Path $projectRoot "research\ghidra-project"
New-Item -ItemType Directory -Force -Path `
    $ghidraUser, `
    $projectDirectory, `
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
    -import $resolvedPe `
    -overwrite `
    -analysisTimeoutPerFile 1800
if ($LASTEXITCODE -ne 0) {
    throw "Ghidra headless import failed with exit code $LASTEXITCODE"
}
