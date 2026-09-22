# Task Management API

A REST API built with FastAPI for managing users and tasks with authentication, authorization, validation, and automated testing.

## Features

- User management
- User authentication
- JWT-based authorization
- Task management
- User-specific task ownership
- Request validation using Pydantic
- Service-layer architecture
- Automated testing with pytest
- Interactive API documentation with Swagger UI

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- JWT
- Git & GitHub

## Project Structure

```text
task-management-api/
|
+-- app/
|   +-- config.py
|   +-- main.py
|   |
|   +-- auth/
|   |   +-- dependencies.py
|   |   +-- security.py
|   |
|   +-- models/
|   |   +-- task.py
|   |   +-- user.py
|   |
|   +-- schemas/
|   |   +-- auth.py
|   |   +-- task.py
|   |   +-- user.py
|   |
|   +-- services/
|   |   +-- auth_service.py
|   |   +-- task_service.py
|   |   +-- user_service.py
|   |
|   +-- utils/
|       +-- validators.py
|
+-- tests/
|   +-- test_auth.py
|   +-- test_tasks.py
|   +-- test_users.py
|
+-- .env.example
+-- .gitignore
+-- README.md
+-- requirements.txt