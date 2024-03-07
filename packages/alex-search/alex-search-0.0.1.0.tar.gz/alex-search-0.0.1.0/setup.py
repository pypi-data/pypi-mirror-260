from setuptools import setup, find_packages
with open('index.rst', 'r') as f:
    long_description = f.read()
setup(
    name='alex-search',
    version='0.0.1.0',
    description='A command-line tool for quickly searching and extracting papers using OpenAlex API',
    long_description=long_description,
    author='yabets ebren',
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    install_requires=[
        'requests',
        'click',
        'tabulate',
        'jsonlib-python3',
        'csvkit'
    ],
    entry_points={
        'console_scripts': [
            'alex-search = openAlex:cli'
        ]
    }
)
