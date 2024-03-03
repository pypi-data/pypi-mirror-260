from setuptools import setup, find_packages

setup(
    name="cronusalert",
    version="0.1.0",
    author="Mathew Perkins",
    author_email="57matperkins57@gmail.com",
    description="A Python client for Cronus alerts",
    long_description=open("../README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mperkins8080/cronus-alert/python/cronusalert",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
