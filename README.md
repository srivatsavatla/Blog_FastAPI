This is a basic FastAPI application which is built to understand the FastAPI applications.

FastAPI provides documentation using SwaggerUI(/docs) and (/redo) which can be used for unit testing.

SQL Alchemy is a python SQL development toolkit.You can use it for ORM and making tables

You can make relationships b/w tables using it

ORM(Object relational mapping) means mapping our class/model/object to a table. i.e.
we make a class for a table which is reponsible for that table CRUD operations.
db:Session=Depends(get_db) converts the sessionn into  a pydantic thing


To install all the dependencies use 

```
pip install -r requirements.txt
```