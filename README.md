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

## 6. Code Walkthrough (Project Overview & Line-by-Line)

This section explains the core logic and architecture of the project to help you understand how each file contributes to the overall website functionality.

### 🛠️ Core Project Entry Point: `manage.py`
This is your **Swiss Army Knife** for Django. You don't usually edit this file, but it handles all the background automation.
- **`os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myWebsite.settings')`**: This tells Django exactly which settings file to use (e.g., database info, allowed hosts).
- **`execute_from_command_line(sys.argv)`**: This allows you to run commands like `runserver` or `migrate` directly from your terminal.

### ⚙️ The Brain: `myWebsite/settings.py`
This file contains the entire configuration for your project.
- **`BASE_DIR = Path(__file__).resolve().parent.parent`**: Automatically calculates the root folder of your project so file paths work on any computer.
- **`INSTALLED_APPS`**: A list of all active modules. Notice **`'newApp'`** at the bottom—this is essential for Django to recognize our custom application.
- **`DATABASES`**: Configured to use `sqlite3`, which is a lightweight database that stores everything in a single file (`db.sqlite3`).
- **`STATIC_URL` & `MEDIA_ROOT`**:
    - `STATIC`: Stores CSS, JavaScript, and site-wide images.
    - `MEDIA`: Handles user-uploaded content (like product photos). We added `os.path.join(BASE_DIR, 'media')` to ensure uploads are stored correctly.


### 🏗️ The Data Structure: `newApp/models.py`
This is where you define the tables in your database.
- **`Product`**: The primary model storing information about items.
- **`ProductFeedback`**: Linked to `Product` via a **`ForeignKey`**. This means one product can have many feedback entries. We added a **`rating`** field here to store the star-rating (1–5).
- **Relationships**:
    - **`OneToOneField`** (ProductCertificate): One product has exactly one unique certificate.
    - **`ManyToManyField`** (Store): A product can be in many stores, and a store can have many products.

### 🧠 The Logic: `newApp/views.py`
This file decides what content to show when a user visits a page.
- **`product_detail`**: Fetches a single product from the database based on the ID in the URL. It also pulls all associated gallery images into a list for the slider.
- **`submit_feedback`**: Our core interaction logic. When a user clicks "Submit":
    1. It checks if the request is **`POST`**.
    2. It pulls the **`name`**, **`email`**, **`message`**, and **`rating`** from the form data.
    3. It creates a new `ProductFeedback` record.
    4. It uses **`messages.success`** to send a "Thank you" notification back to the user.
    5. It **redirects** the user back to the product details page so they don't submit the form twice by accident.


### 🛣️ The Roadmap: `newApp/urls.py`
This maps a URL pattern (like `/product/1/`) to a specific function in `views.py`.
- **`app_name = 'newApp'`**: This allows us to use shortcuts like `{% url 'newApp:home' %}` in our HTML without worrying about conflicts with other apps.
- **`path('product/<int:product_id>/', views.product_detail, name='product_detail')`**: The **`<int:product_id>`** part captures the number from the URL and passes it to the view.

### 🎨 The Presentation: Templates & UI
We use **Bootstrap 5** to make the site look premium and professional.
- **`layout.html` (Master Template)**: Uses **`{% block content %}`** to act as a skeleton. Every other page "fills in" this skeleton.
- **`product_detail.html` (Interactive Detail Page)**:
    - **Image Slider**: Uses a small piece of JavaScript to change the `display` of images when arrows are clicked.
    - **Feedback Stars**: We built an interactive **SVG-based star rating system**. 
    - **JavaScript**: When you click a star, a hidden input is filled with that number (1-5), which is then sent to the server.

---
*Happy Coding!* 🎈
