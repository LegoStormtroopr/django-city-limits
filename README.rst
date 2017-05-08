django-city-limits
==================

Sometimes you need to be able to restrict how many of a certain model a site can have.
For example, the number of active users, the number of posts per user, or the number of active pages.

This django module allows you to easily setup predefined, hardcoded limits to
enforce these kinds of restrictions.

0. Install ``django-city-limits`` from PyPI::

    pip install django-city-limits

1. Add ``django_limits`` to your ``INSTALLED_APPS``::

    INSTALLED APPS = [
        'django_limits',
        # All your other apps
    ]

2. Create and set your limiter class (see below)

    MODEL_LIMIT_CLASS = 'limiter.MyLimiter'

3. Add the limiter middleware to properly render templates::

    MIDDLEWARE_CLASSES = [
        'django_limits.middleware.LimitExceededMiddleware',
        # Your other middleware
    ]


Defining a Limiter class
------------------------

To properly limit your models, you need a limiter class. This isn't auto loaded,
so it can be anywhere, should probably go in a ``limiter.py`` file or in your ``models.py``.

All limiters inherit from the ``django_limits.limiter.Limiter``, but you can override most of this class
as needed.

The simplest limiter, is just an inheritance of this class, with a class attribute defining
the limiting rules. A set of rules is a dictionary, with the key being a *model class*,
and the associated values being a dictionary described below, or list of dictionaries, like so::

    from django_limits.limiter import Limiter
    from django.contrib.auth.models import User
    
    class MyLimiter(Limiter):
        rules = {
            User: [
                {
                    'limit': 20,
                    'message': "Only 20 active users allowed",
                    'filterset': Q(is_active=True)
                },
                {
                    'limit': 10,
                    'message': "Only 10 staff members allowed",
                    'filterset': Q(is_staff=True)
                }
            ]
        }

The above Limiter will only allow a maximum of 20 active users, and 10 staff members.

Defining a rules dictionary
---------------------------

A rules dictionary can contain the following keys:

* ``limit`` (required - The total number of the given model allowed, or if there is a queryset, the total allowed for that queryset
* ``message`` - The message shown when a user tries to exceed this number
* ``filterset`` - A django Q filters that defines the types of models to restrict on, if this is not set the total number of the model in the database is used (e.g ``Model.objects.all()``)
* ``template`` - The template used to render the page explaining the limit restriction, defaults to ``django_limits/limit_exceeded.html``

An example rule is below for a widget is below::

    Widget: [
        {
            'limit': 10,
            'message': "Only 10 staff members allowed",
            'filterset': Q(color="Blue")
        },
        {
            'limit': 10,
            'message': "Only 10 staff members allowed",
            'filterset': Q(color="Red")
        },
        {
            'limit': 30,
            'message': "Only 30 widgets allowed",
            'template': "widgets/totla_widgets_exceeded.html'
        }
    ]

In this example, at most 10 blue, 10 red and a total 30 widgets are allowed.

How it works
------------

Django limtis installs a ``pre_save`` signal for every model, and checks against the rules, and
to prevent the save from finishing throws a ``LimitExceeded`` exception which is caught by the
middleware, which in turn renders a page with a HTTP 403 error.

Apologies to Tina Turner.