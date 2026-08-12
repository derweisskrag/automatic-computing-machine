using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using Microsoft;

using App.Machine.Entities;

namespace BrainLogic.Models;

public class LocalUserContext : DbContext
{
    public DbSet<User>? Users { get; set; }
    public DbSet<Combination>? Combinations { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder options){
        string relativePath = "../../../../Database/SlotMachine.db";
        string localPath = "./Database/SlotMachine.db";

        string dbPath = File.Exists(relativePath) ? relativePath : localPath;

        options.UseSqlite($"Data Source={dbPath}");
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder){
        modelBuilder.Entity<User>().ToTable("Users");
        modelBuilder.Entity<Combination>().ToTable("Combinations");
    }
    
}

