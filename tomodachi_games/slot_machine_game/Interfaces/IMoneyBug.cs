using System.Runtime.CompilerServices;
using App.Machine.Types;

namespace App.Machine.Interfaces {
    public interface IMoneyBug {
        public Money Balance { get; set; }

        public void Deposit(decimal amount);

        public void Withdraw(decimal amount);
    }
}