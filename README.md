# PyGRAZ website

[![Coverage Status](https://coveralls.io/repos/pygraz/website/badge.svg?branch=develop)](https://coveralls.io/r/pygraz/website?branch=develop)

The PyGRAZ website currently supports the creation of meetups and for admin to make session proposal which can
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

Then install [poetry](https://python-poetry.org/) and install the requirements:

```bash
poetry install
```

Next, install the pre-commit hooks to perform static checks on your code everytime you commit:

```bash
poetry run pre-commit install
```

Currently, the site uses an SQLite database. No further setup is needed for this.

If you just want to run the application locally and want to fill the database with generated demonstration data, you can run:

```bash
poetry run python manage.py make_demo
```

To launch the application run:

```bash
poetry run python manage.py runserver
```

Then visit http://127.0.0.1:8000/

## Testing

All tests are located in the `tests` folder and its respective sub-folders.

For testing, run:

```bash
poetry run pytest
```

## Deployment

**To be defined.**
