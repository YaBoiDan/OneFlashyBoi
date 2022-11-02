$JSON = @"
{
    "Mode":"Off"
}
"@
$JSON
Invoke-WebRequest -uri "192.168.0.97:666" -Method POST -Body $JSON -ContentType "application/json"