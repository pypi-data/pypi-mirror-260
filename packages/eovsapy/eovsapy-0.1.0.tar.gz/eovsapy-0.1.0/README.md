# EOVSAPY
![Latest Version](https://img.shields.io/pypi/v/eovsapy.svg)

Python code and files for Expanded Owens Valley Solar Array. Our homepage [EOVSAPY](https://github.com/ovro-eovsa/eovsapy) has more information about the project.

## Installation
The recommended way to install EOVSAPY is with [pip](https://packaging.python.org/tutorials/installing-packages/).
Once pip is installed, run the following command:

```bash
$ pip install eovsapy
```
To process and calibrate EOVSA raw "Interim" Database (IDB) data, users will require access to the EOVSA SQL database that holds the calibration data. To facilitate this, it's necessary to create a ~/.netrc file containing the following details:
```bash
machine eovsa-db0.cgb0fabhwkos.us-west-2.rds.amazonaws.com
        login Python3
        account eOVSA
        password Py+h0nUser
```
After that, restrict access to only the owner for the netrc file using 
```bash
chmod 0600 ~/.netrc
```
