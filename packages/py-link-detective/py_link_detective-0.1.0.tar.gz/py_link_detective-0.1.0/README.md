<div align="center">
<pre align="center">
<h2 align="center">
;; Python-Link-Detective ;;
</h2>
<h4 align="center">A simple implementation of a dead link detection tool using python httpx & asyncio library</h4>
</pre>
</div>

## Installation
```sh
pip install py-link-detective
```

## Quick-start

## Usage
```sh
py-link-detective -h
```

```text
usage: py-link-detective [-h] [--version] [-n N] (-c | -j) url

Detective: A simple link checker for websites

positional arguments:
  url            The url of the website to be checked

options:
  -h, --help     show this help message and exit
  --version, -v  show program's version number and exit
  -n N           number of concurrent request at a time
  -c             use console for output
  -j             use a json file(in the current path) for output
```

## Test

```sh
pytest -vv
```
