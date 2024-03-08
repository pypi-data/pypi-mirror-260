[![PyPI](https://img.shields.io/pypi/v/odmfclient?logo=pypi)](https://pypi.org/project/odmfclient/)
[![GitHub](https://img.shields.io/github/license/jlu-ilr-hydro/odmfclient?logo=github)](https://github.com/jlu-ilr-hydro/odmfclient)
[![GitHub last commit](https://img.shields.io/github/last-commit/jlu-ilr-hydro/odmfclient?logo=github)](https://github.com/jlu-ilr-hydro/odmfclient)

# API client for ODMF

This package allows programatic access to [ODMF](https://github.com/jlu-ilr-hydro/odmf) databases with Python. 
It is based on [requests](https://pypi.org/project/requests/). 

The code is found on  [Github](https://github.com/jlu-ilr-hydro/odmfclient/) under a free license ![GitHub](https://img.shields.io/github/license/jlu-ilr-hydro/odmfclient?logo=github).

## Installation

From PyPI (current version): [![PyPI](https://img.shields.io/pypi/v/odmfclient?logo=pypi)](https://pypi.org/project/odmfclient/) using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/)

    pip install odmfclient

In an IPython console (eg in Spyder) you can use the same command with 

    %pip install odmfclient

To install the newest version from github do:

   pip install https://github.com/jlu-ilr-hydro/odmfclient/archive/main.zip

For other branches then `main` use the above command as `.../archive/<branch>.zip` 

## Usage

### Direct access to ODMF

~~~~~~~~~~py
from odmfclient import login
with login('https://path/to/odmf', 'user', 'password') as api:
    print(api)
    # Get all datasets at site #1 with valuetype 1
    datasets = api.dataset.list(site=1, valuetype=1)
    # Get values for the first dataset found as pandas.DataFrame
    df = api.dataset.values_parquet(dsid=datasets[0])
    # Upload some content to a file in the ODMF-file manager
    api.upload(b'Some binary content, usually what you load from a file', targetpath='path/to/file', overwrite=True)
~~~~~~~~~~

### Access ODMF behind an reverse proxy requiring authentification

At JLU, we are protecting our ODMF instances behind a reverse proxy 
(Apache) requiring basic authentification for access from outside the
universities network using shared credentials. Of course, any other authentification at your reverse proxy with 
a requests method is possible. To access such an instance, where the shared credentials for basic authentification is
`basic-user` and `basic-password`:

~~~~~~~~~~py
from odmfclient import login
from requests.auth import HTTPBasicAuth

basic_auth = HTTPBasicAuth('basic-user', 'basic-password')

with login('https://path/to/odmf', 'user', 'password', session_auth=basic_auth) as api:
    print(api)
    # Get all datasets at site #1 with valuetype 1
    datasets = api.dataset.list(site=1, valuetype=1)
    # Get values for the first dataset found as pandas.DataFrame
    df = api.dataset.values_parquet(dsid=datasets[0])
~~~~~~~~~~
