$Request = Invoke-WebRequest -uri "192.168.0.97:666" -Method Get -ContentType "application/json" 

$Request.content