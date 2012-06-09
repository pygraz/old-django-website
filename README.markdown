# PyGRAZ website

The PyGRAZ website currently supports the creation of meetups and for users to make session proposal which can
then be assigned to a meetup.

Each proposal can have descriptive information associated with it like an abstract, a description and notes.
Slides can be linked to from the session page (as well as the meetup page).

## Requirements

* Django and everything mentioned in the requirements.txt
* Compass
* For all functionality: a [Postmark][pm] account
* For all functionality: a [Recaptcha][rc] account

To install the Python requirements, using [pip][pip] is recommended.

## Setup

First clone this repository:
<pre>
git clone <url of this repo>
cd website
</pre>

Then create a virtualenv for all the Python requirements, activate it and install the requirements:
<pre>
mkvirtualenv --no-site-packages env
source env/bin/active
pip install -r requirements.txt
</pre>

We are using a multi-settings-file approach for handling settings on different target systems. For local development
you should create a "pygraz_website/settings/development.py" which could include following settings:

<pre><code>from .base import *

RECAPTCHA_PRIVATE_KEY = "GET_YOURSELF_A_RECAPTCHA_KEY"
RECAPTCHA_PUBLIC_KEY = "GET_YOURSELF_A_RECAPTCHA_KEY"
POSTMARK_API_KEY = 'GET_YOURSELF_A_POSTMAR_KEY'
SECRET_KEY = '12345'
POSTMARK_TEST_MODE = True</code></pre>

Now on to creating the database. By default the website looks for a PostgreSQL database by the name of "pygraz-website"
accessibly by the current system user.

If you want to use for instance a sqlite database, add following content to your development.py file you created in
the last step:

<pre><code>
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(ROOT, 'localdb.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
</code></pre>

Now run following commands to initialize the database:

<pre>
python manage-dev.py syncdb
python manage-dev.py migrate
</pre>

To finally start the server run ...

<pre>python manage-dev.py runserver</pre>

When you first visit http://localhost:8000, you will notice that all the stylesheets are still missing.
For local development we would recommend that you open another terminal, go to the pygraz_website/static folder and
execute following command:

<pre>compass watch</pre>

This will compile the stylesheets using Compass and keep the process running so that changes the the .scss files are
automatically compiled into .css files.

## Components not included

The pygraz.org website uses the icomoon icon-font for its icons. Due to license restrictions we are not allowed to
bundle it with the website's source code. For details on this font visit http://keyamoon.com/icomoon/


[pip]: http://pypi.python.org/pypi/pip
[rc]: http://recaptcha.net/
[pm]: http://postmarkapp.com
