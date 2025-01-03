# Final Project
## Project Description
This application serves as a functioning e-commerace website. Users can register as a buyer or seller. Customers can browse the website, add items to their cart, and review items they've purchased. Sellers can create new products, update their existing products, and fulfill orders from customers. 

# Project Specifications
- Tables
 . Cart_Items
 . Categories
 . Customers
 . Items
 . Order_Items
 . Orders
 . Reviews
 . Sellers
 . Users
- Full CRUD functionality for items 
- Regex, yup, and formik for validation
- react-dropzone for product image uploads
- Flask and SQLite/Postgres backend

## Installation
- Clone this project repository
- Flask App(Backend): <br>
 . $ pipenv install && pipenv shell<br>
 . $ cd server<br>
 . $ flask db upgrade<br>
 . $ python seed.py<br>
 . $ python app.py<br>
- React(Frontend): <br>
 . $ npm install --prefix client<br>
 . $ npm run start --prefix client<br>


