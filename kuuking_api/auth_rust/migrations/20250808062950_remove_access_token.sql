-- Add migration script here
-- Removal of Access Token Column
ALTER TABLE tokens DROP COLUMN access_token;
