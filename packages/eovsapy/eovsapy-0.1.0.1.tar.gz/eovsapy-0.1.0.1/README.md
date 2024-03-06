# EOVSAPY

![Latest Version](https://img.shields.io/pypi/v/eovsapy.svg)

EOVSAPY is a Python library dedicated to the processing and analysis of data from the Expanded Owens Valley Solar Array. For more details about the project, visit our [homepage](https://github.com/ovro-eovsa/eovsapy).

## Installation

### Prerequisites

Before installing EOVSAPY, ensure you have `pip` installed. For instructions, refer to the [pip installation guide](https://packaging.python.org/tutorials/installing-packages/).

### Installing EOVSAPY

EOVSAPY can be easily installed using pip. Run the following command:

```bash
pip install eovsapy
```

### Configuring Access to the Interim Database (IDB)

To process and calibrate EOVSA raw "Interim" Database (IDB) data, access to the SQL database containing the calibration data is required. Perform the following steps to configure access:

1. **Obtain Database Credentials**:
Contact sijie.yu@njit.edu to request the `<username>`, `<account_name>`, and `<password>` for database access.

2. **Create a `.netrc` File**:

   Create a `.netrc` file in your home directory (`$HOME`) with the following contents, replacing `<username>`, `<account_name>`, and `<password>` with the actual database credentials:

   ```bash
   machine eovsa-db0.cgb0fabhwkos.us-west-2.rds.amazonaws.com
           login <username>
           account <account_name>
           password <password>
   ```

3. **Secure the `.netrc` File**:

   To ensure that the file is only accessible by you, set its permissions to only allow owner read/write:

   ```bash
   chmod 0600 ~/.netrc
   ```