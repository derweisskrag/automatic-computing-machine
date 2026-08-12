using App.Machine.Interfaces;
using App.Machine.Types;

namespace App.Machine.Entities {
    public class User : IUser {
        public int UserID { get ; set; }

        public string Name { get; init; }

        // For User table
        public decimal Balance { get; set; }

        public ICollection<SpinResult> SpinResults { get; set; } = new List<SpinResult>();

        public ICollection<Bet> UserBets { get; set; } = new List<Bet>();

        // I could simplify to just Money
        private readonly MoneyBug _moneyBug = new MoneyBug();

        public ICollection<Combination>? Combinations { get; set; } // Relationship

        public User(string name){
            Name = name;
        }
 
        public void SayHello(){
            Console.WriteLine($"I am {Name}");
        }

        public void DisplayInfo() => 
            Console.WriteLine($"User: {Name}, Balance: {_moneyBug.Balance.Amount}");

        public void UpdateBalance(decimal amount){
            Result<decimal, System.Exception> result = _moneyBug.UpdateBalance(amount);
        }

        public Currency GetCurrency(){
            return _moneyBug.Balance.Currency;
        }

        public void ChangeCurrency(Currency currency){
            _moneyBug.Balance.ChangeToCurrency(currency);
        }

        public decimal GetBalance(){
            return _moneyBug.Balance.Amount;
        }
    }
}