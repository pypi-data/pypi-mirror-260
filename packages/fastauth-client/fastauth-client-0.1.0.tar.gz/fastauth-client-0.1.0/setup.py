from setuptools import setup

VERSION = "0.1.0"

setup(
    name="fastauth-client",
    version=VERSION,
    license="MIT",
    description="A utility for printing colored messages to the console.",
    long_description=open("README.md").read(),  # Make sure to create a README.md file
    long_description_content_type="text/markdown",
    author="Sikandar Moyal",
    author_email="sikandar1838@gmail.com",
    url="https://github.com/sikandar1838/console",
    package_dir={"": "src"},
    packages=["console"],
    keywords=["Console", "Colorful Output", "CLI", "Text Formatting"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
