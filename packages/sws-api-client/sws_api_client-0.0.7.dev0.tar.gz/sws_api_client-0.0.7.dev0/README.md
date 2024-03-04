# SWS API Client

This library provides the user with a set of useful tools to easily interact with the FAO SWS (Statistical Working System) REST APIs.

## Installation

The module is available on Pypi:

```bash
python -m pip install sws_api_client
```

The library requires Python 3.11+.

## Usage

To use the package the user needs to create an instance of the SwsApiClient class, provide it with the necessary parameters and execute the methods to query the specific endpoints.  

### Instantiate the client locally

There are three methods to instantiate the client:

#### 1. Pass the `sws_endpoint` and the `access_token` to the constructor

```python
from sws_api_client import SwsApiClient

sws_client = SwsApiClient(sws_endpoint="<sws_endpoint>", access_token="<access_token>")
```

#### 2. Pass to `sws_endpoint` and the `access_token` as named arguments

We need to execute the script from command line passing `--sws_endpoint` and `--access_token` as arguments:

```bash
python script.py --sws_endpoint <endpoint> --access_token <test_access_token>
```

And instantiate the client in our script with the class method `from_args`:

```python
from sws_api_client import SwsApiClient

sws_client = SwsApiClient.from_args()
```

#### 3. Create a conf file where to store the arguments

We need to create a conf file (default name: `"conf_sws_api_client.json"`) with the following structure:

```json
{
    "sws_endpoint": "<sws_endpoint>",
    "access_token": "<access_token>"
}
```

And instantiate the client in our script with the class method `from_conf`:

```python
from sws_api_client import SwsApiClient

sws_client = SwsApiClient.from_conf(conf_file="<conf_file_path>")

# Or, if the conf_file is named "conf_sws_api_client.json" and is in the current working directory

sws_client = SwsApiClient.from_conf()
```

### Instantiate the client in a SWS plugin

When working withing a SWS plugin instantiate the client as:

```python
from sws_api_client import SwsApiClient

sws_client = SwsApiClient.from_env()
```

### Perform requests

To perform requests you just need to call the available methods using the SwsApiClient object, as an example:

```python
dataset_details = sws_client.get_dataset_export_details(dataset_id="<dataset_id>")
```
