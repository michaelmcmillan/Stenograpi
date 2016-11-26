# [![Stenograpi](docs/img/header.png)](https://github.com/michaelmcmillan/Stenograpi)

> Document your HTTP API automatically through tests.

[![Build Status](https://travis-ci.org/michaelmcmillan/Stenograpi.svg?branch=master)](https://travis-ci.org/michaelmcmillan/Stenograpi)

Stop worrying about keeping your documentation in sync with your HTTP API. Simply proxy your integration tests through Stenograpi and receive documentation on the other end.

## Install
Stenograpi is a standalone Python script that has no external dependencies. Simply run the following command to retrieve the script.

````
wget https://github.com/michaelmcmillan/Stenograpi/blob/master/dist/stenograpi.py
````

## Usage

Start Stenograpi by running the script from your command line.

````
python3 stenograpi.py --hostname localhost --port 1337 --app-hostname localhost --app-port 1338
````

In your integrated tests, replace the hostname and port of the application you are testing with Stepograpi's hostname and port.