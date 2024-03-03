from setuptools import setup, find_packages


setup(
    name="Py-uTube",
    version="0.1",
    author="Brhoom",
    author_email="hetari4all@gmail.com",
    description="YouTube Downloader CLI",
    packages=find_packages(),
    install_requires=["pytube", "inquirer",
                      "yaspin", "requests", "rich", "inquirer", "termcolor"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "console_scripts": [
            "uTube=uTube:cli.app",
            "utube=uTube:cli.app",
        ],
    },
    python_requires=">=3.6",
    readme="README.md",
)
