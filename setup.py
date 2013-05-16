from setuptools import setup, find_packages

setup(
    name='django-mirrors',
    version=__import__('mirrors').__version__,
    author='Mikela Clemmons',
    author_email='glassreistor@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='http://github.com/glassresistor/django-mirrors/',
    license='BSD',
    description='awesome',
    classifiers=[
    ],
    long_description=open('README.md').read(),
    zip_safe=False, # because we're including media that Django needs
)
