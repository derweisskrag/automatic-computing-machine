namespace App.Machine.Entities;

public class SpinResult {
    public int SpinResultId { get; set; }

    public required string SpinRow { get; set; }

    // 1 - Win, 0 - Loss
    public int Result { get; set; }

    public SpinResult() {}

    public SpinResult((string, string, string) Row, int Outcome){
        var (first, second, third) = Row;
        SpinRow = $"{first} | {second} | {third}";
        Result = Outcome;
    }
}