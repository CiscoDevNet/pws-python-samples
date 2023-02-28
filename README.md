# pws-python-samples

## Overview

These samples demonstrate use of the Presence Web Service REST API of Cisco Unified Communications Manager IM and Presence.

https://developer.cisco.com/site/im-and-presence/

The concepts and techniques shown can be extended to enable integration of IM&P presence functionality with third party applications.

## Available samples

* `device_presence_meeting.py` - Demonstrates application user login, end-user proxy login, and setting/device presence for a meeting service.

* `get_polled_rich_presence.py` - Demonstrates application user login, end-user proxy login, and retrieving rich presence information.

In addition a [Postman collection]() is available for experimenting with PWS - edit the collection **Variables** to configure the collection.

## Getting started

* Install Python 3

    On Windows, choose the option to add to PATH environment variable

* (Optional) Create/activate a Python virtual environment named `venv`:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

* Install needed dependency packages:

    ```bash
    pip install -r requirements.txt
    ```

* Rename `.env.example` to `.env`, and edit it to specify your CIMP address, application user credentials (requires CUCM 'Admin-3rd Party API' group access) and end user Id.

* To run a specific sample, in Visual Studio Code open the sample `.py` file you want to run, then press `F5`, or open the Debugging panel and click the green 'Launch' arrow

## Hints

* Response XML debug output can be enabled in `.env`

* **Requests Session** Creating and using a [requests Session](https://docs.python-requests.org/en/latest/user/advanced/) object allows setting global request parameters like `auth`/`verify`/`headers`.

    In addition, Session maintains a persistent HTTP connection to keep network latency and networking CPU usage lower on the client and CIMP.

