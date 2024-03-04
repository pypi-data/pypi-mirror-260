from setuptools import setup, find_packages

setup(
    name="robotAzureSync",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "robotAzureSync=robotAzureSync.robotAzureSync:robotAzureSync",
        ],
    },
    author="Fábio Ribeiro dos Santos Quispe",
    author_email="fabiorisantos1981@gmail.com",
    description="Synchronization functionalities for Azure-related tasks.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fabiorisantosquispe/robot-azure-sync",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
