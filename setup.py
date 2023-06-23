from setuptools import setup, find_packages

setup(
    name='calendar',
    version='1.0.0',
    description='Calendar App',
    author='Zlata Ranchukova',
    packages=find_packages(),
    install_requires=[
        'google-auth',
        'google-auth-oauthlib',
        'google-api-python-client',
        'sqlalchemy',
        'PySide6',
    ],
    python_requires='>=3.10.7',
)
