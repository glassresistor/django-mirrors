from setuptools import setup, find_packages

setup(
    name='django-sweetness',
    version=__import__('sweetness').__version__,
    author='Mikela Clemmons',
    author_email='glassreistor@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='http://github.com/glassresistor/django-sweetness/',
    license='BSD',
    description='awesome',
    classifiers=[
    ],
    long_description=open('README.md').read(),
    zip_safe=False, # because we're including media that Django needs
)
