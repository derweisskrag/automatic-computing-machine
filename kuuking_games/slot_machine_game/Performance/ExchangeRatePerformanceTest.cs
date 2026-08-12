using App.Machine.Types;
namespace App.Machine.Performance;
using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;

[MemoryDiagnoser] // Adds memory diagnostics to the benchmark report
public class ExchangeRatePerformanceTest
{
    private Money _money = new Money(0.0m, Currency.USD); // default value

    [GlobalSetup]
    public void Setup()
    {
        _money = new Money(100000.0m, Currency.USD);
    }

    [Benchmark]
    public void ExchangeRateTest()
    {
        _money.ChangeToCurrency(Currency.JPY);
    }
}