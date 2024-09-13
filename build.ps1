$exclude = @("venv", "API_Clima_Amazonas.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "API_Clima_Amazonas.zip" -Force