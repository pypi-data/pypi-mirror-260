import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python3-anubis", 
    version="1.0.0",
    author="nmmapper",
    author_email="inquiry@nmmapper.com",
    description="Library used to discover and find subdomains of domains",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nmmapper/python3-anubis",
    project_urls={
        'Documentation': 'https://github.com/nmmapper/python3-anubis',
        'How it is used': 'https://github.com/nmmapper/python3-anubis',
        'Homepage': 'https://www.nmmapper.com/',
        'Source': 'https://github.com/nmmapper/python3-anubis',
        'Subdomain finder': 'https://www.nmmapper.com/sys/tools/subdomainfinder/',
        'theHarvester online': 'https://www.nmmapper.com/sys/theharvester/email-harvester-tool/online/',
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    setup_requires=['wheel'],
    install_requires=['requests','httpx', 'dnspython'],
)
