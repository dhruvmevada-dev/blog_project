# Django Blog Application

A simple blog built with Django as the minor project for **Session 8 – Django Basics**.
Users can sign up, log in, and create, edit and delete their own posts. Posts can have an image, and the post list supports search and pagination.

## Features

- User authentication: signup, login and logout
- Create, edit and delete blog posts (only the author can edit or delete)
- Post list page and individual post detail page
- Django Admin for managing posts and users
- Bootstrap 5 styling (loaded from a CDN)
- Image upload with `ImageField` and `MEDIA_URL`
- Pagination (5 posts per page)
- Search by title or content

## Tech Stack

- Python 3.10+
- Django 5.2+
- SQLite (default database)
- Pillow (needed for `ImageField`)
- Bootstrap 5

## Project Structure

```
blog_project/
├── manage.py
├── requirements.txt
├── README.md
├── config/                  # Project settings
│   ├── settings.py          # Installed apps, templates, media, login URLs
│   └── urls.py              # Root URLs (admin, auth, blog, media)
├── blog/                    # Main app
│   ├── models.py            # Post model
│   ├── forms.py             # PostForm (ModelForm), SignUpForm
│   ├── views.py             # List, detail, create, edit, delete, signup
│   ├── urls.py              # App URLs
│   └── admin.py             # Admin configuration
├── templates/
│   ├── base.html            # Base layout with navbar
│   ├── blog/                # post_list, post_detail, post_form, post_confirm_delete
│   └── registration/        # login.html, signup.html
└── media/                   # Uploaded images (created at runtime)
```

## Setup and Installation

1. **Go to the project folder**
   ```bash
   cd blog_project
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create an admin user**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open in the browser**
   - Blog: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## URL Routes

| URL | View | Description | Login required |
|---|---|---|---|
| `/` | `post_list` | All posts, with `?q=` search and `?page=` pagination | No |
| `/post/<id>/` | `post_detail` | Single post | No |
| `/post/new/` | `post_create` | Create a post | Yes |
| `/post/<id>/edit/` | `post_edit` | Edit own post | Yes (author only) |
| `/post/<id>/delete/` | `post_delete` | Delete own post | Yes (author only) |
| `/signup/` | `signup` | Register a new account | No |
| `/accounts/login/` | Django auth | Login | No |
| `/accounts/logout/` | Django auth | Logout (POST request) | Yes |
| `/admin/` | Django admin | Manage data | Staff only |

## Data Model

**Post**

| Field | Type | Notes |
|---|---|---|
| `title` | CharField(200) | Post title |
| `content` | TextField | Post body |
| `image` | ImageField | Optional, saved in `media/posts/` |
| `author` | ForeignKey(User) | Set automatically to the logged-in user |
| `created_at` | DateTimeField | Set when the post is created |
| `updated_at` | DateTimeField | Updated on every save |

## Usage Guide

1. Click **Sign Up** to create an account. You are logged in automatically.
2. Click **New Post**, fill in the title and content, optionally add an image, and save.
3. Open a post to read it. If you are the author, you will see **Edit** and **Delete** buttons.
4. Use the search box on the home page to find posts by title or content.
5. Log in to `/admin/` with the superuser account to manage all posts and users.

## Trying the ORM in the Django Shell

```bash
python manage.py shell
```
```python
from blog.models import Post
from django.contrib.auth.models import User

user = User.objects.first()

Post.objects.create(title="Test", content="Hello", author=user)    # Create
Post.objects.filter(title__icontains="test")                       # Read
Post.objects.filter(title="Test").update(title="Updated")          # Update
Post.objects.get(title="Updated").delete()                         # Delete
```

## Concepts Covered

- Project and app setup (`startproject`, `startapp`, `runserver`)
- MVT architecture (Models, Views, Templates)
- Models, fields and relationships (`ForeignKey`), plus migrations
- ORM CRUD operations and `Q` objects for search
- Template inheritance (`base.html`), template tags and filters
- Django forms: `ModelForm`, `UserCreationForm`, GET vs POST handling, CSRF token
- Authentication with `django.contrib.auth`
- Django Admin customization
- Media file handling and pagination

## Notes

- This project is set up for **development only**. Before deploying, set `DEBUG = False`, change `SECRET_KEY`, configure `ALLOWED_HOSTS`, and serve media files through a web server.
- Logout is a POST request in Django 5+, so the navbar uses a small form with a button instead of a plain link.
- Uploaded images are stored in the `media/` folder.
