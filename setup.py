from setuptools import setup

exec(open("rmrkl/version.py").read())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rmrkl",
    version=__version__,
    description="Robust Modular Reasoning, Knowledge and Language agent that uses tools and retries on failure",
    author="Andrew White",
    author_email="andrew.white@rochester.edu",
    url="https://github.com/whitead/robust-mrkl",
    license="MIT",
    packages=["rmrkl"],
    install_requires=["langchain>=0.0.157"],
    test_suite="tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)
