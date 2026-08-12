using System.ComponentModel.DataAnnotations;
using SQLitePCL;

namespace App.Machine.Entities;

public class Statistics {
    public decimal TotalBet { get; set; }

    public decimal TotalWin { get; set; }

    public Dictionary<string, int> SpinsData { get; set;}

    public decimal RTP { get; set; }

    public decimal Profit { get; set; }

    public Statistics(decimal BetsInTotal, decimal WinnedMoneyAmount, Dictionary<string, int> CollectedSpinsData, decimal ProfitMoney){
        TotalBet = BetsInTotal;
        TotalWin = WinnedMoneyAmount;
        SpinsData = CollectedSpinsData;
        Profit = ProfitMoney;
    }

    public void UpdateRTP(){
        if(TotalWin == 0)
            Console.WriteLine("Cannot determine 'RTP' due to not collected data during the session!");
        else{   
            decimal NewRTP = Math.Round((TotalWin / TotalBet) * 100.0m, 2);
            RTP = NewRTP;
        }
    }

    public void Display(){
        string sessionSummary = $"\nConclusion of your session:" +
                        $"\n\t- Total Bet: {TotalBet}," +
                        $"\n\t- Total Win: {TotalWin}," +
                        $"\n\t- RTP: {RTP}" + 
                        $"\n\t - Current Balance: {Profit}";

        string collectedData = $"\n\nCollected Data:" +
                            $"\n\t- '777' was hit {SpinsData.GetValueOrDefault("777", 0)} times," +
                            $"\n\t- 'Cherry' was hit {SpinsData.GetValueOrDefault("Cherry", 0)} times," +
                            $"\n\t- 'Bar' was hit {SpinsData.GetValueOrDefault("Bar", 0)} times," +
                            $"\n\t- 'Wild' was hit {SpinsData.GetValueOrDefault("Wild", 0)} times.";

        string sessionEnd = "\n\nThus, you ended your session!";

        // Combine everything for the final output
        Console.WriteLine(sessionSummary + collectedData + sessionEnd);
    }
}