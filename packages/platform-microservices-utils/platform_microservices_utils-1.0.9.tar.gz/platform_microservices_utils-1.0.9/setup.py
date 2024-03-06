from setuptools import setup, find_packages

setup(
    name="platform_microservices_utils",
    version="1.0.9",
    author="Vishwajeet Kale",
    author_email="vishwajeet.kale.v2stech@gmail.com",
    description="""
    "Platform Microservices Utils is a comprehensive Python package designed to streamline microservice communication. 
    With a focus on security and efficiency, this package offers a range of utilities including microservice client requests, 
    header builders, middleware such as microservice token validators, URL builders, and an INI parser. 
    Simplify your microservice architecture and enhance communication reliability with Platform Microservices Utils.""",
    packages=find_packages(),
    long_description_content_type="text/markdown",
    # long_description=open("README.md").read(),
    license="MIT",
    include_package_data=True,  # Include package data specified in MANIFEST.in
    install_requires=[
        # 'Django>=3.1',
        # 'djangorestframework>=3.11.1'
        # Add other dependencies here
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
