using BrainLogic.Services;
using BrainLogic.Models;

using App.Machine.Entities;
using Microsoft.EntityFrameworkCore.Infrastructure;
using System.Security.Cryptography.X509Certificates;

namespace BrainLogic {
    public class Brain { 
        public Dictionary<Combination, decimal> MemoizedCombinations = new Dictionary<Combination, decimal>(); 

        private readonly Lazy<Dictionary<Combination, decimal>> _lazyCombinations;

        public Dictionary<Combination, decimal> CachedCombinations => _lazyCombinations.Value;

        public Brain()
        {
            // Initialize Lazy to fetch from DB on first access
            _lazyCombinations = new Lazy<Dictionary<Combination, decimal>>(FetchAllCombinations);
        }

        public void DbService(){
            using (var db = new LocalUserContext()){
                // Console.WriteLine("Inserting new user");
                // db.Add(new User("Alice"));
                // db.SaveChanges();
                
                // Console.WriteLine("Inserting new combination");
                // db.Add(new Combination("Wild", 100.0m));
                // db.SaveChanges();

                // Update the alice money
                // if(db.Users == null)
                //     return;

                // var user = db.Users.FirstOrDefault(u => u.Name == "Alice");


                // if (user != null)
                // {
                //     // Step 2: Update the balance
                //     user.Balance = 1000.0m;

                //     // Step 3: Mark the entity as updated
                //     db.Users.Update(user);

                //     // Step 4: Save changes to the database
                //     db.SaveChanges();

                //     Console.WriteLine($"Updated {user.Name}'s balance to {user.Balance}.");
                // }
                // else
                // {
                //     Console.WriteLine($"User '{user?.Name}' not found.");
                // }
            }
        }

        public Dictionary<Combination, decimal> FetchAllCombinations(){
            using(var db = new LocalUserContext()){
                if(db.Combinations == null) throw new NullReferenceException("Combinations are not present in the database!");

                var results = db.Combinations
                    .Select(Combination => new { Combination.CombinationName, Combination.Value })
                    .ToList();

                
                var combinationsDict = new Dictionary<Combination, decimal>();

                foreach (var item in results)
                {
                    var key = new Combination { CombinationName = item.CombinationName, Value = item.Value } ;
                    combinationsDict[key] = item.Value;
                }

                return combinationsDict;
            }
        }

        


        public User FindUser(string Name){
            using(var db = new LocalUserContext()){
                if(db.Users == null)
                    throw new Exception("Database table 'Users' does NOT exist!");
                
                var user = db.Users.FirstOrDefault(u => u.Name == Name);

                if(user == null){
                    // Throw exc
                    Console.WriteLine($"User name {Name} was not found!");
                }

                return user!;
            }
        }

        public void UpdateUserHistory(string Name, decimal BetAmount, (string, string, string) SpinRow, int Result){
            var (first, second, third) = SpinRow;
            using(var db = new LocalUserContext()){
                if(db.Users != null){
                    User user = FindUser(Name);
                    // run the update history
                    user.SpinResults.Add( new SpinResult { SpinRow = $"{first} | {second} | {third}", Result = Result });

                    // update the user bet
                    user.UserBets.Add( new Bet { Amount = BetAmount });
                    
                    // update the user
                    UpdateUser(user, db);
                }
            }
        }

        public void UpdateUserBalance(string Name, decimal Amount){
            using(var db = new LocalUserContext()){
                if(db.Users != null){
                    var user = FindUser(Name);

                    // update the balance
                    user.Balance += Amount;

                    // update the user
                    UpdateUser(user, db);
                }
            }
        }

        private void UpdateUser(User user, LocalUserContext db){
            if(db.Users != null){
                db.Users.Update(user);
                db.SaveChanges();
            }
        }
    }
}