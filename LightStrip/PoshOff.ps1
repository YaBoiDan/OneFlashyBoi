$JSON = @"
{
    "Mode":"Off"
}
"@
$JSON
Invoke-WebRequest -uri "192.168.1.59:666" -Method POST -Body $JSON -ContentType "application/json"