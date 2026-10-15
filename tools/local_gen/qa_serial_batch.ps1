param(
  [Parameter(Mandatory = $true)][string]$BatchManifest,
  [Parameter(Mandatory = $true)][string]$StudioRoot,
  [Parameter(Mandatory = $true)][string]$PythonExe,
  [Parameter(Mandatory = $true)][string]$QaScript
)

$ErrorActionPreference = 'Stop'
$items = Get-Content -LiteralPath $BatchManifest -Raw -Encoding utf8 | ConvertFrom-Json
$logDir = Join-Path $StudioRoot 'reports\qa_logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

foreach ($item in $items) {
  $shotDir = Join-Path $StudioRoot "$($item.category)\$($item.folder)"
  $video = Join-Path $shotDir "attempts\$($item.run_id)\$($item.output_name)"
  $previewDir = Join-Path $shotDir "previews\v1"
  $log = Join-Path $logDir "$($item.shot_id)_decode.log"
  if (-not (Test-Path -LiteralPath $video)) {
    Write-Output "FAIL $($item.shot_id): video missing"
    continue
  }

  & $PythonExe $QaScript --video $video --output-dir $previewDir *> $log
  if ($LASTEXITCODE -ne 0) {
    Write-Output "FAIL $($item.shot_id): decoder exit $LASTEXITCODE; see $log"
    continue
  }
  $report = Get-Content -LiteralPath (Join-Path $previewDir 'decode_report.json') -Raw -Encoding utf8 | ConvertFrom-Json
  if (-not $report.decode_ok) {
    Write-Output "FAIL $($item.shot_id): decoded $($report.decoded_frames)/$($report.declared_frames)"
    continue
  }
  Write-Output "DECODED $($item.shot_id) | $($report.decoded_frames) frames | $($report.resolution[0])x$($report.resolution[1])"
}

Write-Output 'SERIAL QA BATCH FINISHED'
