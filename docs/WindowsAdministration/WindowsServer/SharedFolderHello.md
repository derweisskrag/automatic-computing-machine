## 📁 Windows Server 2022 File Sharing Setup – Access from Windows 11 Client

### 🎯 **Objective**

Enable a Windows 11 Pro client to access a folder on Windows Server 2022 and read a file (`hello_world.txt`) over the local network.

---

### 🧠 **Reasoning Behind the Setup**

- Both machines are on the same subnet (`192.168.1.49` and `192.168.1.50`), so direct network access is possible.
- The server’s firewall must allow **File and Printer Sharing** and **Network Discovery** for SMB access.
- A shared folder must be created and permissions configured to allow access.
- The file must be created with content and placed inside the shared folder.
- The client accesses the folder using UNC path: `\\192.168.1.49\hello`

---

## 🛠️ Step-by-Step Commands

### ✅ 1. Create Folder on Server
```powershell
mkdir C:\Users\Administrator\hello
cd C:\Users\Administrator\hello
```

### ✅ 2. Create File with Content
```powershell
Set-Content -Path "hello_world.txt" -Value "Hello, World!"
```

### ✅ 3. Share the Folder Over Network
```powershell
New-SmbShare -Name "hello" -Path "C:\Users\Administrator\hello" -FullAccess "Everyone"
```

> You can replace `"Everyone"` with a specific user or group for tighter control.

### ✅ 4. Enable Firewall Rules for Sharing
```powershell
Enable-NetFirewallRule -DisplayGroup "File and Printer Sharing"
Enable-NetFirewallRule -DisplayGroup "Network Discovery"
```

### ✅ 5. (Optional) Set NTFS Permissions
```powershell
icacls "C:\Users\Administrator\hello" /grant Everyone:(R)
```

> Use `(F)` instead of `(R)` for full access.

---

### 🧪 6. Access from Windows 11 Client

- Open File Explorer
- Enter:
  ```
  \\192.168.1.49\hello
  ```
- Open `hello_world.txt` and confirm contents

