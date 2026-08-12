namespace App.Machine.Error {
    public class InsufficientFundsException : System.Exception {
        public InsufficientFundsException(string message) : base(message) {}
    }
}