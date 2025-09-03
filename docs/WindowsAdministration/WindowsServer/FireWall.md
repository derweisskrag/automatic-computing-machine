## 🛡️ Windows Server 2022 Firewall & ICMP Setup via PowerShell

### 📍 Initial Firewall Status Check
```powershell
Get-NetFirewallProfile | Format-Table Name, Enabled
```

### 🔄 Enable or Disable Firewall
```powershell
Set-NetFirewallProfile -All -Enabled True   # Enable all profiles
Set-NetFirewallProfile -All -Enabled False  # Disable all profiles
```

### 📜 List All Active Firewall Rules
```powershell
Get-NetFirewallRule | Where-Object {$_.Enabled -eq "True"} | Format-Table Name, Direction, Action, Enabled
```

### ➕ Create New Firewall Rule (Example: Allow HTTP)
```powershell
New-NetFirewallRule -DisplayName "Allow HTTP" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow
```

### ❌ Remove Firewall Rule
```powershell
Remove-NetFirewallRule -DisplayName "Allow HTTP"
```

---

## 📶 Enable ICMP (Ping) Access

### ✅ Allow All ICMPv4 (Ping) Requests
```powershell
netsh advfirewall firewall add rule name="Allow ICMPv4-In" protocol=icmpv4:8,any dir=in action=allow
```

### ✅ Allow Ping Only from Specific IP (Windows 11 VM)
```powershell
New-NetFirewallRule -DisplayName "Allow Ping from Win11" -Direction Inbound -Protocol ICMPv4 -RemoteAddress 192.168.1.50 -Action Allow
```

---

## 🌐 Network Profile Check & Adjustment

### 🔍 Check Current Network Profile
```powershell
Get-NetConnectionProfile
```

### 🔧 Set Network Profile to Private
```powershell
Set-NetConnectionProfile -InterfaceAlias "Ethernet" -NetworkCategory Private
```

---

## 🧪 Connectivity Test

### 🔍 Ping Test from Windows 11
```bash
ping 192.168.1.49
```

### 🔍 Port Test (e.g., RDP)
```powershell
Test-NetConnection -ComputerName 192.168.1.49 -Port 3389
```
