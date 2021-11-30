# Fastapi Boilerplate
In Progress

## Task
* [x] Define Project Structure
    * [x] Resource
    * [x] Service
    * [x] Repository
    * [x] Model
* [x] PostgresSQL Integrations
    * [x] Migration
    * [x] Query
* [x] User Module
    * [x] CRUD Api
    * [x] Encrypt Password
    * [x] Swagger
* [x] Role Module
    * [x] CRUD Api
    * [x] Swagger
* [ ] Post Module
    * [ ] CRUD Api
    * [ ] Swagger
* [x] Role Module
    * [x] CRUD SQL
* [x] User Module
    * [x] CRUD SQL
* [ ] Post Module
    * [ ] CRUD SQL
* [ ] Authentication and Authorization
    * [ ] JWT Integration
    * [ ] Login Route (Auth Route)
    * [ ] Logout Route (Auth Route)
    * [ ] Authorization / Guard / Permissions
        * [ ] User Authorization
        * [ ] Post Authorization
* [ ] Unit Testing
    * [ ] Login & Logout (Auth Services)
    * [ ] User Services
    * [x] Role Services
    * [ ] Post Services
* [ ] Integration Testing
    * [ ] Auth Repository
    * [ ] Auth Resources
    * [ ] User Repository
    * [ ] User Resources
    * [ ] Role Repository
    * [ ] Role Resources
    * [ ] Post Repository
    * [ ] Post Resources


## How To use
1. Create new alembic migration`alembic revision -m "your message"`
1. Auto generate migration `alembic revision --autogenerate -m "your message"`
1. `uvicorn main:app --reload`