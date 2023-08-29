# PyGRAZ website

[![Coverage Status](https://coveralls.io/repos/pygraz/website/badge.svg?branch=develop)](https://coveralls.io/r/pygraz/website?branch=develop)

The PyGRAZ website currently supports the creation of meetups and for users to make session proposal which can
then be assigned to a meetup.

Each proposal can have descriptive information associated with it like an abstract, a description and notes.
Slides can be linked to from the session page (as well as the meetup page).

## Requirements

- Django and everything mentioned in the requirements.txt
- Compass
- For all functionality: a [Postmark][pm] account
- For all functionality: a [Recaptcha][rc] account

To install the Python requirements, using [pip][pip] is recommended.

## Setup

First clone this repository:

```bash
git clone <url of this repo>
cd website
```

Then create a virtualenv for all the Python requirements, activate it and install the requirements:

```bash
mkvirtualenv --no-site-packages env
source env/bin/active
pip install -r requirements/base.txt
pip install -r requirements/development.txt
```

We are using a multi-settings-file approach for handling settings on different target systems. For local development
you should use "pygraz_website/settings/development.py" which just sets some plain defaults and doesn't send emails.

Next, install the pre-commit hooks to perform static checks on your code everytime you commit:

```bash
pre-commit install
```

Now on to creating the database. By default, the website looks for a PostgreSQL database by the name of
"pygraz-website" accessibly by the current system user.

If you want to use for instance a sqlite database, add following content to your development.py file you created in
the last step:

```python
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
```

Now run following commands to initialize the database:

```bash
python manage-dev.py syncdb
python manage-dev.py migrate
```

To finally start the server run ...

```bash
python manage-dev.py runserver
```

When you first visit http://localhost:8000, you will notice that all the stylesheets are still missing.
For local development we would recommend that you open another terminal, go to the pygraz_website/static folder and
execute following command:

```bash
compass watch
```

This will compile the stylesheets using Compass and keep the process running so that changes the .scss files are
automatically compiled into .css files.

## Components not included

The pygraz.org website uses the icomoon icon-font for its icons. Due to license restrictions we are not allowed to
bundle it with the website's source code. For details on this font visit http://keyamoon.com/icomoon/

## Deployment

For deployments, we are using an Ansible playbook which builds a production.zip
and deploys that onto the target server:

```bash
cd ansible/playbooks
ansible-playbook -i ../hosts deploy.yml
```

[pip]: http://pypi.python.org/pypi/pip
[rc]: http://recaptcha.net/
[pm]: http://postmarkapp.com
