$JSON = @"
{
    "Mode":"ClearAnyway",
    "Colour":[{
        "R":"255",
        "G":"0",
        "B":"255"
    }]
}
"@
$JSON
Invoke-WebRequest -uri "192.168.1.59:666" -Method POST -Body $JSON -ContentType "application/json"