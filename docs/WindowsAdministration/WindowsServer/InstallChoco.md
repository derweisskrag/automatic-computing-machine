
## Installing the Chocolatey:


```
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```


## Installing dev tools

To install other tools, we can leverage `choco install` command, as in

```
choco install git -y # installs the git (GitHub manager for repositories and remote access to your GitHub)
```

You can install multiple tools at once:

```
choco install mingw cmake make -y
```

### Insalled mingw:

```
choco install mingw # then type A when it asks permission
```

We got troubles. We had to manually install it on HOST machine (faster the internet), then drag it towards Windows 11 PRO VM and then from there using SMB we passed to Windows Server and then using zip-7 and PowerShell we did:

```
7z x mingw.7z -oC:\mingw64
```

and then we had to

```
[environment]::SetEnvironmentVariable("PATH", "C:\ming64\mingw64\bin", "User") # User -> admin 
```

Source of download: https://github.com/niXman/mingw-builds-binaries/releases


## Installing the cmake

```
choco install cmake --install-arguments="'ADD_CMAKE_TO_PATH=System'"
```

## Installing Rust

```
Invoke-WebRequest -Uri "https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe" -OutFile "rustup-init.exe"
```

### LINK.EXE

To fix the "linker link.exe not found" error by switching to the gnu toolchain, open your PowerShell or Command Prompt and run the following commands:

Add the gnu toolchain to your Rust installation:
rustup toolchain install stable-x86_64-pc-windows-gnu

Set the gnu toolchain as your default:
rustup default stable-x86_64-pc-windows-gnu

After running these commands, navigate back to your hello_world directory and run cargo run again. This time, Rust will use the linker (ld.exe) from your MinGW installation and should compile your program successfully.

