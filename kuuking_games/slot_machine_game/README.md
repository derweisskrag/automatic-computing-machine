# Solution 1: Console App

## Table of Contents

- [Description](#description)
    - [Classes](#classes)
        - [User](#user)
        - [Wallet](#wallet)
        - [Auxiliary classes](#auxiliary-classes)
        - [History & Statistics](#history--statistics)
- [Machine Brain](#machine-brain)
    - [Rust Service](#rust-as-the-brain)
        - [Introduction](#introduction)
        - [Integration Into C#](#integration-into-c)
        - [What services?](#what-services)
    - [C# Service | MS Daemon](#c-as-the-brain)
        - [Introduction](#introduction-1)
        - [How to achieve my goal?](#how-to-achieve-my-goal)
- [Testing](#testing)
    - [Unittests](#unittests)
    - [Integration Tests](#integration-tests)
- [Performance](#performance)


## Description

I will use C# and Rust for this implementation. Python job would be analyze Math file and make some statistics based
on which I could use Rust for computational power (performance or C++), and then C# just implements bussiness logic
clear and concise.

### Classes

#### User

In this example, I use the User class for storing and manipulating data with User. What kind of fields User must have?

According to requirements:

- Name: string;
- Balance: their account & money related // wallet
- History (to maintain statistics)

In other words, quite simple class. Not mentioned in the Requirements:

> User might update their balance. If true, we can add extra functionality to this test 
assignment and let users play until they run out of money.

#### Wallet 

Or, also, known as "MoneyBug" (naming can be edited at any moment). So, the functionality is pretty simple:

- Create wallet once user.

```cs

public static void Main(){
    User user = new User("Jake", new MoneyBug()); 
}
```
This isnt something that I really wanted, but I also wanna keep, because it is not essentially bad: you can give something like

```cs
User user = new User(UserData, Options);
```

as long as we handle different constructors. Actually, I will test and benchmark it. So, do not worry. 

Another important part is to work with wallet. It contains Enum called `currency` and is used to define the currency of money. The default is "$" - USD (U. S. Dollar). It can be changed to any other as default:

```cs
public class Money {
    private Currency Currency { get; } = Currency.USD; // U.S. dollar is default
    public decimal Amount { get; } = 0.0m; // amount of dollars
}
```

In other words, inside MoneyBag (Wallet), we have Money (class) that represents money. It is convenient to 
change the currency of them. For example,

```cs
public class Money {
    /* code above */
    private static Dictionary<Currency, decimal> exchangeRates = new Dictionary<Currency, decimal>();


    public void ChangeCurrencyTo(Currency currency){
        // not static
        // check if nothing to convert to
        if(Currency == currency) return;

        // Try
        decimal FromCurrency = ExchangeRates.GetValueOrDefault(Currency);
        decimal ToCurrency = ExchangeRates.GetValueOrDefault(currency);
        
        // Convert
        Amount = _utilities.ConvertTo(Amount, FromCurrency, ToCurrency);
        Currency = currency;
    }

}
```

> I would like to remind myself that here, we can use OOP. For example, int.Parse("5"); works, right? 
So why not `Balance.ChangeCurrencyTo(Currency.EUR)`? Ah, yes, it is STATIC.

The implementation is straightforward:

```cs

public static Money ChangeCurrencyTo(
    decimal Amount, 
    Currency FromCurrency, 
    Currency ToCurrency
){
    // check if valid
    if (Amount < 0)
        throw new InsufficientFundsException(
            $"Cannot convert {Amount}" + 
            $"from {FromCurrency} to {ToCurrency} due to negative amount of money! Error!"
        );

    // Convert
    Utilities utils = new Utilities();
    decimal FromRate = Money.ExchangeRates.GetValueOrDefault(FromCurrency);
    decimal ToRate = Money.ExchangeRates.GetValueOrDefault(ToCurrency),

    decimal ConvertedAmount = utils.ConvertTo(
        Amount,
        FromRate,
        ToRate 
    );

    return new Money(ConvertedAmount, ToCurrency);
}
```

So, what we just covered? How the system of conversion money works! It is covered in UnitTests.

#### Auxiliary classes

As we just showed, we have 

- Utilities
- ExchangeRate
- Money 
- MoneyBug

They help and modularize the process of working with user within the service 

> Please, notice that in real world, instead of these classes, we actually have Services to work with
money and data. For example: JwtService for JWT, MailServer for email, and now we can do `MoneyService.cs`,
for example. However, my main task here was to simulat the slot machine, not the user and money. It was done 
for formality. As we done with User and its data, we have to store wins or loses. How do we so?

#### History & Statistics

I believe that for simplicity, I just add another class called `UserHistory.cs` and that is it. I can store, manipulate 
and even "serialize" or "deserialize" the data used by User as necessary. 

According to Requirements, it must have the following fields:

```txt
Win Stats example outcome:
==========================================
RTP: 210.00%, Spins: 10, Total bet: 100, Total win: 210
Win Stats:
  "777"     - 0 hit, Total win: 0
  "Cherry"  - 1 hit, Total win: 180
  "Bar"     - 3 hits, Total win: 30
  "Wild"    - 0 hit, Total win: 0
```

So, we can instead use Dictionary or class. I will try Dictionary and class for experimentation, why not.

## Machine Brain

This sectiona is called the brain of the slot machine. All information is hidden and not published to people who are not involved. How  to achieve this goal? I will use SQLite. Why? Unlike plain text or CSV, SQLite has the built-in encryption, even if it is basic, it is definitely advantage over the plain text or hard-coded values. 

### Rust as the brain

#### Introduction

The main objective of Rust is to work with the random (determines if we get the combination or not) and SQLite service. That is basically it. I will NOT use my DoublyLinkedList implemented in Python from DSA (even though I can) to implement LRU or MRU cache mechanisms. I should use C# own mechanisms from `Unity.Runtime` namespace. That will be idiomatic and simple. 

#### Integration Into C#

I used DLL to integrate Rust into C#, and I had to use `toml` and `cargo` to download all necessary packaged to `build & release` my Rust library for C#.

- rusqlite
- rand

For testing the performnace against C#, I also included the `change_to_currency`
function having the `const` signature to mean that it is inlined and optimized for direct calculation. For C#, I have the same logic, so we can benchmark those (it helps me to realize the trade offs.):

```rs
const fn add(a: f32, b: f32) -> f32 {
    a + b
}
```

Notice that this works now for Stable Rust version, but use it like

```rs
fn main(){
    let result = add(1.0, 2.0);
    println!("The result is {}", result);
}
```

After, I create Rust service to let C# interact with SQLite database.

> Please, notice! C# part (same service created for comparison) is going to leverage Microsoft SQL Daemon) and Entity Framework. So, I will use the `Model.cs` to integrate my `User.cs` into MS SQL Daemon in order to make ASYNC connections to DB. 

> I would like to point out that for local DB, I should use SYNC, and to verify this, I must benchmark and test everything. Words are not enough.

#### What services?

Nope! 

> I decided not to proceed with this idea. Rust should behave as API in this case, running server, and I am out of time. FFI for DB service is a bad idea. Glad I learned this way! 
It would be better to use C/C++ for this task (SQLite FFI service, but the best is to use Azure or C# native DB -> So, I will proceed with C# Solution!)

Pretty simple? So,

```
Welcome to the Console Application, Jake! 

Enter:
1-do one spin
2-do 10 spins
3-withdraw money
4-exit

/* Bet is set automatically */

> 1
> You won 100 Dollars! Do you want to continue(y/n)?
> n

Enter:
1-do one spin
2-do 10 spins
3-withdraw money
4-exit

> 3
> Starting to withdraw the money...
> Balance is valid! Withdrawing...
> Success! Money are transacted to your Bank Account
> Do you wanna continue or exit (y/n)?
> n

/* exits

    Action is confirmed once they send "n" to the server.
 */
```

So, as you can see, the system is quite simple. All we do is continuosly run the program and prompt user. So, we have to create a table for DB and then based on this table, we can conclude if they won or lost. So:

- Create table
- Insert secured data (SQLite provides encryption)
- Create the logic for the game (use rand crate to get 3 symbols from the symbols allowed. We store them in DB as well for security)
- Do spin -> calls Rust function that reads from DB to get symbols and caches them (to avoid doing same requests). Engine computes the result and then verifies it for user: win / lose.

```
> 1
> You lose! 
> 1 
> Error! Insufficient funds! Please, deposit the specific amount of money to do one pin!
```

So, we call it and it returns the result. All we need is to check if there is result: Win or Lose, we are fine. If there is Error, we handle gracefully without shutting down the system. 


> Docs Done: 14.12.2024
> Day of work: I worked the second day
> New idea: We can simulate Bank for updating cash. Kotlin can be our Bank. Real quick to set up NEXT.js + Kotlin and use gRCP for RESTful API.

> Do not work today. Rest and prepare to create Rust service and then immediately NEXT.js + Kotlin in one day: I will leverage UIVerse.com and NextUI. I do NOT do CLERK.js or NEXT-AUTH, as my only task is to simulate Bank. I have to do running service. 

> I send the jwt token to Kotlin server to just say `Hey, this user is logged`.

### C# as the brain

#### Introduction

In order to compare the performance and see which approach is the best, I will use C# own mechanism too. Why not? I am curious and the requirement never said I should stick to one or another. 

#### How to achieve my goal?

- I have to download MS SQL db
- Using `dotnet`, I have to add all necessary packages:
    - Entity Framework
    - Miscrosoft SqlServer
- Finish off the test assignment and start testing.

## Testing

### Unittests

For unit tests, I used XUnit and tested functions separately. Some functions are meant to be private, so we cannot test that easily.

Usually, we just re-implement them as public in the testing directory (just like I did for one integration test)

### Integration tests

For the integration test, I used a Database connection and compared the game result with data in the database to ensure it is correct. 
I used the Async approach.

## Performance

For performance, I used the BenchmarkDotNet package. The test revealed that my conversion function is fast. However, I have minor issue with assembly stuff even though the code is running just fine. All tests I wrote passed. Time of testing: 06:00-10:00. 

