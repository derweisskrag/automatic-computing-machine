using System.Globalization;
using App.Machine.Entities;
using BrainLogic.Services;
using Microsoft.Data.Sqlite;
using Xunit;
using Xunit.Sdk;

public class GameLogicTest{
    [Fact]
    public async Task SlotMachineResultTest(){
        // initialize the service
        SlotMachineService slotMachineService = new SlotMachineService();

        // define the path to db
        string DbPath = "Data Source=../../../../Database/SlotMachine.db;Mode=ReadOnly";

        // create user
        User Alice = new User("Alice");
        Alice.Balance += 1000.0m;

        // Play the game
        if (slotMachineService != null){
            // Perform Action of the machine
            slotMachineService.MakeSpin(Alice, 250.0m);

            // The action updates the Database
            // Let us fetch the spin result
            var (spinResult, SpinResult, user) = await GetLastRowFromDb(DbPath);

            if(spinResult != null && user != null){
                string result = DispatchSpinRow(spinResult);
                if(result == "Lose"){
                    // Test if the lost case
                    Assert.Equal("0", SpinResult);
                } else {
                    Assert.Equal("1", SpinResult);
                }

                Assert.Equal("Alice", user.Name);
            }
        }

        
    }

    private async Task<(string? SpinRow, string? Result, User? User)> GetLastRowFromDb(string path)
    {
        await using var db = new SqliteConnection(path);
        await db.OpenAsync();

        var command = db.CreateCommand();
        command.CommandText = @"
            SELECT 
                sr.SpinRow,
                sr.Result,
                u.UserID, 
                u.Name, 
                u.Balance 
            FROM 
                SpinResult sr
            INNER JOIN 
                Users u ON sr.UserID = u.UserID
            WHERE 
                sr.UserID = 1 
            ORDER BY 
                sr.SpinResultID DESC 
            LIMIT 1;
        ";

        await using var reader = await command.ExecuteReaderAsync();

        if(!await reader.ReadAsync())
            return (null, null, null);

        var spinRow = reader["SpinRow"]?.ToString();
        var result = reader["Result"]?.ToString();

        // NB! Different InvariantCulture: '10,0` or `10.0` - difference is clear.

        var user = new User(reader["Name"].ToString()!) {
            UserID = Convert.ToInt32(reader["UserID"]),
            Balance = Convert.ToDecimal(reader["Balance"].ToString(), CultureInfo.InvariantCulture)
        };

        return (spinRow, result, user);
    }


        // grab this function
    private string DispatchSpinRow(string Row) {
        return Row switch {
            "777 | 777 | Wild" or "777 | Wild | 777" or "Wild | 777 | 777" => "777",
            "Cherry | Cherry | Wild" or "Cherry | Wild | Cherry" or "Wild | Cherry | Cherry" => "Cherry",
            "Bar | Bar | Wild" or "Bar | Wild | Bar" or "Wild | Bar | Bar" => "Bar",
            "Wild | Wild | Wild" => "Wild",
            _ => "Lose"
        };
    }
}