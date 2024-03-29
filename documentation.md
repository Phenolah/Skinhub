SKINHUB PROJECT DOCUMENTATION

a. Prerequisities

Before you begin, ensure you have met the following requirements:
- Python 3.x installed locally
- Virtual environment <code> (venv) or (pipenv) </code> for managing dependancies.
- Basic Understanding of Python and Django Rest Framework

b. Installation
Setting up on Local Machine

- Clone the repository
<code> 
git clone (repository_url)

 cd <repository_directory)
</code>

- Create a Virtual Environment

<code> 
Python3 -m venv venv
</code> 

c. Activate the Virtual Environment
<code>

    Linux: source venv/bin/activate   
    
    Windows: venv\Scripts\activate
 </code>

d. Install Project Dependancies

<code> 
pip install -r requirements.txt 
</code>

e. Start the Django Server

<code>
python  manage.py runserver 
</code>

API will run on local host 

#API ENDPOINTS

1. Home

Home Page 

Endpoint: <code>
http://127.0.0.1:8000 
</code>

Method: GET

Description: This is the Home page with an overview about the ecommerce product.


2. Blog

Blog Page

Endpoint: <code> 
http://127.0.0.1:8000/blog 
</code>

Method: GET

Description: The blog page contains different blog post descriptions

3. log detail

Blog Article Page

Endpoint <code> 
http://127.0.0.1:8000/blogdetail/<slug:slug>/ 
</code>

Method: GET

Description: Blog detail page contains the Articles  of the Blog posts.

<code> 
  curl -X GET http://127.0.0.1:8000/blogdetail/slug-value/

</code>

4. Shop

Products Page

Endpoint: <code> 
http://127.0.0.1:8000/shop
</code>

Method: GET

Description: The shop page contains various skincare products on sale.

5. Shop Details

Products details Page

Endpoint: <code> 
http://127.0.0.1:8000/details/<slug>/ 
</code>

Method: GET

Description: The products details contains details of the products such as Description, Price, Add to Cart, Remove from cart and choose size

<code> 

  curl -X GET http://127.0.0.1:8000/details/slug-value/

</code>

6. About Details

About Page

Endpoint: <code> 
http://127.0.0.1:8000/about 
</code>

Method: GET

Description: The About page 

<code> 

  curl -X GET http://127.0.0.1:8000/about

</code>

7. Add to Cart

Add to Cart Functionality

Method: GET

Endpoint: <code> 
https://127.0.0.1:8000/add-to-cart/<slug>/ 
</code>

Description: Adds item to cart

<code> 

  curl -X GET http://127.0.0.1:8000/add-to-cart/slug-value

</code>

8. Remove from Cart

Remove from Cart Functionality

Method: DELETE

Endpoint: <code> 
https://127.0.0.1:8000/remove-from-cart/<slug>/ 
</code>

Description: Deletes items from cart

<code> 

  curl -X GET http://127.0.0.1:8000/remove-from-cart/slug-value

</code>

9. Removes a Single item from Cart

Removes a single item from Cart Functionality

Method: DELETE

Endpoint: <code> 
https://127.0.0.1:8000/remove-single-item-from-cart/<slug>/ 
</code>

Description: Deletes a single item the  from cart

<code> 
  curl -X GET http://127.0.0.1:8000/remove-single-item-from-cart/slug-value

</code>

10. Accounts/Registration Page

Registration Page

Method: POST

Endpoint: <code> 
https://127.0.0.1:8000/accounts 
</code>

Description: Users can be able to register an account to be able to Shop

- Parameters
Username:<code> STR </code>
Email: <code> STR </code>
Password1: <code> STR </code>
Password2: <code> STR </code>

<code>  CURL -X POST https://127.0.0.1:8000/accounts  </code>

11. Login Page

Login Page

Method: POST

Endpoint: <code>
https://127.0.0.1:8000/login 
</code>

Description: Users can be able to login into the ecommerce website and shop for skincare items
 
- Parameters
Username:<code> STR </code>
Password: <code> STR </code>


<code>  CURL -X POST https://127.0.0.1:8000/login  </code>



12. Logout Page

Logout Page

Method: GET

Endpoint: <code> 
https://127.0.0.1:8000/logout 
</code>

Description: Logs users out of their accounts

<code> 
CURL -X GET https://127.0.0.1:8000/logout 
</code>

13. Order summary Page

Order summary Page

Method: GET

Endpoint: <code> 
https://127.0.0.1:8000/Order_Summary
</code>

Description: Displays the order summary of a logged in user

<code> CURL -X GET https://127.0.0.1:8000/Order_Summary </code>

14. Checkout Page

Checkout Page

Method: POST

Endpoint: <code> 
https://127.0.0.1:8000/checkout
</code>

Description: Displays the checkout page that contains details for payment and postal details

- Parameters:

street_address: <code> STR </code>
apartment_address: <code> STR </code>
town: <code> STR </code>
state: <code> STR </code>
country: <code> STR </code>
zip: <code> STR </code>
payment_info: <code> STR </code>
phone: <code> INT </code>
email: <code> STR </code>


<code> 
CURL -X POST https://127.0.0.1:8000/checkout 
</code>

15. Payment Options

Payment Options Page

Method: POST

Endpoint: <code> 
https://127.0.0.1:8000/payment/<payment_option>
</code>

Description: User chooses a payment option to checkout

<code> 
CURL -X GET https://127.0.0.1:8000/payment/slug-payment-option 
</code>


16. Coupon Page

Coupon Page

Method: POST

Endpoint:
<code> 
https://127.0.0.1:8000/coupon/
</code>

Description: User can key in their coupon code to get a discount when paying

Parameters:
code: <code> INT </code
<code> 
CURL -X POST https://127.0.0.1:8000/coupon/coupon_code 
</code>

17. Refund Page

Refund Page

Method: GET

Endpoint: <code> https://127.0.0.1:8000/refund </code>

Description: User can key in their coupon code to get a discount when paying

<code> CURL -X GET https://127.0.0.1:8000/refund</code>





pip