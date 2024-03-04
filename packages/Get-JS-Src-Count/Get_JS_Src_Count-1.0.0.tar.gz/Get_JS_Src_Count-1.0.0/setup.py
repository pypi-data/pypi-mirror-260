from setuptools import setup, find_packages

setup(
    name='Get_JS_Src_Count',
    version='1.0.0',
    description='A package that get total js src',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'web-assets-downloader',
        'requests',
        'beautifulsoup4'
    ],
)