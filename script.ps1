Write-Host "Starting CPU Stress Test - 60 seconds"
$stopTime = [DateTime]::Now.AddSeconds(60)
while ([DateTime]::Now -lt $stopTime) {
    for ($i = 0; $i -lt 100000000; $i++) {
        [math]::Sqrt($i) | Out-Null
    }
    Write-Host "." -NoNewline
}
Write-Host ""
Write-Host "CPU Stress Test Complete!"
 