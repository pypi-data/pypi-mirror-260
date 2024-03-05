from setuptools import setup, find_packages

setup(
    name="coolearn",
    version="0.1.0",
    author="boyjiangboyu",
    author_email="boyjiangboyu@outlook.com",
    description="Personalized Learning Assistant",
    long_description=open("Readme.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=open("requirements.txt").read().splitlines(),
    python_requires='>=3.10',
)