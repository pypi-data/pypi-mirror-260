from setuptools import setup, find_packages

setup(
    name='gougleai',
    version='1.0.5.5',
    author='Gougle AI LLC',
    author_email='gouglellc@gmail.com',
    description='The Python package for Gougle AI API.',
    long_description=open('README.md', "r").read(),
    long_description_content_type='text/markdown',
    url='https://www.github.com/gougle-official/gougleai-python',
    packages=find_packages(),
    py_modules=['gougleai'],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
    license='GPL-2.0',
)
