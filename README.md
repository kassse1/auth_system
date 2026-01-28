Custom Authentication and Authorization System

---

## Description

This project implements a custom backend authentication and authorization system using FastAPI, JWT, and PostgreSQL.

The system provides:
- User registration with password confirmation
- Login and logout
- JWT-based authentication
- Role-based access control (RBAC)
- Database-driven permission management
- Soft deletion of user accounts

The solution does not rely on built-in authentication or authorization mechanisms.

---

## Technologies Used

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT (python-jose)
- Passlib (bcrypt)
- Uvicorn

---

## Project Structure
Project structure is shown in the screenshot below.

---

## Authentication

Authentication is implemented using JWT tokens.

### Registration

- Endpoint: `POST /register`
- Required fields:
  - first_name
  - last_name
  - email
  - password
  - password_confirm
- Passwords must match
- Email must be unique
- User is created with `is_active = true`

### Login

- Endpoint: `POST /login`
- User logs in using email and password
- On success, a JWT token is issued

### Logout

- Stateless logout
- Implemented by removing the JWT token on the client side

---

## User Management

### Update Profile

- Endpoint: `PATCH /users/me`
- Allows authenticated users to update their own profile data

### Delete Account (Soft Delete)

- Endpoint: `DELETE /users/me`
- User account is not removed from the database
- Field `is_active` is set to `false`
- Further login attempts are denied

---

## Access Control Model

The project uses a custom role-based access control (RBAC) model with database-driven permissions.

### Core Entities

#### Users
- Each user has:
  - role_id
  - is_active flag
- Only active users can authenticate and access protected endpoints

#### Roles
- Define permission sets
- Examples:
  - user
  - admin

#### Business Elements
- Represent protected application resources
- Examples:
  - products
  - users

#### Access Rules

Permissions are stored in the `access_role_rules` table.

Each rule defines:
- role
- business element
- allowed actions

Supported permissions:
- read
- create
- update
- delete
- read_all
- update_all
- delete_all

---

## Authorization Flow

1. User authenticates and receives a JWT token
2. Token is validated on each protected request
3. User role is extracted from the token
4. Required permission is checked in the database
5. Access decision:
   - 401 Unauthorized — user is not authenticated
   - 403 Forbidden — insufficient permissions
   - 200 OK — access granted

---

## Example: Products Endpoint

Endpoint:
GET /products

Access logic:
- Requires `read` permission for the `products` business element
- Regular users receive 403 Forbidden
- Admin users receive 200 OK

---

```## Database Setup

1. Create database:
CREATE DATABASE auth_db;
INSERT INTO roles (id, name) VALUES (1, 'user'), (2, 'admin');
INSERT INTO business_elements (id, name) VALUES (1, 'products');
INSERT INTO access_role_rules (role_id, element_id, read_permission)
VALUES (2, 1, true);

Running the Project
Install dependencies : pip install -r requirements.txt

Run the application : uvicorn app.main:app --reload

Swagger UI : http://127.0.0.1:8000/docs
