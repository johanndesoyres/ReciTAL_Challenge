# ReciTAL Challenge

For this challenge I was asked to create a basic API for the backend of a management property plateform.


![](https://github.com/johanndesoyres/ReciTAL_Challenge/blob/master/SwaggerUI_Screenshot.png)


The API was designed with FastAPI, SQL Alchemy and Pydantic. Thanks to this API you can interact with a 
SQL database (SQLite). The database contains two tables :

![](https://github.com/johanndesoyres/ReciTAL_Challenge/blob/master/DBschema.png)


A property can be owned by a user thanks to the "owner_id". Here are the operations that the API
allows you to do :

- List all the users
- Register new user
- Get the data from a single user
- Update user data
- Delete a user
- List all properties from a user
- Create a property
- Update property owner
- Update property data
- Delete a property

You can test all these operations with the Swagger UI (http://127.0.0.1:8000/docs) once you have
downloaded the git repository, set up the virtual environment and run the API.

