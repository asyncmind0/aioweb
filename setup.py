from setuptools import setup, find_packages

setup(
    name = "aioweb",
    version = "0.1",
    url = 'http://github.com/jagguli/aioweb',
    license = 'BSD',
    description = "A minimal framework for webapps using asyncio",
    author = 'Steven Joseph',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)

