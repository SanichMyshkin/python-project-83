CREATE TABLE IF NOT EXISTS urls (
  id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name varchar(255) UNIQUE,
  created_at timestamp NOT NULL
);