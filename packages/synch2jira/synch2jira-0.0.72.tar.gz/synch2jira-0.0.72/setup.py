import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # Here is the module name.
    name="synch2jira",
    # version of the module
    version="0.0.72",
    # Name of Author
    author="wefine",
    # your Email address
    author_email="wefine2529@ebuthor.com",
    # #Small Description about module
    description="Lib",
    # long_description=long_description,
    # Specifying that we are using markdown file for description
    long_description=long_description,
    long_description_content_type="text/markdown",

    # Any link to reach this module, ***if*** you have any webpage or github profile
    # url="https://github.com/username/",
    packages=setuptools.find_packages(),
    #
    # install_requires=[
    #     "fastapi==0.85.1",
    #     "fabric==2.7.1",
    #     "uvicorn==0.19.0",
    #     "pandas==1.5.1",
    #     "openpyxl==3.0.10",
    #     "starlette==0.20.4",
    #     "schedule==1.1.0",
    #     "SQLAlchemy==2.0.16",
    #     "ldap3==2.9.1",
    #     "patchwork==1.0.1",
    #     "pycryptodome==3.17",
    #     "gunicorn==20.1.0",
    #     "pyjwt==2.7.0",
    #     "requests==2.31.0",
    #     "watchdog==3.0.0",
    # ],

    license="MIT",
    # classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
