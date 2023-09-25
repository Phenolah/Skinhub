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
Endpoint
Login User
Endpoint: https://team-piranha.onrender.com/api/login/

Method: POST

Description: Logs a user in to the event app.

Parameters:

Email: string

pass_id: string