PowerShell Disk Space Commands
This document contains two useful PowerShell commands for checking the disk space on your C: drive.
Simple Command (Easy to Read)
This command uses the Get-Volume cmdlet to show the disk space in a clean, human-readable format. It's the perfect one to use for a quick check.

```
Get-Volume -DriveLetter C
```

Detailed Command (For Documentation)
This command uses Get-PSDrive and custom properties to display the used, free, and total space in gigabytes (GB), formatted to two decimal places. This is a great way to get a precise reading and document your process.

```
Get-PSDrive C | Format-List -Property @{label="Total Size (GB)"; expression={[math]::Round($_.Used/1GB + $_.Free/1GB, 2)}}, @{label="Free Space (GB)"; expression={[math]::Round($_.Free/1GB, 2)}}, @{label="Used Space (GB)"; expression={[math]::Round($_.Used/1GB, 2)}}
```

```
Get-CimInstance -ClassName Win32_LogicalDisk | Select-Object DeviceID, VolumeName,
@{Name="FreeSpace(GB)";Expression={[math]::Round($_.FreeSpace / 1GB, 2)}},
@{Name="TotalSize(GB)";Expression={[math]::Round($_.Size / 1GB, 2)}},
@{Name="Free(%)";Expression={[math]::Round(($_.FreeSpace / $_.Size) * 100, 2)}}
```


