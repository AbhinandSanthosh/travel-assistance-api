-- Phase 4.3: least-privilege database role for the running application.
--
-- Run this ONCE, connected as your existing superuser/owner role
-- (the one currently in DATABASE_URL, e.g. `postgres`), against the
-- travel_assistance_api database. After it's run, update .env:
--
--   DATABASE_URL           -> the new travel_assistance_app role below
--                              (used by the running FastAPI app)
--   MIGRATION_DATABASE_URL -> your EXISTING elevated connection string
--                              (used only by `alembic upgrade`)
--
-- Why two roles: the app only ever needs to read/write rows in
-- existing tables. It never needs to CREATE TABLE, ALTER TABLE, DROP
-- TABLE, or create other roles -- those happen exactly once per
-- deploy, via a human/CI running `alembic upgrade head` under the
-- elevated role. Every other minute of every day, the app should be
-- running as a role that literally cannot execute DDL, so that a SQL
-- injection bug, a compromised dependency, or a leaked DATABASE_URL
-- can do damage to DATA at worst -- not schema, not other databases,
-- not create a new superuser for itself.

-- 1. Create the role. CHANGE THIS PASSWORD before running -- this is
--    a placeholder, not a value to actually deploy with.
CREATE ROLE travel_assistance_app
    WITH LOGIN
    PASSWORD 'CHANGE_ME_BEFORE_RUNNING'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOREPLICATION
    NOBYPASSRLS;

-- 2. Allow it to connect to this database and use the public schema.
GRANT CONNECT ON DATABASE travel_assistance_api TO travel_assistance_app;
GRANT USAGE ON SCHEMA public TO travel_assistance_app;

-- 3. DML only on existing tables -- no CREATE/ALTER/DROP/TRUNCATE.
GRANT SELECT, INSERT, UPDATE, DELETE
    ON ALL TABLES IN SCHEMA public
    TO travel_assistance_app;

-- 4. Sequences (needed for SERIAL/IDENTITY primary keys on INSERT).
GRANT USAGE, SELECT
    ON ALL SEQUENCES IN SCHEMA public
    TO travel_assistance_app;

-- 5. Make step 3/4 apply automatically to tables created by FUTURE
--    migrations too, so this script doesn't need re-running after
--    every `alembic upgrade`. Replace `postgres` below if your
--    elevated/migration role has a different name.
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO travel_assistance_app;

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
    GRANT USAGE, SELECT ON SEQUENCES TO travel_assistance_app;

-- 6. Harden the schema itself: by default PUBLIC (i.e. every role)
--    can CREATE objects in the public schema on some Postgres
--    versions/configurations. Revoke that so only the elevated role
--    can create new tables at all.
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

-- Verification (run as travel_assistance_app after switching
-- DATABASE_URL, to confirm DDL is actually blocked):
--   CREATE TABLE should_fail (id serial);
--   -- expected: ERROR: permission denied for schema public
