#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
        raise OSError("environment variable DJANGO_SETTINGS_MODULE must be set")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
