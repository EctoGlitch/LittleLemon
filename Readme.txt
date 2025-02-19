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



