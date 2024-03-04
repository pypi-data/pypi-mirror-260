from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as req:
        return req.read().splitlines()

setup(
    name='askdoc',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'loguru==0.7.2',
        'gradio==4.19.2',
        'loguru==0.7.2',
        'openai==1.13.3',
        'backoff==2.2.1',
        'numpy==1.24.3',
        'sentence-transformers==2.3.1',
        'pytesseract==0.3.10',
        'pdf2image==1.17.0',
        'python-dotenv==0.21.1'
    ],
    entry_points={
        'console_scripts': [
            'askdoc=src.chat:main',
        ],
    },
    # Metadata
    author='Romit',
    author_email='romit.73@gmail.com',
    description='Ask a personal doctor for your medical queries',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/romitjain/askdoc',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
