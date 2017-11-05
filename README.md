testing

0. install the necessary python packages

1. generate db with ./scripts/build_db_fixed.sql
2. populate countries with ./scripts/insert_countries.sql
3. populate users + chefs with ./scripts/insert_chefs.sql
4. populate customers with ./scripts/insert_ccustomers.sql

if changes to the build_db_fixed.sql script were made, it means the schema was
changed and you should delete the db and build a new one and populate
everything again with the above steps.
