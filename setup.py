from setuptools import setup


setup(
    name='pytba-calendar',
      version='0.1.0',
      description='InlineKeyboardButtons-Calendar for PyTelegramBotApi',
      author='Pavel Anokhin',
      author_email='p.a.anokhin@gmail.com',
      url='https://github.com/kazusman/pytba-calendar',
      packages=['pytba_calendar'],
      license='MIT',
      keywords='telegram bot api calendar inline',
      install_requires=['pytelegrambotapi', 'pytz']
)