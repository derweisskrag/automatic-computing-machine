using System.Text;
using App.Machine.Entities;
using App.Machine.Error;
using BrainLogic;

namespace App.Machine.Session {
    public class UserSession {
        private User? _user;

        public decimal StartMoney => _user != null ? _user.Balance : 0;

        public void SignIn(User user)
        {
            _user = user;
        }

        public void SignOut()
        {
            _user = null;
        }

        public User GetUserSession(){
            if(_user != null)
                return _user;
            
            throw new UserSessionEmpty("No user is logged!");
        }
    }
}