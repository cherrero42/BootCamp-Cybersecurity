from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='my_minipack',
    version="1.0.1",
    author='cherrero',
    author_email='cherrero@student.42.fr',
    description="A small example package called my_minipack",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="None",
    package_dir={"": "src"},
    packages=find_packages(where="./src"),    
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Students",
        "Topic :: Education",
        "Topic :: HowTo",
        "Topic :: Package",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires='>=3.7',
)