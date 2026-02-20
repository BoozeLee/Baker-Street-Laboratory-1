-- Run in Supabase SQL Editor
CREATE TABLE IF NOT EXISTS subscriptions (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         text NOT NULL,
  stripe_sub_id   text,
  email           text,
  plan            text DEFAULT 'free',
  status          text DEFAULT 'active',
  created_at      timestamptz DEFAULT now()
);
CREATE INDEX ON subscriptions(user_id);
CREATE INDEX ON subscriptions(stripe_sub_id);

-- Row Level Security
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_own ON subscriptions
  FOR SELECT USING (auth.uid()::text = user_id);