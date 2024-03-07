from setuptools import setup, find_packages

setup(
    name="FreeNove_4WD-Rover_Pico",
    version="0.1",
    author="AstroScott",
    #author_email="your_email@example.com",
    description="A package for controlling the FreeNove 4WD Rover for pi pico using micropython. This package has "
                "been adapted from the arduino-pico version.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="http://github.com/yourusername/FreeNove_Rover",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
