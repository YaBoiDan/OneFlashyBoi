# Test Webserver
#Invoke-WebRequest -Uri 192.168.2.211:666 -Method POST -ContentType application/json -Body '{"Test":"Test"}'

#Invoke-WebRequest -Uri 192.168.2.211:666 -Method POST -ContentType application/json -Body '{ "Mode": "Manual", "Sticks": [{"StickID": "1","Pixels": [{"PixelID": "1","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "2","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "3","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "4","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "5","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "6","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "7","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "8","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "9","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "10","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "11","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "12","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "13","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "14","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "15","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "16","Colour": "#00FF00","Brightness" : "1" }],"Brightness" : "1"},{"StickID": "2","Pixels": [{"PixelID": "1","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "2","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "3","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "4","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "5","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "6","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "7","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "8","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "9","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "10","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "11","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "12","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "13","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "14","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "15","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "16","Colour": "#00FF00","Brightness" : "1" }],"Brightness" : "1"},{"StickID": "3","Pixels": [{"PixelID": "1","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "2","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "3","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "4","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "5","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "6","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "7","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "8","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "9","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "10","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "11","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "12","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "13","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "14","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "15","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "16","Colour": "#00FF00","Brightness" : "1" }],"Brightness" : "1"},{"StickID": "4","Pixels": [{"PixelID": "1","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "2","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "3","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "4","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "5","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "6","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "7","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "8","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "9","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "10","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "11","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "12","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "13","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "14","Colour": "#00FF00","Brightness" : "1" },{"PixelID": "15","Colour": "#FF0000","Brightness" : "1" },{"PixelID": "16","Colour": "#00FF00","Brightness" : "1" }],"Brightness" : "1"}]}'

Param (
    [string] $URI = "192.168.2.211:666"
)

$ManualModeJSON = @"
{
    "Mode": "Manual",
    "Sticks": [
        {
            "StickID": "1",
            "Colour": "#FF0000",
            "Brightness" : "1"
        },
        {
            "StickID": "2",
            "Colour": "#FF0000",
            "Brightness" : "1"
        },
        {
            "StickID": "3",
            "Colour": "#FF0000",
            "Brightness" : "1"
        },
        {
            "StickID": "4",
            "Colour": "#FF0000",
            "Brightness" : "1"
        }
    ]
}
"@

#$ManualModeJSON | ConvertFrom-Json
Write-Host "----GET----"
$Response = Invoke-WebRequest -Uri $URI
$Response.content | ConvertFrom-Json

Start-Sleep(1)

Write-Host "----POST - ON----"
$Body = @{
    Mode = "On"
    #Mode = "Off"
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

Start-Sleep(10)

Invoke-WebRequest -Uri 192.168.2.211:666 -Method POST -ContentType application/json -Body '{"Mode":"Off"}'

Start-Sleep(1)

Write-Host "----POST - Manual----"
#Manual
Invoke-WebRequest -Uri 192.168.2.211:666 -Method POST -ContentType application/json -Body '{"Mode": "Manual","Sticks": [ { "StickID": "1", "Colour": "#FF0000", "Brightness" : "1" }, { "StickID": "2", "Colour": "#FF0000", "Brightness" : "1" }, { "StickID": "3", "Colour": "#FF0000", "Brightness" : "1" }, { "StickID": "4", "Colour": "#FF0000", "Brightness" : "1" }]}'

Start-Sleep(10)

Invoke-WebRequest -Uri 192.168.2.211:666 -Method POST -ContentType application/json -Body '{"Mode":"Off"}'

Start-Sleep(1)


$SuperManualModeJSON = @"
{
    "Mode": "Manual",
    "Sticks": [
        {
            "StickID": "1",
            "Pixels": [
                {
                    "PixelID": "1",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "2",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "3",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "4",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "5",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "6",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "7",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "8",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "9",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "10",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "11",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "12",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "13",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "14",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "15",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "16",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                }
            ],
            "Brightness" : "1"
        },
        {
            "StickID": "2",
            "Pixels": [
                {
                    "PixelID": "1",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "2",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "3",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "4",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "5",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "6",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "7",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "8",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "9",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "10",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "11",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "12",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "13",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "14",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "15",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "16",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                }
            ],
            "Brightness" : "1"
        },
        {
            "StickID": "3",
            "Pixels": [
                {
                    "PixelID": "1",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "2",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "3",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "4",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "5",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "6",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "7",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "8",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "9",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "10",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "11",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "12",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "13",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "14",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "15",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "16",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                }
            ],
            "Brightness" : "1"
        },
        {
            "StickID": "4",
            "Pixels": [
                {
                    "PixelID": "1",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "2",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "3",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "4",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "5",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "6",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "7",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "8",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "9",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "10",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "11",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "12",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "13",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "14",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "15",
                    "Colour": "#FF0000",
                    "Brightness" : "1"
                },
                {
                    "PixelID": "16",
                    "Colour": "#00FF00",
                    "Brightness" : "1"
                }
            ],
            "Brightness" : "1"
        }
    ]
}
"@

#$SuperManualModeJSON | ConvertFrom-Json

Write-Host "----POST - SuperManual----"

$Params = @{
    URI         = $URI
    Method      = "Post"
    ContentType = "application/json"
    Body        = $SuperManualModeJSON
}

$Response = Invoke-WebRequest @Params
$Response.content | ConvertFrom-Json