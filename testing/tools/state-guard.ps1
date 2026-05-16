<#
  state-guard.ps1 - preserve/verify/restore a dirty fixture in a target repo
  across Codocu test iterations.

  Usage:
    .\state-guard.ps1 snapshot -Repo <path-to-target-repo>            # capture fixture (read-only on repo)
    .\state-guard.ps1 verify   -Repo <path-to-target-repo>            # PASS if repo unchanged since snapshot
    .\state-guard.ps1 restore  -Repo <path-to-target-repo>            # DRY RUN - prints recovery plan
    .\state-guard.ps1 restore  -Repo <path-to-target-repo> -Execute   # DESTRUCTIVE - recover the fixture

  -Repo is required and has no default: point it at the working copy whose
  dirty state is the test fixture. snapshot/verify never write to the target
  repo. restore is destructive and gated behind -Execute (dry-run by default).

  The snapshot is stored in a `.snapshot/` directory next to this script
  (gitignored). It holds a copy of the target repo's untracked files plus a
  `git stash create` SHA for tracked changes - regenerate it any time with
  `snapshot`; it is local-only and machine-specific.
#>
[CmdletBinding()]
param(
  [Parameter(Position=0,Mandatory=$true)]
  [ValidateSet('snapshot','verify','restore')]
  [string]$Action,
  [Parameter(Mandatory=$true)]
  [string]$Repo,
  [switch]$Execute
)

$ErrorActionPreference = 'Stop'
$snap    = Join-Path $PSScriptRoot '.snapshot'
$shaFile = Join-Path $snap 'stash-sha.txt'
$fpFile  = Join-Path $snap 'fingerprint.txt'
$utDir   = Join-Path $snap 'untracked'

function Get-Untracked($r) {
  $o = git -C $r ls-files --others --exclude-standard
  if (-not $o) { return @() }
  return @($o)
}

function Get-Fingerprint($r) {
  $lines = @()
  $lines += @(git -C $r status --porcelain=v1 | Sort-Object)
  foreach ($f in (Get-Untracked $r | Sort-Object)) {
    $p = Join-Path $r $f
    if (Test-Path -LiteralPath $p -PathType Leaf) {
      $h = (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash
      $lines += "H $f $h"
    }
  }
  return (($lines -join "`n") -replace "`r","")
}

switch ($Action) {

  'snapshot' {
    if (Test-Path $snap) { Remove-Item $snap -Recurse -Force }
    New-Item -ItemType Directory -Path $utDir -Force | Out-Null

    $sha = git -C $Repo stash create
    if ($sha) { $sha = $sha.Trim() } else { $sha = '' }
    if (-not $sha) {
      Write-Warning "git stash create returned empty - no tracked changes. Snapshotting untracked only."
    }
    Set-Content -Path $shaFile -Value $sha -Encoding ascii

    $ut = Get-Untracked $Repo
    foreach ($f in $ut) {
      $src = Join-Path $Repo $f
      $dst = Join-Path $utDir $f
      $dd  = Split-Path $dst -Parent
      if (-not (Test-Path $dd)) { New-Item -ItemType Directory -Path $dd -Force | Out-Null }
      Copy-Item -LiteralPath $src -Destination $dst -Force
    }

    Set-Content -Path $fpFile -Value (Get-Fingerprint $Repo) -Encoding ascii

    $tracked = @(git -C $Repo status --porcelain=v1 | Where-Object { $_ -notmatch '^\?\?' }).Count
    Write-Host "Snapshot OK"
    Write-Host "  repo:            $Repo"
    Write-Host "  stash sha:       $(if ($sha) { $sha } else { '(none)' })"
    Write-Host "  tracked changes: $tracked"
    Write-Host "  untracked saved: $($ut.Count)"
    Write-Host "  snapshot dir:    $snap"
  }

  'verify' {
    if (-not (Test-Path $fpFile)) { throw "No snapshot. Run: state-guard.ps1 snapshot -Repo <path>" }
    $before = ((Get-Content $fpFile -Raw) -replace "`r","").TrimEnd()
    $after  = (Get-Fingerprint $Repo).TrimEnd()
    if ($before -eq $after) {
      Write-Host "VERIFY PASS - repo state unchanged (analysis was read-only)."
      exit 0
    }
    Write-Host "VERIFY FAIL - repo state changed during the run. The run mutated the fixture."
    Write-Host "--- diff: SNAP ONLY = lost, NOW ONLY = introduced ---"
    Compare-Object ($before -split "`n") ($after -split "`n") | ForEach-Object {
      $tag = if ($_.SideIndicator -eq '=>') { 'NOW ONLY ' } else { 'SNAP ONLY' }
      Write-Host "  $tag : $($_.InputObject)"
    }
    Write-Host "Recover with: state-guard.ps1 restore -Repo <path> -Execute"
    exit 1
  }

  'restore' {
    if (-not (Test-Path $shaFile)) { throw "No snapshot. Run snapshot first." }
    $sha   = (Get-Content $shaFile -Raw).Trim()
    $curUt = Get-Untracked $Repo
    $bakUt = @()
    if (Test-Path $utDir) {
      Push-Location $utDir
      $bakUt = @(Get-ChildItem -Recurse -File | ForEach-Object {
        (Resolve-Path -Relative $_.FullName) -replace '^\.\\','' -replace '\\','/'
      })
      Pop-Location
    }

    if (-not $Execute) {
      Write-Host "DRY RUN - would do (re-run with -Execute to apply):"
      Write-Host "  1. git -C $Repo reset --hard HEAD   (drop current tracked changes)"
      if ($sha) { Write-Host "  2. git -C $Repo stash apply $sha   (reapply snapshot tracked state)" }
      Write-Host "  3. delete currently-untracked files ($($curUt.Count)):"
      $curUt | ForEach-Object { Write-Host "       - $_" }
      Write-Host "  4. restore $($bakUt.Count) untracked files from backup"
      Write-Host "DESTRUCTIVE. Nothing changed."
      exit 0
    }

    Write-Host "Restoring..."
    git -C $Repo reset --hard HEAD | Out-Null
    if ($sha) { git -C $Repo stash apply $sha | Out-Null }
    foreach ($f in $curUt) {
      $p = Join-Path $Repo $f
      if (Test-Path -LiteralPath $p) { Remove-Item -LiteralPath $p -Recurse -Force }
    }
    foreach ($f in $bakUt) {
      $src = Join-Path $utDir $f
      $dst = Join-Path $Repo $f
      $dd  = Split-Path $dst -Parent
      if (-not (Test-Path $dd)) { New-Item -ItemType Directory -Path $dd -Force | Out-Null }
      Copy-Item -LiteralPath $src -Destination $dst -Force
    }
    $now  = (Get-Fingerprint $Repo).TrimEnd()
    $orig = ((Get-Content $fpFile -Raw) -replace "`r","").TrimEnd()
    if ($now -eq $orig) { Write-Host "Restore OK - fixture matches snapshot." }
    else { Write-Warning "Restore done but fingerprint differs - inspect manually." }
  }
}
