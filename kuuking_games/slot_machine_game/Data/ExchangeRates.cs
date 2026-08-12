using System.Runtime.CompilerServices;
using App.Machine.Types;

namespace App.Machine.Data {
    public class ExchangeRate {
        public Dictionary<Currency, decimal> ExchangeRates = new Dictionary<Currency, decimal>();

        public ExchangeRate()
        {
            ExchangeRates = LoadExchangeRates();
        }

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        Dictionary<Currency, decimal> LoadExchangeRates(){
            return new Dictionary<Currency, decimal>
            {
                { Currency.USD, 1.0m },
                { Currency.EUR, 0.85m },
                { Currency.GBP, 0.75m },
                { Currency.JPY, 110.0m },
                { Currency.AUD, 1.3m }
            };
        }
    }
}