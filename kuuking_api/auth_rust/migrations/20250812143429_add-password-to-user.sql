-- Add migration script here
-- Adding password to the user table
ALTER TABLE users 
ADD COLUMN password_hash TEXT NOT NULL;
