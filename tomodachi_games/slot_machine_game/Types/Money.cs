using App.Machine.Data;
using App.Machine.Utils;

namespace App.Machine.Types {
    public class Money {
        public decimal Amount { get; set; } = 0.0m;
        public Currency Currency { get; set; } = Currency.USD;

        private static readonly Dictionary<Currency, decimal> ExchangeRates = new ExchangeRate().ExchangeRates;
        private Utilities _utilities = new Utilities();

        public Money(decimal amount, Currency currency){
            Amount = amount;
            Currency = currency;
        }

        public void ChangeToCurrency(Currency ToCurrency){
            if (Currency == ToCurrency) return;

            decimal TargetRate = ExchangeRates.GetValueOrDefault(ToCurrency);
            decimal CurrentRate = ExchangeRates.GetValueOrDefault(Currency);

            // convert
            // TODO: Refactor into utils
            Amount = _utilities.ConvertTo(Amount, CurrentRate, TargetRate);
            Currency = ToCurrency;
        }

        public void ChangeToCurrencyRustImpl(Currency ToCurrency){
            if (Currency == ToCurrency) return;

            decimal TargetRate = ExchangeRates.GetValueOrDefault(ToCurrency);
            decimal CurrentRate = ExchangeRates.GetValueOrDefault(Currency);

            // convert
            // TODO: Refactor into utils
            Amount = _utilities.ConvertToRustImpl(Amount, CurrentRate, TargetRate);
            Currency = ToCurrency;
        }

        public static Money ChangeToCurrency(decimal Amount, Currency FromCurrency, Currency ToCurrency){
            if (FromCurrency == ToCurrency) return new Money(Amount, FromCurrency);

            decimal FromRate = Money.ExchangeRates.GetValueOrDefault(FromCurrency);
            decimal ToRate = Money.ExchangeRates.GetValueOrDefault(ToCurrency);

            // TODO: Check how efficient it is
            Utilities utilities = new Utilities();
            decimal ConvertedAmount = utilities.ConvertTo(Amount, FromRate, ToRate);
            return new Money(ConvertedAmount, ToCurrency);
        }

        public override string ToString() => $"{Amount} {Currency}";
    }
}