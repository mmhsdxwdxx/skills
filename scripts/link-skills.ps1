param(
    [string[]]$Destinations = @((Join-Path $HOME '.codex\skills')),
    [switch]$IncludeDrafts
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$buckets = @('official', 'engineering', 'productivity')
if ($IncludeDrafts) { $buckets += 'in-progress' }

$skillFiles = foreach ($bucket in $buckets) {
    $bucketPath = Join-Path $repo "skills\$bucket"
    if (Test-Path -LiteralPath $bucketPath) {
        Get-ChildItem -LiteralPath $bucketPath -Filter SKILL.md -File -Recurse
    }
}

foreach ($destination in $Destinations) {
    New-Item -ItemType Directory -Force -Path $destination | Out-Null
    foreach ($skillFile in $skillFiles) {
        $source = $skillFile.Directory.FullName
        $name = $skillFile.Directory.Name
        $target = Join-Path $destination $name
        if (Test-Path -LiteralPath $target) {
            $existing = Get-Item -LiteralPath $target -Force
            if ($existing.LinkType) {
                Remove-Item -LiteralPath $target -Force
            } else {
                Write-Warning "Skipping $target because it is a real directory. Move it manually if you want the repository link."
                continue
            }
        }
        try {
            New-Item -ItemType SymbolicLink -Path $target -Target $source | Out-Null
        } catch {
            New-Item -ItemType Junction -Path $target -Target $source | Out-Null
        }
        Write-Host "linked $name -> $source ($destination)"
    }
}
