Subfork Python API
==================

Subfork is the easiest way to build and deploy static sites and micro web apps.
This package provides the Subfork Python API and command line interface.

## Installation

The easiest way to install:

```shell
$ pip install subfork
```

Requires Python 3.6+.

In order to authenticate with the Subfork API, you will first need to create
a site and API access keys for your site at [subfork.com](https://subfork.com).

## Quick Start

To use the Subfork Python API you must first complete the configuration steps
below. Then instantiate a client using the site domain and access keys:

```python
sf = subfork.get_client()
```

## Configuration

Using the Subfork Python API requires basic authentication. To use
environment variables, set the following:

```shell
$ export SUBFORK_DOMAIN=<site domain>
$ export SUBFORK_ACCESS_KEY=<access key>
$ export SUBFORK_SECRET_KEY=<secret key>
```

To use a [template file](/#template), create a `subfork.yml` at the root of your project and make required updates, or set `$SUBFORK_CONFIG_FILE` to the path to `subfork.yml`:

```shell
$ export SUBFORK_CONFIG_FILE=/path/to/subfork.yml
```

## Basic Commands

To create a site template file from existing html and static files:

```shell
$ subfork create -t templates -s static
```

Be sure to update the values in the new `subfork.yml` if necessary.

To test the site using the dev server:

```shell
$ subfork run
```

To deploy and release a site:

```shell
$ subfork deploy -c "initial deployment" --release
```

To process queued tasks:

```shell
$ subfork worker
```

## Templates

The `subfork.yml` template file is a config file that contains required auth info,
page templates, routes (or endpoints), static files and task workers.

For example, this template contains two routes and a worker:

```yaml
# enter verified site domain here
domain: ${SUBFORK_DOMAIN}

# enter site credentials here
access_key: ${SUBFORK_ACCESS_KEY}
secret_key: ${SUBFORK_SECRET_KEY}

# path to folder containing template files
# template_folder: templates

# path to static file folder
# static_folder: static

# page template definitions
templates:
  index:
    route: /
    file: index.html
  user:
    route: /user/<username>
    file: user.html

# task worker definitions
workers:
  test:
    queue: test
    function: subfork.worker.test
```
