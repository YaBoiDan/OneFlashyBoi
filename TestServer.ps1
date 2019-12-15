# Test Webserver
#Invoke-WebRequest -Uri 192.168.2.211:666 -Method POST -ContentType application/json -Body '{"Test":"Test"}'

$Body = @{
    Mode = "On"
}

$Params = @{
    URI = "http://192.168.2.211:666"
    Method = "Post"
    ContentType = "application/json"
    Body = $Body | ConvertTo-Json
}

$Response = Invoke-WebRequest @Params
$Response.content | ConvertFrom-Json