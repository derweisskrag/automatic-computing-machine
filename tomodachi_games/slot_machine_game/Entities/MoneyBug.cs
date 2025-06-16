using App.Machine.Interfaces;
using App.Machine.Types;
using App.Machine.Error;

namespace App.Machine.Entities {
    public class MoneyBug : IMoneyBug {
        public Money Balance { get; set; }

        public void Deposit(decimal amount) {

        }

        public void Withdraw(decimal amount){

        }

        public MoneyBug(decimal initialBalance = 0){
            if (initialBalance < 0)
                throw new ArgumentException("Balance cannot be negative.");

            Balance = new Money(initialBalance, Currency.USD);
        }

        public Result<decimal, System.Exception> UpdateBalance(decimal amount) {
            if(amount < 0 || amount == 0)
                return Result<decimal, System.Exception>.Error(new InsufficientFundsException("Amount cannot be negative."));

            Balance.Amount += amount;
            decimal UpdatedBalanceAmount = Balance.Amount;
            
            return Result<decimal, System.Exception>.Success(UpdatedBalanceAmount);
        }
    }
}