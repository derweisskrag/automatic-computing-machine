using System.Reflection;
using App.Machine.Entities;
using App.Machine.Error;
using App.Machine.Lib;
using App.Machine.Types;
using Microsoft.EntityFrameworkCore.Internal;

namespace BrainLogic.Services;

public class SlotMachineService {
    private readonly Random random = new Random();

    // The naming is misleading
    // TODO: New name (Objective: Contains DbService)
    private readonly Brain brain = new Brain();

    private Lazy<Dictionary<Combination, decimal>> _combinations 
        => new Lazy<Dictionary<Combination, decimal>>(brain.FetchAllCombinations());

    private Dictionary<Combination, decimal> Combinations => _combinations.Value;

    private readonly RustUtils rustUtils = new RustUtils();

    public Dictionary<string, int> CollectedSpinsData = new Dictionary<string, int>
        {
            { "777", 0 },
            { "Cherry", 0 },
            { "Wild", 0}, 
            { "Bar", 0}
        };

    public decimal TotalBet = 0;

    public decimal TotalWin = 0;

    public (string, string, string) GenerateCombination(){
        return (CreateCombination(), CreateCombination(), CreateCombination());
    }

    private string CreateCombination(){
        var randomKey = _combinations.Value.Keys.ElementAt(random.Next(Combinations.Count));
        return randomKey.CombinationName;
    }

    public bool CheckResultRustImpl(string x, string y, string z){
        // bad
        // use only for performance tests (can refine function using match statement)
        return RustUtils.check_result(x, y, z);
    }

    public void MakeSpin(User user, decimal Bet){
        if(!HasBalance(user, Bet)){
            throw new InsufficientFundsException("\nCannot bet, because no money!");
        }

        // update the total Bet
        TotalBet += Bet;



        // Generate the slots
        (string, string, string) SpinResult = GenerateCombination();

        // Draw it to Console
        DrawSpinResult(SpinResult);

        // Apply changes (win/loss)
        // Consider handle errors here
        ApplyResult(SpinResult, user, Bet);
    }

    public void MakeTenSpins(User user, decimal Bet){
        // I am confused
        // My first attempt
        // Also must handle all errors
        for(int i = 1; i < 11; i++){
            MakeSpin(user, Bet);
        }
    }


    private void ApplyResult((string, string, string) SpinResult, User user, decimal Bet){

        // Dispatch the combo
        string WinningCombo = DispatchSpinRow(SpinResult);

        // Fetch prices
        // Remember it is lazy! We do not do same queries

        var result = _combinations
                .Value.Where(key => key.Key.CombinationName == WinningCombo)
                .Select(key => key.Key.Value)
                .DefaultIfEmpty(1.0m)
                .Last();
        
        if(WinningCombo == "Lose"){
            // User lost the bet
            Console.WriteLine($"\n{user.Name} lost the bet! Processing the balance...");
            
            // update the user balance accordingly 
            // I update the session User and DB one (I believe that I should only update)
            // DB user and update User on client when needed (service -> back-end)
            // For this task, I just update both for now

            // Lost, so UserSession one changes:
            user.Balance -= Bet;

            // Log how much lost
            Console.WriteLine($"\nUser {user.Name} lost {Bet} | Current Balance: {user.Balance}");

            // ACTION: Deduct the bet
            user.UpdateBalance(-Bet);

            // update the DB
            brain.UpdateUserBalance(user.Name, -Bet);

            // update total win
            TotalWin -= Bet;

            

            // load history
            brain.UpdateUserHistory(user.Name, Bet, SpinResult, 0);
        } else {
            Console.WriteLine($"\n{user.Name} won the bet! Processing the balance..."); 

            // determine the winning money
            decimal PayOut = DeterminePayout(Bet, result);

            // update total win
            TotalWin += PayOut;

            // try to mutate balance (user session one)
            user.Balance += PayOut;
            
            // update both client & server states
            user.UpdateBalance(PayOut);

            // update the user in DB
            brain.UpdateUserBalance(user.Name, PayOut);

            // load history
            brain.UpdateUserHistory(user.Name, Bet, SpinResult, 1);

            // Log how much lost
            Console.WriteLine($"\nUser {user.Name} won {Bet} | Current Balance: {user.Balance}");

            // Collect hits
            if (CollectedSpinsData.TryGetValue(WinningCombo, out int currentValue))
            {
                CollectedSpinsData[WinningCombo] = currentValue + 1;
            }
            else
            {
                CollectedSpinsData[WinningCombo] = 0;
            }
        }
    }

    private bool HasBalance(User user, decimal Bet){
        return user.Balance >= Bet;
    }

    private string DispatchSpinRow((string, string, string) Row) {
        return Row switch {
            ("777", "777", "Wild") or ("777", "Wild", "777") or ("Wild", "777", "777") or ("777", "777", "777") => "777",
            ("Cherry", "Cherry", "Wild") or ("Cherry", "Wild", "Cherry") or ("Wild", "Cherry", "Cherry") or ("Cherry", "Cherry", "Cherry") => "Cherry",
            ("Bar", "Bar", "Wild") or ("Bar", "Wild", "Bar") or ("Wild", "Bar", "Bar") or ("Bar", "Bar", "Bar") => "Bar",
            ("Wild", "Wild", "Wild") => "Wild",
            _ => "Lose"
        };
    }

    private void DrawSpinResult((string, string, string) SpinResult) {
        Console.WriteLine("\n-------------------------------");
        Console.WriteLine($"| {SpinResult.Item1 } | { SpinResult.Item2 } | { SpinResult.Item3 } |");
        Console.WriteLine("-------------------------------");
    }

    private decimal DeterminePayout(decimal Bet, decimal WinningComboValue){
        return Bet * WinningComboValue;
    }
}