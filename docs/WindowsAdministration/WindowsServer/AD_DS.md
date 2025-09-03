# Active Directory Domain Service

## Installation

```
Install-ADDSForest -DomainName "lab.local" -DomainNetbiosName "LAB" -SafeModeAdministratorPassword (ConvertTo-SecureString "YourSafeModePassword123" -AsPlainText -Force) -Force
```

### GPO Application

```
Install-ADDSDomainController -DomainName "lab.local" -Credential (Get-Credential) -SafeModeAdministratorPassword (ConvertTo-SecureString "YourSafeModePassword123" -AsPlainText -Force) -Force
```

#### Pro Tips

Assign a static IP before installing AD DS:

```
New-NetIPAddress -InterfaceIndex 12 -IPAddress 192.168.1.10 -PrefixLength 24 -DefaultGateway 192.168.1.1
```

Rename your server before promotion:

```
Rename-Computer -NewName "LAB-DC01"
```

Use Get-WindowsFeature to verify installed roles.


## System AUTH vs Application Auth

## Video:

https://www.youtube.com/watch?time_continue=58&v=OH9a0cBvyxM&embeds_referring_euri=https%3A%2F%2Fgemini.google.com%2F&embeds_referring_origin=https%3A%2F%2Fgemini.google.com&source_ve_path=Mjg2NjY


### Rust way

Using Rust with Active Directory

Integrating Rust with Active Directory can be achieved using the ldap3 crate, which provides a pure-Rust LDAP client library using the Tokio stack. This library supports both synchronous and asynchronous interfaces, making it versatile for different use cases.

Setting Up

To use the ldap3 crate, add it to your Cargo.toml file:

```
[dependencies]
ldap3 = "0.11.5"
```


##### Synchronous Example

Here is an example of performing a synchronous LDAP search:

```
use ldap3::{LdapConn, Scope, SearchEntry};
use ldap3::result::Result;

fn main() -> Result<()> {
let mut ldap = LdapConn::new("ldap://localhost:2389")?;
let (rs, _res) = ldap.search(
"ou=Places,dc=example,dc=org",
Scope::Subtree,
"(&(objectClass=locality)(l=ma*))",
vec!["l"]
)?.success()?;
for entry in rs {
println!("{:?}", SearchEntry::construct(entry));
}
Ok(ldap.unbind()?)
}
```

##### Asynchronous Example

For asynchronous operations, you can use the following example:

```
use ldap3::{LdapConnAsync, Scope, SearchEntry};
use ldap3::result::Result;

#[tokio::main]
async fn main() -> Result<()> {
let (conn, mut ldap) = LdapConnAsync::new("ldap://localhost:2389").await?;
ldap3::drive!(conn);
let (rs, _res) = ldap.search(
"ou=Places,dc=example,dc=org",
Scope::Subtree,
"(&(objectClass=locality)(l=ma*))",
vec!["l"]
).await?.success()?;
for entry in rs {
println!("{:?}", SearchEntry::construct(entry));
}
Ok(ldap.unbind().await?)
}
```

##### Features and Configuration

The ldap3 crate offers several compile-time features:

    1. sync: Synchronous API support (enabled by default).
    2. gssapi: Kerberos/GSSAPI support for integrated Windows authentication in Active Directory domains.

This requires additional dependencies like Clang and Kerberos development libraries on non-Windows platforms.

tls: TLS support using the native-tls crate (enabled by default).

tls-rustls: TLS support using the Rustls library.

To enable GSSAPI support, modify your Cargo.toml:

```
[dependencies]
ldap3 = { version = "0.11.5", features = ["gssapi"] }
```

##### Azure Active Directory

For Azure Active Directory (AAD) authentication, you can use the OpenID Connect protocol. While there is no official Rust library for AAD, you can refer to the Azure REST API Reference to register a client application and authenticate using REST APIs. Alternatively, you can use Python's ADAL library and call it from Rust using cargo modules like PyO3 or rust-cpython


### Conclusion

Using the ldap3 crate, you can easily integrate Rust with Active Directory for both synchronous and asynchronous operations. For Azure Active Directory, leveraging REST APIs or integrating with Python can provide a robust solution.
