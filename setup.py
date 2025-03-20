from setuptools import setup, find_packages

setup(
    name="src",
    version="0.0.1",
    author="AYUSH",
    author_email="ayushrajputparihar@gmail.com",
    packages=find_packages(),
    install_requires=[
        'numpy==1.24.3',
        'pandas==2.0.3',
        'PyPDF2==3.0.1',
        'python-docx==1.0.1',
        'nltk==3.8.1',
        'flask==3.0.0',
        'flask_cors==4.0.0',
        'requests==2.31.0',
    ]
)