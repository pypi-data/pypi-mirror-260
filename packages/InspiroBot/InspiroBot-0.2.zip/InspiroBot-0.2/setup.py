from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="InspiroBot",
    version="0.2",
    author="masswyn",
    author_email="maswwyn24@gmail.com",
    description="A web application for generating random motivational affirmations and inspiring quotes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maswwyn/InspiroBot",
    packages=find_packages(),
    package_data={
        "": ["LICENSE", "README.md", "requirements.txt", "app.py", "index.html", "inspirobot.py", "quotes_of_the_day.txt"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
