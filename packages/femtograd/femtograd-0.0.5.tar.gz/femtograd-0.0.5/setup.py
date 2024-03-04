import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="femtograd",
    version="0.0.5",
    author="German Gonzalez Karpath",
    author_email="ghgv@yahoo.com",
    description="A tiny scalar-valued autograd engine copied from Karpathy's.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghgv/femtograd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
