# Django Tutorial for Beginners - Step by Step Guide

## 📚 Table of Contents
1. [What is Django?](#what-is-django)
2. [Installation & Setup](#installation--setup)
3. [Creating Your First Project](#creating-your-first-project)
4. [Understanding Project Structure](#understanding-project-structure)
5. [Creating Your First App](#creating-your-first-app)
6. [Views & URL Routing](#views--url-routing)
7. [Templates](#templates)
8. [Static Files (CSS, JS, Images)](#static-files-css-js-images)
9. [Common Problems & Solutions]~
(#common-problems--solutions)

---

## 🎯 What is Django?

**Django** is a Python web framework that helps you build websites quickly and easily.

**Key Points:**
- It's like a toolbox for building websites
- Written in Python programming language
- Follows the "Don't Repeat Yourself" principle
- Helps organize your code neatly

---

## 🛠️ Installation & Setup

### Step 1: Install Python
- Download Python from [python.org](https://python.org)
- Version 3.8 or higher is recommended
- During installation, check "Add Python to PATH"

### Step 2: Install Django
Open Command Prompt/Terminal and type:
```bash
pip install django
```

### Step 3: Verify Installation
```bash
django-admin --version
```
You should see a version number if installation was successful.

---

## 🚀 Creating Your First Project

### Step 1: Create Project
```bash
django-admin startproject mywebsite
cd mywebsite
```

**What happened?**
- `django-admin startproject` creates a new Django project
- `mywebsite` is your project name (you can change it)
- `cd mywebsite` moves you into the project folder

### Step 2: Run Development Server
```bash
python manage.py runserver
```

**What you'll see:**
- Server starts at http://127.0.0.1:8000/
- Open this URL in your browser
- You should see the Django welcome page!

---

## 📁 Understanding Project Structure

Your project folder looks like this:
```
mywebsite/
├── manage.py          # Django's command-line tool
└── mywebsite/         # Your main project folder
    ├── __init__.py    # Tells Python this is a package
    ├── settings.py    # Project settings (database, apps, etc.)
    ├── urls.py        # URL routing configuration
    ├── asgi.py        # ASGI server config
    └── wsgi.py        # WSGI server config
```

**Important Files:**
- `manage.py`: Use this for Django commands
- `settings.py`: Configuration file for your project
- `urls.py`: Maps URLs to views (like a phone book for your website)

---

## 🎮 Creating Your First App

### What is an App?
An app is a self-contained part of your website (like a blog, shop, or user system).

### Step 1: Create an App
```bash
python manage.py startapp blog
```

### Step 2: Register the App
Open `settings.py` and add your app to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ... other apps
    'blog',  # Add your app here
]
```

---

## 🔗 Views & URL Routing

### What are Views?
Views are Python functions that handle web requests and return responses.

### Step 1: Create a View
Open `blog/views.py` and add:
```python
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, World! This is my first Django page!")
```

### Step 2: Create URLs for the App
Create `blog/urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

### Step 3: Include App URLs in Main Project
Open `mywebsite/urls.py` and add:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Add this line
]
```

### Step 4: Test It!
Run the server and visit http://127.0.0.1:8000/

---

## 🎨 Templates

### What are Templates?
Templates are HTML files with Django-specific tags that display dynamic content.

### Step 1: Create Templates Folder
Create these folders:
```
blog/
└── templates/
    └── blog/
        └── home.html
```

### Step 2: Create HTML Template
In `blog/templates/blog/home.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Blog</title>
</head>
<body>
    <h1>Welcome to My Blog!</h1>
    <p>This is my first Django template.</p>
</body>
</html>
```

### Step 3: Update View to Use Template
Modify `blog/views.py`:
```python
from django.shortcuts import render

def home(request):
    return render(request, 'blog/home.html')
```

---

## 🎭 Static Files (CSS, JavaScript, Images)

### What are Static Files?
These are files that don't change: CSS styles, JavaScript, images, etc.

### Step 1: Create Static Folder
```
blog/
└── static/
    └── blog/
        ├── css/
        │   └── style.css
        └── images/
```

### Step 2: Add CSS
In `blog/static/blog/css/style.css`:
```css
body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    margin: 0;
    padding: 20px;
}

h1 {
    color: #333;
    text-align: center;
}
```

### Step 3: Link CSS in Template
Update your template to include CSS:
```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>My Blog</title>
    <link rel="stylesheet" href="{% static 'blog/css/style.css' %}">
</head>
<body>
    <h1>Welcome to My Blog!</h1>
    <p>This is my first Django template with styling!</p>
</body>
</html>
```

---

## 🚨 Common Problems & Solutions

### Problem 1: Template Not Found
**Error:** `TemplateDoesNotExist`
**Solution:** Check your template folder structure. It should be:
```
app_name/
└── templates/
    └── app_name/
        └── template_name.html
```

### Problem 2: Static Files Not Working
**Error:** CSS/JS files not loading
**Solution:** 
1. Check `settings.py` has `STATIC_URL = 'static/'`
2. Make sure you use `{% load static %}` in templates
3. Verify folder structure is correct

### Problem 3: Page Not Found (404)
**Error:** URL not found
**Solution:** 
1. Check your `urls.py` files
2. Make sure you included app URLs in main project
3. Verify URL patterns match what you're typing

### Problem 4: Server Won't Start
**Error:** Port already in use
**Solution:** Run server on different port:
```bash
python manage.py runserver 8080
```

---

## 📝 Quick Reference Commands

### Django Management Commands
```bash
# Start new project
django-admin startproject projectname

# Start new app
python manage.py startapp appname

# Run development server
python manage.py runserver

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
```

---

## 🎯 Next Steps

After mastering these basics, you can learn:
1. **Django Models** - Working with databases
2. **Django Forms** - Handling user input
3. **User Authentication** - Login/registration systems
4. **Django Admin** - Built-in admin interface
5. **Deployment** - Putting your website online

---

## 💡 Tips for Students

1. **Practice Daily**: Even 15 minutes helps!
2. **Break Problems Down**: Big problems are just small problems together
3. **Read Error Messages**: They tell you exactly what's wrong
4. **Use Documentation**: Django has excellent official docs
5. **Ask for Help**: Don't be afraid to ask questions!

---

## 🔗 Helpful Resources

- [Official Django Documentation](https://docs.djangoproject.com/)
- [Django Girls Tutorial](https://tutorial.djangogirls.org/)
- [MDN Web Docs](https://developer.mozilla.org/) - For HTML/CSS help

---

**Happy Coding! 🎉**

Remember: Every expert was once a beginner. Keep practicing and you'll get better!
