# Aceit Platform

Aceit Platform is an online revision platform that allows students to take tests and get graded while keeping track of their performance.  Tutors can also create and manage tests for different educational levels and subjects. The platform provides various endpoints to manage the users, taking tests and creating tests.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Permissions](#permissions)
- [Category Hierarchy](#category-hierarchy)
- [Contributing](#contributing)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/mally13/aceit_platform.git
    cd aceit_platform
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**

    ```bash
    cd aceit
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

6. **Start the development server:**

    ```bash
    python manage.py runserver
    ```

## Usage

To view and try out the API endpoints navigate to `http://127.0.0.1:8000/api/v1/schema/swagger-ui/`.

To access the Django admin panel, navigate to `http://127.0.0.1:8000/admin` and log in with the superuser credentials.

## API Endpoints

Here are some of the key API endpoints:

- **Authentication:**
    - `POST /api/v1/account/login/`: Login user
    - `POST /api/v1/account/register/`: Register user
    - `POST /api/v1/account/password-reset/`:  Reset password
    - `POST /api/v1/account/change-password/`: Ch
    - `POST /api/v1/account/token/refresh/`: Refresh access token

- **User Management:**
    - `GET /api/v1/user/profile/`: Get user profile
    - `PUT /api/v1/user/profile/`: Update user profile
    - `GET /api/v1/user/roles/`: Get user roles
    - `PUT /api/v1/user/roles/`: Update user roles

- **Categories:**
    - `GET /api/v1/tests/categories/`: List all top-level categories and their children
    - `GET /api/v1/tests/category/tests/{category_id}/ `: List all tests under a category


- **Tests:**
    - `GET /api/v1/tests/`: List all complete tests from various tutors
    - `GET /api/v1/tests/{id}/`: Retrieve a test by ID

- **Student:**
    - `POST /api/v1/student/tests/{test_id}/responses/`: Submit responses to a test
    - `GET /api/v1/student/tests/attempted`: Retrieve all attempted tests
    - `GET /api/v1/student/tests/attempted/{test_id}`: Retrieve a particular attempted test


- **Tutor:**
    - `GET /api/v1/tutor/completed-tests/`: List all complete tests(Tutors only)
    - `GET /api/v1/tutor/draft-tests/`: List all draft tests(Tutors only) 
    - `POST /api/v1/tutor/test/`: Create a new test (Tutors only)
    - `GET /api/v1/tutor/tests/{id}/`: Retrieve a test by ID(Tutors only)
    - `PUT /api/v1/tutor/tests/{id}/`: Update a test by ID (Tutors only)
    - `DELETE /api/v1/tutor/tests/{id}/`: Delete a test by ID (Tutors only)

## Authentication

This project uses JWT (JSON Web Tokens) for authentication. To obtain a token, use the `/api/v1/account/login/` endpoint. Include the access token in the `Authorization` header of your requests.

## Permissions

- Only authenticated users can access user-specific endpoints.
- Only users with the `tutor` role can create, update, or delete tests.

## Category Hierarchy

Categories can have multiple levels, and each level can have multiple subcategories. For example:

- Pre-Primary
  - PP1
    - Language Activities
    - Mathematical Activities
    - Environmental Activities
    - Psychomotor and Creative Activities
    - Religious Education Activities
    - Pre Braille Activities
  - PP2
    - Language Activities
    - Mathematical Activities
    - Environmental Activities
    - Psychomotor and Creative Activities
    - Religious Education Activities
    - Pre Braille Activities

## Contributing

Contributions are welcome! Please create an issue or submit a pull request for any features, bugs, or documentation improvements.

