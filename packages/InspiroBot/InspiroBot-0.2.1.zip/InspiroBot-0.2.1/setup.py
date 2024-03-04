from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="InspiroBot",
    version="0.2.1",
    author="masswyn",
    author_email="maswwyn24@gmail.com",
    description="A web application for generating random motivational affirmations and inspiring quotes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maswwyn/InspiroBot",
    packages=find_packages(),
    install_requires=[
        "Flask==3.0.2",
        "certifi==2024.2.2",
        "charset-normalizer==3.3.2",
        "click==8.1.7",
        "colorama==0.4.6",
        "blinker==1.7.0",
        "idna==3.6",
        "importlib-metadata==7.0.1",
        "itsdangerous==2.1.2",
        "Jinja2==3.1.3",
        "markdown-it-py==3.0.0",
        "MarkupSafe==2.1.5",
        "more-itertools==10.2.0",
        "pkginfo==1.9.6",
        "Pygments==2.17.2",
        "requests==2.31.0",
        "requests-toolbelt==1.0.0",
        "rich==13.7.1",
        "urllib3==2.2.1",
        "Werkzeug==3.0.1",
        "zipp==3.17.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
