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
- **`ProductFeedback`**: Linked to `Product` via a **`ForeignKey`**. This includes a **`rating`** field (1–5).
- **`Order` & `OrderItem`**: 
    - **Order** stores delivery information (Name, Phone, Address) and the total price.
    - **OrderItem** links specific products to an order, saving a "snapshot" of the price and name at the time of purchase.
- **Relationships**:
    - **`OneToOneField`** (ProductCertificate): One product has exactly one unique certificate.
    - **`ManyToManyField`** (Store): A product can be in many stores, and a store can have many products.

### 🧠 The Logic: `newApp/views.py`
This file contains the "brains" of the application, handling everything from listing products to processing payments.
- **Session-Based Cart**: We use **`request.session`** to store cart data. This allows users to add items without logging in.
- **`add_to_cart`**: 
    1. It captures the product ID and quantity.
    2. It updates a dictionary in the browser session.
    3. If "Buy Now" is clicked, it skips the cart and goes straight to **`checkout`**.
- **`checkout`**: 
    1. Displays a delivery form.
    2. On submission, it creates an **`Order`** record and multiple **`OrderItem`** records.
    3. It then clears the session cart and redirects to the **Success** page.
- **`submit_feedback`**: Validates form data, creates a feedback record, and uses **`messages.success`** to notify the user.


### 🛣️ The Roadmap: `newApp/urls.py`
This maps URL patterns to view functions.
- **`cart/`**, **`checkout/`**, **`order-success/`**: Added these routes to handle the complete purchase flow.
- **`app_name = 'newApp'`**: Namespacing allows us to use `{% url 'newApp:view_cart' %}` cleanly in our templates.

### 🎨 The Presentation: Templates & UI
We use **Bootstrap 5** and custom CSS/JS for a premium eCommerce feel.
- **`layout.html`**: Now includes a **Cart Badge** in the navigation bar that updates live based on the number of items in your cart.
- **`product_detail.html`**:
    - **"Read More" Toggle**: Implemented a "More/Less" button for descriptions using JavaScript to toggle CSS classes (`desc-collapsed` vs `desc-expanded`).
    - **Real Checkout Forms**: Replaced JS alerts with actual HTML forms for "Add to Cart" and "Buy Now".
- **`cart.html` & `checkout.html`**: 
    - Designed with a clean, modern layout.
    - Includes quantity controls and an interactive "Place Order" button with a loading spinner.
- **`order_success.html`**: Uses an **animated SVG checkmark** and provides a full summary of the user's order details.

---
*Happy Coding!* 🎈
