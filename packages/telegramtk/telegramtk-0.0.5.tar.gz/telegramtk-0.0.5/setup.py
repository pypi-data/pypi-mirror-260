from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()
requirements = ['requests']

setup(
    name='telegramtk',
    version='0.0.5',
    url='https://github.com/sdelquin/telegramtk.git',
    author='Sergio Delgado Quintero',
    author_email='sdelquin@gmail.com',
    description='Telegram toolkit',
    license='MIT',
    packages=['telegramtk'],
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type='text/markdown',
)
