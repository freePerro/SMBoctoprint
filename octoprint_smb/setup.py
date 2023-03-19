from setuptools import setup, find_packages

setup(
    name="octoprint_smb",
    version="0.1",
    description="An OctoPrint plugin for accessing and managing files on an SMB/CIFS network share",
    author="Doug Blumer",
    author_email="dougblumer51@gmail.com",
    url="https://github.com/your_username/octoprint_smb",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "OctoPrint>=1.3.0",
        "smbprotocol>=1.6.0",
    ],
    entry_points={
        "octoprint.plugin": [
            "octoprint_smb = octoprint_smb"
        ]
    },
)
