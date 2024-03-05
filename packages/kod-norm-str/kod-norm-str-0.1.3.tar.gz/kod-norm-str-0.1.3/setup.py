from setuptools import setup, find_packages

setup(
    name="kod-norm-str",
    version="0.1.3",
    author="Nestor Rivera",
    author_email="kod3000@gmail.com",
    description="A package for normalizing and generating a unique identifier of "
                "strings. Great for when you need to search for exact matches.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/kod3000/kod-normalize-str",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
