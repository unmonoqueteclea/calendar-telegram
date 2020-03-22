#!/usr/bin/env python

from distutils.core import setup

setup(name='calendar-telegram',
      version='0.1.2',
      description='Datepicker for python-telegram-bot',
      author='',
      author_email='',
      url='https://github.com/chiselko6/calendar-telegram',
      package_dir={'': 'src'},
      packages=['calendar_telegram'],
      install_requires=['python-telegram-bot>=12,<12.5'],
     )
