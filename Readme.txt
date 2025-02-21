Starting the project
1. Open terminal
2. change into the workspace directory
`cd workspace`
3. start the virtual environment
scripts\activate
4. change into the littleLemon directory
`cd littleLemon`
5. start the server
`python manage.py runserver`

/**********************************************************************************************/
/**********************************************************************************************/
/**********************************************************************************************/
/**********************************************************************************************/

When testing if INSOMNIA be sure to clear cookies because the application 
will cache the old token and you will get a 403 error
{"detail": "CSRF Failed: CSRF token missing."}


/* Pathing for peer testing */
/**********************************************************************************************/
restaurant/book/

Setup for INSOMNIA
METHOD: POST
http://127.0.0.1:8000/restaurant/book/

multipart/form-data

"name": "John",
"no_of_guests": "1",
"reservation": "12/12/2022",
"time_slot": "14", // 14:00 (army time)

application/json
{
    "name": "John",
    "no_of_guests": "1",
    "reservation": "12/12/2022",
    "time_slot": "14"
}

/*************************************************************************************************/
restaurant/booking/tables/
displays all bookings if a valid token is provided

Setup for INSOMNIA
METHOD: GET
http://127.0.0.1:8000/restaurant/booking/tables/


/*************************************************************************************************/
/signup/
creates a new user
Setup for INSOMNIA
METHOD: POST
http://127.0.0.1:8000/signup/

multipart/form-data
"username": "John",
"email": "john@email.com",
"password1": "123456789",
"password2": "123456789"

application/json
{
    "username": "John",
    "email": "john@email.com",
    "password1": "123456789",
    "password2": "123456789"
}

/*************************************************************************************************/
/signin/
BROWSER
METHOD: POST 
http://127.0.0.1:8000/login/
The browser will automatically send the CSRF token in the headers tab
Input valid username and password
click submit

    

INSOMNIA
METHOD: POST
http://127.0.0.1:8000/api/login/



