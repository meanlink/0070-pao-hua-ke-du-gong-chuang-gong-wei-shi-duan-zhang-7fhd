CREATE TABLE IF NOT EXISTS machines (
    key text PRIMARY KEY, title text NOT NULL, bay text NOT NULL
);
CREATE TABLE IF NOT EXISTS bench_sessions (
    code text PRIMARY KEY, machine text NOT NULL REFERENCES machines(key),
    crew text NOT NULL, service_day date NOT NULL,
    open_minute integer NOT NULL CHECK (open_minute >= 0),
    end_minute integer NOT NULL CHECK (end_minute > open_minute AND end_minute <= 1440),
    decision text NOT NULL DEFAULT 'logged' CHECK(decision IN ('logged','counted','void')),
    checked_by text REFERENCES app_users(email), CHECK ((decision='logged')=(checked_by IS NULL))
);
CREATE TABLE IF NOT EXISTS maintenance_blocks (
    code text PRIMARY KEY, machine text NOT NULL REFERENCES machines(key),
    service_day date NOT NULL, reason text NOT NULL,
    open_minute integer NOT NULL CHECK (open_minute >= 0),
    end_minute integer NOT NULL CHECK (end_minute > open_minute AND end_minute <= 1440)
);
CREATE TABLE IF NOT EXISTS shop_hours (
    machine text NOT NULL REFERENCES machines(key),service_day date NOT NULL,
    lo int NOT NULL CHECK(lo>=0),hi int NOT NULL CHECK(hi>lo AND hi<=1440),
    PRIMARY KEY(machine, service_day)
);
CREATE TABLE IF NOT EXISTS utilization_bulletins (
    service_day date PRIMARY KEY, issued_by text NOT NULL REFERENCES app_users(email),
    report jsonb NOT NULL, job_id bigint REFERENCES app_jobs(id)
);
