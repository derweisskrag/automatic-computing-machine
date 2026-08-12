-- Add migration script here
-- Create the tokens table
CREATE TABLE tokens (
    id SERIAL PRIMARY KEY,
    access_token TEXT NOT NULL,
    refresh_token TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

ALTER TABLE tokens ADD CONSTRAINT unique_user_token UNIQUE(user_id);
