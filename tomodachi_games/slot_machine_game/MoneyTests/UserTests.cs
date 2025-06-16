using Xunit;
using App.Machine.Types;
using App.Machine.Entities;
using App.Machine.Session;
using App.Machine.Error;
using BrainLogic;
using Microsoft.Data.Sqlite;
using System.Data.Common;
using System.Transactions;

public class UserTests {
    [Fact]
    public void UserCreation(){
        User Alice = new User("Alice");

        // bacis testing here
        Assert.Equal("Alice", Alice.Name);
        Assert.Equal(0.0m, Alice.GetBalance());

        // Let us deposit some money
        // NB! Usually, we have a service for that
        // But for simplicity: just update balance manually
        Alice.UpdateBalance(100.0m);

        // Verify the result
        Assert.Equal(100.0m, Alice.GetBalance());

        // Meanwhile
        Assert.Equal(0.0m, Alice.Balance);

        /*

        Reasoning: User.Balance is for Entity Framework. It is For schema.
        To update Alice's Balance in DB, we have to make sure she exists 
        in the database at all. After, we can call the update function on the
        database context (ContextManager for DB - Python)

        - Explanation: In Python, Context Managers are used like

        >>> with dbm.open("mydb", "r") as db: ...

        It manages the resources and cleans up them:

        - Try Open
        - Catch Exception
        - Finally (close connection) 

        In C#, we also leverage this idea, and in addition, just like Python or C++, 
        we have MUTEX & Sepamorphs. 

        Conlusion: User Balance is commiting the change of the SQLite's stored user, rather the
        client side.

        Example: when rendering the Alice' current balance, we did NOT fetch her Balance from 
        Database. Instead, we used simple client-side function to mutate her "fetched" balance in
        between the transactions, as in

        user.Balance += Bet
        user.Balance -= Bet

        and then we could Console.WriteLine("{}'s Balance is {}", user.Name, user.Balance);

        */
    }

    [Fact]
    public void UserSessionTest(){
        // create User Session and check if no user is signed
        UserSession userSession = new UserSession();
        
        // Check no user is signed in
        AssertUserSessionEmpty(userSession);

        // create test used named Jake and Sign them In
        User Jake = new User("Jake");
        userSession.SignIn(Jake);

        // Make sure that UserSession has user now: it is not null anymore
        Assert.NotNull(userSession.GetUserSession());

        // Let us log out
        userSession.SignOut();

        // check no user is there now
        AssertUserSessionEmpty(userSession);
    }

    [Fact]
    public async Task IntegrationUserTest(){
        // Connect to DB 
        await using var db = new SqliteConnection("Data Source=../../../../Database/SlotMachine.db;Mode=ReadOnly");
        await db.OpenAsync();

        var transaction = await db.BeginTransactionAsync();
        await using (transaction) 
                {
                    var command = db.CreateCommand();
                    command.Transaction = (SqliteTransaction)transaction;
                    command.CommandText = "SELECT Name FROM Users WHERE UserID = 1";
                    var result = await command.ExecuteScalarAsync();
                    var userName = result?.ToString();
                    Assert.Equal("Alice", userName);
                }
    }
    private void AssertUserSessionEmpty(UserSession userSession)
    {
        var exception = Assert.Throws<UserSessionEmpty>(() => userSession.GetUserSession());
        Assert.Equal("No user is logged!", exception.Message);
    }
}