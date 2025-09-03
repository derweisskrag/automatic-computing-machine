# Set the download URL for the latest PostgreSQL 17 Windows x64 binaries.
# This URL points to the official community FTP server for the latest stable version.
$url = "https://www.postgresql.org/ftp/pub/postgresql/17/win64/postgresql-17.6-1-win64-binaries.zip"

# Set the destination path for the download.
$destinationPath = "C:\Users\Administrator\Downloads\postgresql-binaries.zip"

# Use Invoke-WebRequest to download the file.
Write-Host "Downloading PostgreSQL binaries..."
Invoke-WebRequest -Uri $url -OutFile $destinationPath

Write-Host "Download complete. File saved to $destinationPath"

# Now, we'll extract the zip file.
Write-Host "Extracting files..."

# Create the installation directory.
$installDir = "C:\Program Files\PostgreSQL"
New-Item -ItemType Directory -Path $installDir -Force

# Expand the archive into the new directory.
# The zip contains a 'pgsql' folder inside, so we'll move its contents up.
Expand-Archive -Path $destinationPath -DestinationPath $installDir
Move-Item -Path "$installDir\pgsql\*" -Destination "$installDir" -Force

Write-Host "Extraction complete. PostgreSQL is now in $installDir"


# Set the paths for your PostgreSQL installation.
$pgHome = "C:\Program Files\PostgreSQL"
$dataDir = "$pgHome\data"
$logFile = "$pgHome\postgresql.log"
$binDir = "$pgHome\bin"

# Navigate to the bin directory.
Set-Location -Path $binDir

Write-Host "Initializing the database cluster..."
# Use initdb.exe to create the data directory.
# We'll use the default locale and a password for the 'postgres' superuser.
# Note: This will prompt you to enter the password.
.\initdb.exe -U postgres -A md5 --pwprompt -D $dataDir
# You will be prompted to enter and confirm a password.

Write-Host "Creating a Windows Service for PostgreSQL..."
# Use pg_ctl.exe to register the service and start it.
.\pg_ctl.exe register -N "PostgreSQL" -D $dataDir -U NT AUTHORITY\NetworkService
.\pg_ctl.exe start -N "PostgreSQL" -D $dataDir -l $logFile

Write-Host "PostgreSQL service is running. You can check its status with Get-Service PostgreSQL."

# Add the PostgreSQL bin directory to the system-wide Path variable.
Write-Host "Adding PostgreSQL to the system Path..."
$path = [Environment]::GetEnvironmentVariable("Path", "Machine")
[Environment]::SetEnvironmentVariable("Path", "$path;$pgHome\bin", "Machine")

Write-Host "Path variable updated. You may need to restart your PowerShell session for the changes to take effect."