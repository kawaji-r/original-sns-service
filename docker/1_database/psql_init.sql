CREATE DATABASE sns_dbname;
CREATE USER sns_user WITH PASSWORD 'nH9Us5zw';
ALTER ROLE sns_user SET client_encoding TO 'utf8';
ALTER ROLE sns_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE sns_user SET timezone TO 'Asia/Tokyo';
GRANT ALL PRIVILEGES ON DATABASE sns_dbname TO sns_user;
