An advanced Python API wrapper for tidal music.

## Installation
### Using pip
The package can be installed in Python environments using package managers like pip.
```bat
pip install -U tidal
```
## Basic usage
First, register an app at the [Tidal dev dashboard](https://developer.tidal.com/dashboard) to obtain a client ID and secret
- Create a TidalClient instance passing in the client ID and secret
- The annotated datatypes returned can be accessed similarly to a dict
```python
import tidal
import os

client = tidal.TidalClient("my_client_id_here", "my_client_secret_here")
# .track("track_id", "country_code")
track = client.track("35079505", "GB")

print(f"Name: {track["title"]}\nURL:{track["tidalUrl"]}")
```
