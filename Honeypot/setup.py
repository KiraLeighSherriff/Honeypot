from setuptools import setup, find_packages

setup(
    name='honeypot',
    version='1.0', 
    description="honeypot for SSH, Telnet, FTP, HTTP",
    packages=find_packages(),
    author="kira Leigh Sherriff",
    install_requires=["Flask", 
                      "waitress", 
                      "mysql-connector",
                      "mysql-connector-python", 
                      "minetext", 
                      "paramiko"],
    python_requires=">=3.10",
    )

# File to find all modules in the source directory AKA find the with __init__.py 
# so they that the files can be access all thought the program

# pip install -e . command to run setup
