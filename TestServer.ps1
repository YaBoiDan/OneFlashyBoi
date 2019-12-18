# Test Webserver
#Invoke-WebRequest -Uri 192.168.2.211:666 -Method POST -ContentType application/json -Body '{"Test":"Test"}'

Param (
    [string] $URI = "192.168.2.211:666"
)

$ManualModeJSON = @"
{
    "Mode": "on",
    "Sticks": [
        {
            "StickID": "1",
            "Colour": "RRGGBB",
            "Brightness" : "1"
        },
        {
            "StickID": "2",
            "Colour": "RRGGBB",
            "Brightness" : "1"
        },
        {
            "StickID": "3",
            "Colour": "RRGGBB",
            "Brightness" : "1"
        },
        {
            "StickID": "4",
            "Colour": "RRGGBB",
            "Brightness" : "1"
        }
    ]
}
"@

#$ManualModeJSON | ConvertFrom-Json

Invoke-WebRequest -Uri $URI

Start-Sleep(1)

$Body = @{
    #Mode = "On"
    Mode = "Off"
    #Mode = "Reload"
}

$Params = @{
    URI         = $URI
    Method      = "Post"
    ContentType = "application/json"
    Body        = $Body | ConvertTo-Json
}

$Response = Invoke-WebRequest @Params
$Response.content | ConvertFrom-Json

#Manual
Invoke-WebRequest -Uri 192.168.2.211:666 -Method POST -ContentType application/json -Body '{"Mode": "Manual","Sticks": [ { "StickID": "1", "Colour": "RRGGBB", "Brightness" : "1" }, { "StickID": "2", "Colour": "RRGGBB", "Brightness" : "1" }, { "StickID": "3", "Colour": "RRGGBB", "Brightness" : "1" }, { "StickID": "4", "Colour": "RRGGBB", "Brightness" : "1" }]}'