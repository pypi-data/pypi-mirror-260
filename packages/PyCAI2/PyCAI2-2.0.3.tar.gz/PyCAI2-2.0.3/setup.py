from setuptools import setup, find_packages

VERSION = '2.0.3'
DESCRIPTION = 'Unofficial Python wrapper for character ai, More Easy to use'


# Setting up
setup(
    name="PyCAI2",
    version=VERSION,
    author="Tokai Faclo",
    author_email="otsronca@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['tls_client', 'websockets'],
    keywords=['python', 'AI', 'chat bot', 'character ai'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)