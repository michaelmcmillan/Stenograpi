# [![Stenograpi](docs/img/header.png)](https://github.com/michaelmcmillan/Stenograpi)

> Document your HTTP API automatically through tests.

[![Build Status](https://travis-ci.org/michaelmcmillan/Stenograpi.svg?branch=master)](https://travis-ci.org/michaelmcmillan/Stenograpi)
[![Coverage Status](https://coveralls.io/repos/github/michaelmcmillan/Stenograpi/badge.svg?branch=master)](https://coveralls.io/github/michaelmcmillan/Stenograpi?branch=master)

Stop worrying about keeping your documentation in sync with your HTTP API. Simply proxy your integration tests through Stenograpi and receive documentation on the other end.

## Install
Stenograpi is a standalone Python script that has no external dependencies. Simply run the following command to retrieve the script.

````
wget https://raw.githubusercontent.com/michaelmcmillan/Stenograpi/master/dist/stenograpi.py
````

## Usage

Start Stenograpi by running the script from your command line.

````
python3 stenograpi.py localhost 1337 localhost 1338
````

In your integrated tests, replace the hostname and port of the application you are testing with Stenograpi's hostname and port.

## Mechanics

Stenograpi steps in between your tests and your application. However, neither your tests nor your application will notice any difference. 

![Request flow](docs/img/flow.png)

While the requests and responses are delivered as usual, Stenograpi will create Markdown documents describing the exchange. The documents are written with developers in mind,
[see for yourself](docs/examples/output.md).
