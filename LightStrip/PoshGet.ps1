$JSON = @"
{
    "Mode":"Off"
}
"@

Invoke-WebRequest -uri "192.168.1.59:666" -Method Get -ContentType "application/json" #-Body $JSON 