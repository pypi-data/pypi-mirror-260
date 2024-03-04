import os
import setuptools

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md'), 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = "apikeylogger",
    version = "1.1.1",
    author = "Federico Romeo",
    author_email = "federico.romeo.98@gmail.com",
    description = "This library allows you to log the OpenAI api usage *by key* without having to change your code",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/federicoromeo/apikeylogger",
    keywords  =  ['openai', 'apikey', 'api', 'logger', 'tracker'],
    project_urls = {'Source': 'https://github.com/federicoromeo/apikeylogger'},
    license = 'MIT',
    packages = setuptools.find_packages(),
    include_package_data = True,
    classifiers = [],
    python_requires = ">=3.6",
    install_requires = [
        "openai >= 1.6.0",
        "python-dotenv >= 0.18.0",
        "tiktoken",
        "beautifulsoup4"
    ],
)
