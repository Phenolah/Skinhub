SKINHUB PROJECT DOCUMENTATION

#Prerequisities

Before you begin, ensure you have met the following requirements:
- Python 3.x installed locally
- Virtual environment <code> (venv) or (pipenv) </code> for managing dependancies.
- Basic Understanding of Python and Django Rest Framework

#Installation
##Setting up on Local Machine

- Clone the repository
<code> 
git clone (repository_url)

 cd <repository_directory)
</code>

- Create a Virtual Environment

<code> 
Python3 -m venv venv
</code> 

 - Activate the Virtual Environment
<code>

    Linux: source venv/bin/activate   
    
    Windows: venv\Scripts\activate
 </code>

 - Install Project Dependancies

<code> pip install -r requirements.txt </code>

- Start the Django Server

<code> pyton  manage.py runserver </code>

API will run on local host 

#API ENDPOINTS

##Home
Home Page 

Endpoint: <code> http://127.0.0.1:8000 </code>

Method: GET

Description: This is the Home page with an overview about the ecommerce product.


##Blog
Blog Page

Endpoint: <code> http://127.0.0.1:8000/blog </code>

Method: GET

Description: The blog page contains different blog post descriptions

##Blog detail
Blog Article Page

Endpoint <code> http://127.0.0.1:8000/blogdetail/<slug:slug>/ </code>

Method: GET

Description: Blog detail page contains the Articles  of the Blog posts.

<code> 
  curl -X GET http://127.0.0.1:8000/blogdetail/slug-value/

</code>

##Shop
Products Page

Endpoint: <code> http://127.0.0.1:8000/shop</code>

Method: GET

Description: The shop page contains various skincare products on sale.

##Shop Details
Products details Page

Endpoint: <code> http://127.0.0.1:8000/details/<slug>/ </code>

Method: GET

Description: The products details contains details of the products such as Description, Price, Add to Cart, Remove from cart and choose size

<code> 
  curl -X GET http://127.0.0.1:8000/details/slug-value/

</code>