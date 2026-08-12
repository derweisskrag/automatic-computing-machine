using System.Runtime.InteropServices;
using App.Machine.Entities;
using BrainLogic;
using BrainLogic.Services;
using App.Machine.Lib;
using App.Machine.Session;
using BenchmarkDotNet.Running;
using App.Machine.Performance;

namespace App.Machine{
    public class Machine {
        BrainLogic.Brain brain = new Brain(); 

        public readonly UserSession _userSession = new UserSession();

        private readonly SlotMachineService slotMachineService = new SlotMachineService();

        private User? user;

        private string[] GameOptions =>
            new string[] {
                "1 - Make One Spin",
                "2 - Make Ten Spins",
                "3 - Deposit Money", 
                "4 - Exit"
            };

        public static void Main(){
           // We set up the DB, so don't need to override 
           // machine?.brain?.DbService();
           // Set Up
           Machine machine = new Machine();
           machine.SetUp();

           // initialize the app
           // TEST: You are Alice (I assume logged user!)
           machine.CreateConsoleMachine();

           // Performance check
           //var summary = BenchmarkRunner.Run<ExchangeRatePerformanceTest>();
        }

        private void SetUp(){
            User Alice = brain.FindUser("Alice");
            if(Alice != null){
                user = Alice;
            }

            // Be confident: Alice is not null, right?
            _userSession.SignIn(Alice!);
        }

        private void CleanUp(){
            _userSession.SignOut();
            user = null;
        }

        private void CreateConsoleMachine(){
            Console.WriteLine($"Welcome to the Slot Machine, {(user != null ? user.Name : "Guest")}!");

            // Simulating Server
           while (true){
                foreach(var option in GameOptions){
                    Console.WriteLine(option);
                }

                // read the key
                string? UserAction = Console.ReadLine();

                if(UserAction == null){
                    Console.WriteLine("Invalid action!");
                    // skips to the new iteration
                    // so that Alice could choose again
                    continue;
                }

                // dispatch the action
                string DispatchedAction = DispatchUserAction(UserAction);

                if(DispatchedAction == "Exit")
                    break;
                else
                    continue;
           } 
        }

        private string DispatchUserAction(string UserAction){
            // here we can handle 
            // options
            // 1 - Bet 1 Spin
            // 2 - Bet 10 Spins
            // 3 - Deposit Money
            // 4 - Exit

            return UserAction switch {
                "1" => SpinOne(),
                "2" => SpinTen(),
                "3" => DepositMoney(),
                "4" => Exit(),
                _ => "Wrong Action!"
            };
        }

        private string SpinOne(){
            User user = _userSession.GetUserSession();
            Console.WriteLine($"\nUser {user.Name} is performing 1 Spin!");

            decimal.TryParse(Console.ReadLine(), out decimal Bet);

            slotMachineService.MakeSpin(user,  Bet);

            return "SpinOne";
        }

        private string SpinTen(){
            User user = _userSession.GetUserSession();
            Console.WriteLine($"\nUser {user.Name} is performing 10 Spins!");

            decimal.TryParse(Console.ReadLine(), out decimal Bet);

            slotMachineService.MakeTenSpins(user,  Bet);

            return "SpinTen";
        }


        private string DepositMoney(){
            User user = _userSession.GetUserSession();
            Console.WriteLine($"User {user.Name} is going to deposit money!");

            // update the balance
            try {
                decimal.TryParse(Console.ReadLine(), out decimal result);
                user.UpdateBalance(result);
                brain.UpdateUserBalance(user.Name, result);

                Console.WriteLine("Transaction completed!");

            } catch (Exception ex){
                Console.WriteLine("Could not deposite due to an error: ", ex);
            }

            return "Deposit";
        }

        private string Exit(){
            User user = _userSession.GetUserSession();
            Console.WriteLine($"User {user.Name} is ending the session");

            Dictionary<string, int> CollectedData = slotMachineService.CollectedSpinsData;
            decimal WinnedInTotal = slotMachineService.TotalWin;
            decimal BetInTotal = slotMachineService.TotalBet;

            // Final money in Alice / User
            decimal Profit = _userSession.StartMoney;

            // Draw
            ReportStatistics(BetInTotal, WinnedInTotal, CollectedData, Profit);

            try {
                CleanUp();
            } catch(Exception ex) {
                Console.WriteLine("Could not exit due to an error: ", ex);
            }

            return "Exit";
        }

        private void ReportStatistics(decimal TotalBet, decimal TotalWin, Dictionary<string, int> CollectedSpinsData, decimal Profit){
            Statistics statistics = new Statistics(TotalBet, TotalWin, CollectedSpinsData, Profit);
            statistics.UpdateRTP();
            statistics.Display();
        }
    }
}