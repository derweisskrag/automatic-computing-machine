using App.Machine.Error;
using App.Machine.Lib;
using App.Machine.Types;
using Microsoft.EntityFrameworkCore.Storage;

namespace App.Machine.Utils {
    public class Utilities {
        private readonly RustUtils rustUtils = new();

        public decimal ConvertTo(decimal Amount, decimal FromRate, decimal ToRate){
            // Check if valid data are passed to the function
            // Rename & Refactor
            // User the OOP
            if(Amount < 0 || FromRate < 0 || ToRate < 0) throw new InsufficientFundsException("Cannot convert from negative");

            return Amount * (ToRate / FromRate);
        }

        public decimal ConvertToRustImpl(decimal Amount, decimal ToRate, decimal FromRate){
            return (decimal) RustUtils.calculate_new_currency(Amount, ToRate, FromRate);
        }
    }
}