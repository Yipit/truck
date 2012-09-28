## truck - 0.1.3

[![Build Status](https://secure.travis-ci.org/Yipit/truck.png)](http://travis-ci.org/Yipit/truck)

Truck is an event bus layer on top of django signals.

Truck signals and listeners are nothing but regular django signals and
listeners, the difference is that truck imports listeners
automatically from each app, but gives you a global switch to enable
and disable them.

It's intended to use in a django project that has a lot of test
coverage, so that you can avoid slow listeners to run within automated
tests.


# Installation + setup

    user@machine:~$ [sudo] pip install truck


### inside settings.py

When django imports the `truck` app it will trigger its import engine
that will find `listeners.py` inside each one of your installed apps.

There is more information about how it works below, for now just
install the truck app before your local apps.

```python
INSTALLED_APPS = (
    # Things Django Does
    'django.contrib.sessions',
    'django.contrib.sites',
   # ... django builtin apps

   # Then truck:

   "truck",

   # Then your apps
)
```

# Using truck

Truck conveys
"[convention over configuration](http://en.wikipedia.org/wiki/Convention_over_configuration)",
it will try to import a file named `listeners.py` inside each Django
app declared in `settings.INSTALLED_APPS`

## In action

Considering a programmer wants to have the [`post_save`](https://docs.djangoproject.com/en/dev/ref/signals/#post-save) signal connected to the [`User`](https://docs.djangoproject.com/en/dev/topics/auth/#django.contrib.auth.models.User) model.

### {your_django_app}/listeners.py

```python
from truck import receiver

from django.contrib.auth.models import User
from django.db.models.signals import post_save

from your_django_app.models import Profile


@receiver(post_save)
def create_profile(sender, instance=None, **kwargs):
    if isinstance(instance, User):
        profile, created = Profile.objects.get_or_create(user=instance)

```

## Configuring

In order to disable truck, the programmer must set `settings.TESTING` to `True`:

```python

INSTALLED_APPS = (
   # ...
   "truck",
   "your_django_app",
)

TESTING = True
```

The ideal django project layout will have different settings in your
project: at least one for regular environment and another for running
your tests.

### settings/production.py

    TESTING = False

### settings/testing.py

    TESTING = True


# License: LGPL3

    This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
