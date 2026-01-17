-- Enable UUID support
create extension if not exists "uuid-ossp";

-- USERS TABLE
create table users (
    id uuid primary key default uuid_generate_v4(),
    username text unique not null,
    password_hash text not null,
    created_at timestamp with time zone default now()
);

-- ROOMS (optional but future-proof)
create table rooms (
    id uuid primary key default uuid_generate_v4(),
    code text unique not null,
    host_id uuid references users(id),
    password text,
    created_at timestamp with time zone default now()
);

-- PLAYER SESSIONS (reconnect support)
create table sessions (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references users(id) on delete cascade,
    room_code text,
    last_seen timestamp with time zone default now()
);

-- Indexes
create index idx_users_username on users(username);
create index idx_sessions_user on sessions(user_id);
