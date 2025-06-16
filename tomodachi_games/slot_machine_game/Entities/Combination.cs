namespace App.Machine.Entities;

public class Combination {
    public int CombinationID { get; set; }

    public required string CombinationName { get; set; }

    public decimal Value { get; set; }

    public Combination() { }

    public Combination(string CombName){
        CombinationName = CombName;
    }

    public Combination(string CombName, decimal Val){
        CombinationName = CombName;
        Value = Val;
    }


    public override int GetHashCode()
    {
        return CombinationName.GetHashCode();
    }
}