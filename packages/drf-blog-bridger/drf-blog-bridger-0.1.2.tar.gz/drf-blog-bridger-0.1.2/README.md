# DRF Blog Bridger

## Introduction

DRF Blog Bridger is a simple tool that allows Djamgo Rest Framework Developers to set up a simple blog API without worrying about the underlying code. The tool takes care of things like CRUD operations for blog posts, as well as the comment feature for each post.

## Getting Started

The following instructions will help you install DRF Blog Bridger on your local system and have it running.

### Prerequisites

- Python 3.10 or higher
- Pip
- Django Rest Framework

### Installation and Setup
1. Install the package with:

    ```bash
    pip install drf_blog_bridger
    ```

2. Include the following settings in your `settings.py` file:
    ```python
    INSTALLED_APPS = [

        'blog_bridger_drf',
        'rest_framework',
    ]

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES':[
            'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        ]
    }
    ```
3. Include the following in your project level `urls.py` file:
    ```python
    path('api/posts/', include('blog_bridger_drf.urls')),
    ```
4. Run ``python manage.py migrate`` to create the models.