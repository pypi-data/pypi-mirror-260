<div align="center">

# ondemandutils

Utilities and APIs for orchestrating the Open Ondemand deployment lifecycle.

[![Matrix](https://img.shields.io/matrix/ubuntu-hpc%3Amatrix.org?logo=matrix&label=ubuntu-hpc)](https://matrix.to/#/#ubuntu-hpc:matrix.org)

</div>

## Features

`ondemandutils` is a collection of various utilities and APIs to make it easier 
for you and your friends to interface with Open OnDemand, especially if you 
are orchestrating the deployment of new Open OnDemand. Gone are the days of
seething over incomplete Jinja2 templates or misconfigured YAML documents. 
Current utilities and APIs shipped in the `ondemandutils` package include:

#### `from ondemandutils.editors import ...`

* `ood_portal`:  An editor _ood_portal.yml_ configuration files.
* `nginx_stage`: An editor for _nginx_stage.yml_ configuration files.

## Installation

#### Option 1: Install from PyPI

```shell
$ python3 -m pip install ondemandutils
```

#### Option 2: Install from source

We use the [Poetry](https://python-poetry.org) packaging and dependency manager to
manage this project. It must be installed on your system if installing `ondemandutils`
from source.

```shell
$ git clone https://github.com/charmed-hpc/ondemandutils.git
$ cd ondemandutils
$ poetry install
```

## Usage

### Editors

#### `ood_portal`

This module provides an API for editing _ood_portal.yml_ configuration files, 
creating them if they do not exist. Here's some common Open OnDemand
lifecycle management operations you can perform using this editor:

##### Edit a pre-existing _ood_portal.yml_ configuration file

```python
from ondemandutils.editors import ood_portal

# Open, edit, and save the ood_portal.yml file located at /etc/ood/config/ood_portal.yaml.
with ood_portal.edit("/etc/ood/config/ood_portal.yaml") as config:
    config.servername = "ondemand-testing"
    config.server_aliases = []
    config.ssl = None
    config.public_root = "/var/snap/ondemand/common/var/www/public"
    config.log_root = "/var/snap/ondemand/common/var/logs/ondemand"
    config.pun_stage_cmd = "sudo /snap/ondemand/current/nginx_stage/sbin/nginx_stage"
```

##### Add Dex configuration to the _ood_portal.yml_ configuration file

```python
from ondemandutils.editors import ood_portal
from ondemandutils.models import DexConfig

with ood_portal.edit("/etc/ood/config/ood_portal.yaml") as config:
    dex = DexConfig(
        http_port = 5556,
        tls_cert = "/var/snap/ondemand/common/tls.cert",
        tls_key = "/var/snap/ondemand/common/tls.secret",
    )
    config.dex = dex
```

#### `nginx_stage`

This module provides and API for editing _nginx_stage.yml_ configuration files, 
creating them if they do not exist. Here's some common nginx operations you can perform
on the _nginx_stage.yml_ configuration file using this editor:

##### Edit a pre-existing _nginx_stage.yml_ configuration file

```python
from ondemandutils.editors import nginx_stage

with nginx_stage.edit("/etc/ood/config/nginx_stage.yml") as config:
    config.pun_access_log_path = "/var/snap/ondemand/common/var/log/nginx/%{user}/access.log"
    config.pun_error_log_path = "/var/snap/ondemand/common/var/log/nginx/%{user}/error.log"
    config.passenger_ruby = "/snap/ondemand/common/usr/bin/ruby"
    config.passenger_nodejs = "/snap/ondemand/common/bin/node"
    config.passenger_root = "/snap/ondemand/current/opt/passenger/locations.ini"
    config.disable_bundle_user_config = False
    config.pun_custom_env_declarations = ["CPATH"]
```

## Project & Community

The `ondemandutils` package is a project of the 
[Ubuntu HPC](https://discourse.ubuntu.com/t/high-performance-computing-team/35988) community. 
It is an open-source project that is welcome to community involvement, contributions, suggestions, fixes, 
and constructive feedback. Interested in being involved with the development of `ondemandutils`? 
Check out these links below:

* [Join our online chat](https://matrix.to/#/#ubuntu-hpc:matrix.org)
* [Code of Conduct](https://ubuntu.com/community/code-of-conduct)
* [Contributing guidelines](./CONTRIBUTING.md)

## License

The `ondemandutils` package is free software, distributed under the GNU Lesser General Public License, v3.0.
See the [LICENSE](./LICENSE) file for more information.
