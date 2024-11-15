DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = 'customer-db'
   ) THEN
      PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE "customer-db"');
   END IF;
END
$do$;


CREATE TABLE IF NOT EXISTS channel(
   id UUID PRIMARY KEY,
   name VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS plan(
   id UUID PRIMARY KEY,
   name VARCHAR(20),
   basic_monthly_rate NUMERIC(10, 2),
   issue_fee NUMERIC(10, 2)
);

CREATE TABLE IF NOT EXISTS customer (
    id UUID PRIMARY KEY,
    document VARCHAR(20),
    name VARCHAR(150),
    plan_id UUID,
    date_suscription TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_plan
        FOREIGN KEY (plan_id) 
        REFERENCES plan (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS channel_plan (
    id UUID PRIMARY KEY,
    channel_id UUID,
    plan_id UUID,
    CONSTRAINT fk_plan
        FOREIGN KEY (plan_id) 
        REFERENCES plan (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_channel
      FOREIGN KEY (channel_id) 
      REFERENCES channel (id)
      ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS customer_database (
    id UUID PRIMARY KEY,
    customer_id UUID,
    topic TEXT,
    content TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id) 
        REFERENCES customer (id)
        ON DELETE CASCADE
);