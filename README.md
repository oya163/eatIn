testing

0. install the necessary python packages

1. generate db with ./scripts/build_db_fixed.sql
2. populate countries with ./scripts/insert_countries.sql
3. populate users + chefs with ./scripts/insert_chefs.sql
4. populate customers with ./scripts/insert_customers.sql
5. populate fooditems with ./scripts/insert_meals.sql
6. populate cuisines with ./scripts/insert_cuisines.sql

if changes to the build_db_fixed.sql script were made, it means the schema was
changed and you should delete the db and build a new one and populate
everything again with the above steps.


Data sources:  
chefs: https://www.chefdb.com/nm/atoz/  
meals: http://www.foodnetwork.com/recipes/a-z/  
countries: 


Packages needed:  
python 2.7  
flask  
flask-sqlalchemy  
wtforms  
passlib  
