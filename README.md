# 🚀 Django Website Project Setup Guide

This guide contains the exact steps taken to configure and run this Django project.

## 1. Environment Setup
To keep the project dependencies isolated, we used a Python Virtual Environment.

```powershell
# Create the virtual environment
python -m venv .venv

# Activate the environment (Windows)
.venv\Scripts\activate
```

## 2. Installing Dependencies
The project requires **Django** and **Pillow** (for handling image uploads in the `Product` model).

```powershell
pip install django
pip install Pillow
```

## 3. Configuration Fixes
We added the following line to `myWebsite/myWebsite/settings.py` to resolve modern Django primary key warnings:

```python
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

## 4. Database Setup
Before running the server, ensure all database tables are created and create an admin account.

```powershell
# Navigate to the folder with manage.py
cd myWebsite

# Apply database migrations
python manage.py migrate

# Create your admin account (Set Username and Password)
python manage.py createsuperuser
```

> [!TIP]
> **Setting the Password**: 
> When you run `createsuperuser`, follow the prompts:
> 1. Type a **Username** (e.g., `user`) and hit Enter.
> 2. Skip **Email** by hitting Enter.
> 3. Type your **Password** (letters will not appear—this is normal!) and hit Enter.
> 4. Type it again and hit Enter.
> 5. If it says your password is "too common" or "too short", just type **`y`** to bypass and create it anyway!

## 5. Running the Server
To start the development server, run:

```powershell
python manage.py runserver
```

You can then access the site at:
*   **Website**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
*   **Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---
*Happy Coding!* 🎈
