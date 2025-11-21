# PowerShell script to update DevContainer settings from environment variables

param(
    [string]$EnvFile = ".env.devcontainer",
    [string]$DevContainerPath = ".devcontainer/devcontainer.json",
    [string]$DockerComposePath = "docker-compose.yml"
)

# Check if environment variable file exists
if (-not (Test-Path $EnvFile)) {
    Write-Error "Environment variable file not found: $EnvFile"
    exit 1
}

# Load environment variables
Write-Host "Loading environment variables: $EnvFile" -ForegroundColor Cyan
$envVars = @{}
Get-Content $EnvFile | ForEach-Object {
    $line = $_.Trim()
    # Skip comment lines and empty lines
    if ($line -and -not $line.StartsWith("#")) {
        $parts = $line -split "=", 2
        if ($parts.Length -eq 2) {
            $key = $parts[0].Trim()
            $value = $parts[1].Trim()
            $envVars[$key] = $value
            Write-Host "  $key = $value" -ForegroundColor Gray
        }
    }
}

# Check required environment variables
$requiredVars = @("DEVCONTAINER_NAME", "SERVICE_NAME", "CONTAINER_NAME")
foreach ($var in $requiredVars) {
    if (-not $envVars.ContainsKey($var)) {
        Write-Error "Required environment variable is not set: $var"
        exit 1
    }
}

# Update devcontainer.json
Write-Host "`nUpdating devcontainer.json..." -ForegroundColor Cyan
if (-not (Test-Path $DevContainerPath)) {
    Write-Error "devcontainer.json not found: $DevContainerPath"
    exit 1
}

# Resolve to absolute path
$DevContainerPathAbsolute = (Resolve-Path $DevContainerPath).Path

$devContainerContent = Get-Content $DevContainerPath -Raw -Encoding UTF8

# Extract current values for display
if ($devContainerContent -match '"name"\s*:\s*"([^"]+)"') {
    $oldName = $matches[1]
}
if ($devContainerContent -match '"service"\s*:\s*"([^"]+)"') {
    $oldService = $matches[1]
}

# Update name and service using regex to preserve formatting
$updatedContent = $devContainerContent -replace '"name"\s*:\s*"[^"]+"', "`"name`": `"$($envVars['DEVCONTAINER_NAME'])`""
$updatedContent = $updatedContent -replace '"service"\s*:\s*"[^"]+"', "`"service`": `"$($envVars['SERVICE_NAME'])`""

Write-Host "  name: $oldName -> $($envVars['DEVCONTAINER_NAME'])" -ForegroundColor Yellow
Write-Host "  service: $oldService -> $($envVars['SERVICE_NAME'])" -ForegroundColor Yellow

# Save without reformatting, preserving line endings (no BOM)
[System.IO.File]::WriteAllText($DevContainerPathAbsolute, $updatedContent, [System.Text.UTF8Encoding]::new($false))
Write-Host "  ✓ Update complete" -ForegroundColor Green

# Update docker-compose.yml
Write-Host "`nUpdating docker-compose.yml..." -ForegroundColor Cyan
if (-not (Test-Path $DockerComposePath)) {
    Write-Error "docker-compose.yml not found: $DockerComposePath"
    exit 1
}

# Resolve to absolute path
$DockerComposePathAbsolute = (Resolve-Path $DockerComposePath).Path

$composeContent = Get-Content $DockerComposePath -Raw -Encoding UTF8

# Update service name using regex to preserve formatting
$oldServiceName = ""
if ($composeContent -match "services:\s*\r?\n\s+(\S+):") {
    $oldServiceName = $matches[1]
    $composeContent = $composeContent -replace "(services:\s*\r?\n\s+)\S+:", "`$1$($envVars['SERVICE_NAME']):"
    Write-Host "  Service name: $oldServiceName -> $($envVars['SERVICE_NAME'])" -ForegroundColor Yellow
}

# Update container_name using regex to preserve formatting
$oldContainerName = ""
if ($composeContent -match "container_name:\s*(\S+)") {
    $oldContainerName = $matches[1]
    $composeContent = $composeContent -replace "(container_name:\s*)\S+", "`$1$($envVars['CONTAINER_NAME'])"
    Write-Host "  container_name: $oldContainerName -> $($envVars['CONTAINER_NAME'])" -ForegroundColor Yellow
}

# Write to file preserving line endings and formatting
[System.IO.File]::WriteAllText($DockerComposePathAbsolute, $composeContent, [System.Text.UTF8Encoding]::new($false))
Write-Host "  ✓ Update complete" -ForegroundColor Green

Write-Host "`nAll settings have been successfully updated!" -ForegroundColor Green
Write-Host "Please restart the DevContainer to apply the changes." -ForegroundColor Cyan
