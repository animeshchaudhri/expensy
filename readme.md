# Expensy backemnd

## Overview

The Expense Tracker API allows users to manage their expenses and track shared costs with friends or family. It supports multiple split types: equal, exact, and percentage.

## Features

- User registration and profile management
- Expense creation with different split types
- Ability to view user expenses
- Download balance sheet in CSV format

## Technologies Used

- Django
- Django REST Framework
- SQLite (for local development)
- Python 3.x

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone https://github.com/animeshchaudhri/expensy
cd expense-tracker
```

### Step 2: Create a Virtual Environment

It’s recommended to create a virtual environment for the project.

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Requirements

```bash
pip install -r requirements.txt
```

### Step 4: Configure Database

The project is set up to use SQLite by default. Ensure the following configuration is in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Step 5: Run Migrations

```bash
python manage.py migrate
```

### Step 6: Create a Superuser (Optional)

If you want to access the Django admin panel:

```bash
python manage.py createsuperuser
```

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

The API will be accessible at `http://127.0.0.1:8000/api/`.

## API Documentation

### User Registration

- **Endpoint:** `/api/users/`
- **Method:** `POST`
- **Request Body:**

```json
{
    "email": "user@example.com",
    "first_name": "First",
    "last_name": "Last",
    "password": "yourpassword",
    "profile": {
        "mobile": "1234567890"
    }
}
```

- **Response:**

```json
{
    "id": 1,
    "email": "user@example.com",
    "first_name": "First",
    "last_name": "Last",
    "mobile": "1234567890"
}
```

### Create an Expense

- **Endpoint:** `/api/expenses/`
- **Method:** `POST`
- **Request Body:**

```json
{
    "title": "Dinner",
    "amount": "3000.00",
    "split_type": "EQUAL",
    "paid_by_email": "user@example.com",
    "splits": [
        {"user_email": "user1@example.com"},
        {"user_email": "user2@example.com"},
        {"user_email": "user3@example.com"}
    ]
}
```

- **Response:**

```json
{
    "id": 1,
    "title": "Dinner",
    "amount": "3000.00",
    "split_type": "EQUAL",
    "splits": [
        {
            "user_email": "user1@example.com",
            "amount": "1000.00",
            "percentage": 33.33
        },
        {
            "user_email": "user2@example.com",
            "amount": "1000.00",
            "percentage": 33.33
        },
        {
            "user_email": "user3@example.com",
            "amount": "1000.00",
            "percentage": 33.33
        }
    ],
    "created_at": "2024-10-27T07:30:10.259409Z"
}
```

### View User Expenses

- **Endpoint:** `/api/expenses/user_expenses/`
- **Method:** `GET`
- **Query Parameters:** `email=user@example.com`

- **Response:**

```json
[
    {
        "id": 1,
        "title": "Dinner",
        "amount": "3000.00",
        "split_type": "EQUAL",
        "splits": [...],
        "created_at": "2024-10-27T07:30:10.259409Z"
    }
]
```

### Download Balance Sheet

- **Endpoint:** `/api/expenses/download_balance_sheet/`
- **Method:** `GET`
- **Response:** A CSV file download containing user balances.

#
