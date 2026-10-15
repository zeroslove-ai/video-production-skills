param(
  [Parameter(Mandatory = $true)][string]$BatchManifest,
  [Parameter(Mandatory = $true)][string]$StudioRoot,
  [Parameter(Mandatory = $true)][string]$ComfyInput,
  [Parameter(Mandatory = $true)][string]$ComfyOutput,
  [Parameter(Mandatory = $true)][string]$Runner,
  [Parameter(Mandatory = $true)][string]$PythonExe,
  [Parameter(Mandatory = $true)][string]$NvidiaSmi,
  [Parameter(Mandatory = $true)][string]$CommonNegativePrompt,
  [string]$Api = 'http://127.0.0.1:8190',
  [int]$ComfyPid = 33284,
  [int]$QueueWaitTimeoutSeconds = 1800
)

$ErrorActionPreference = 'Stop'
$items = Get-Content -LiteralPath $BatchManifest -Raw -Encoding utf8 | ConvertFrom-Json
$negative = Get-Content -LiteralPath $CommonNegativePrompt -Raw -Encoding utf8
$logDir = Join-Path $StudioRoot 'reports\batch_logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

foreach ($item in $items) {
  $queueWaitStart = Get-Date
  do {
    $queue = Invoke-RestMethod -Uri "$Api/queue" -TimeoutSec 15
    $busy = (@($queue.queue_running).Count -gt 0) -or (@($queue.queue_pending).Count -gt 0)
    if ($busy) {
      if (((Get-Date) - $queueWaitStart).TotalSeconds -gt $QueueWaitTimeoutSeconds) {
        throw "ComfyUI queue stayed busy too long before $($item.shot_id); leaving existing work untouched."
      }
      Start-Sleep -Seconds 10
    }
  } while ($busy)

  $attemptsParent = Join-Path $StudioRoot "$($item.category)\$($item.folder)\attempts"
  New-Item -ItemType Directory -Force -Path $attemptsParent | Out-Null
  $runDir = Join-Path $attemptsParent $item.run_id
  if (Test-Path -LiteralPath $runDir) {
    Write-Output "SKIP $($item.shot_id): run directory already exists ($runDir)"
    continue
  }

  $logPath = Join-Path $logDir "$($item.shot_id)_$($item.run_id).log"
  $inputPath = Join-Path $ComfyInput $item.image_name
  $arguments = @(
    $Runner,
    '--api', $Api,
    '--input', $inputPath,
    '--image-name', $item.image_name,
    '--comfy-output', $ComfyOutput,
    '--run-dir', $runDir,
    '--nvidia-smi', $NvidiaSmi,
    '--comfy-pid', "$ComfyPid",
    '--seed', "$($item.seed)",
    '--width', "$($item.width)",
    '--height', "$($item.height)",
    '--frames', "$($item.frames)",
    '--timeout-seconds', '1800',
    '--prefix', $item.prefix,
    '--output-name', $item.output_name,
    '--prompt', $item.prompt,
    '--negative-prompt', $negative
  )

  $start = Get-Date
  & $PythonExe @arguments *> $logPath
  $exitCode = $LASTEXITCODE
  if ($exitCode -ne 0) {
    Write-Output "FAIL $($item.shot_id): runner exit $exitCode; see $logPath"
    continue
  }

  $metricsPath = Join-Path $runDir 'metrics.json'
  if (-not (Test-Path -LiteralPath $metricsPath)) {
    Write-Output "FAIL $($item.shot_id): metrics.json missing; see $logPath"
    continue
  }
  $metrics = Get-Content -LiteralPath $metricsPath -Raw -Encoding utf8 | ConvertFrom-Json
  $elapsed = [math]::Round(((Get-Date) - $start).TotalSeconds, 1)
  $peak = ($metrics.gpu_samples | Measure-Object -Property memory_used_mib -Maximum).Maximum
  Write-Output "DONE $($item.shot_id) | $($metrics.status) | ${elapsed}s | peak ${peak}MiB"
}

Write-Output 'SERIAL BATCH FINISHED'
