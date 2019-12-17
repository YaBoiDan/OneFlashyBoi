# Test Webserver
#Invoke-WebRequest -Uri 192.168.2.211:666 -Method POST -ContentType application/json -Body '{"Test":"Test"}'

Param (
    [string] $URI = "192.168.2.211:666"
)

Invoke-WebRequest -Uri $URI

Start-Sleep(1)

$Body = @{
    #Mode = "On"
    Mode = "Off"
    #Mode = "Reload"
}

$Params = @{
    URI = $URI
    Method = "Post"
    ContentType = "application/json"
    Body = $Body | ConvertTo-Json
}

$Response = Invoke-WebRequest @Params
$Response.content | ConvertFrom-Json
