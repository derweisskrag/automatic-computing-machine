namespace App.Machine.Error {
    public class UserSessionEmpty : System.Exception {
        public UserSessionEmpty(string message) : base(message) {}
    }
}