"""device_presence_meeting.py

Demonstrates application user login, end-user proxy login, and setting/clearing
device presence for a meeting service.

Copyright (c) 2023 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import requests
import sys
import urllib3
from lxml import etree

# Edit .env file to specify your CIMP host/admin/end-user details
import os
from dotenv import load_dotenv
load_dotenv()

# Change to true to enable output of request/response headers and XML
DEBUG = os.getenv('DEBUG') == 'True'

serviceUrl = f'https://{ os.getenv( "CIMP_ADDRESS" ) }:8083/presence-service'
xmppDomain = os.getenv( 'CIMP_XMPP_DOMAIN' )
appUser = os.getenv( 'CIMP_APPUSER' )
endUser = os.getenv( 'CIMP_ENDUSER' )

# The first step is to create a HTTP requests session
session = requests.Session()

# We avoid certificate verification by default
# And disable insecure request warnings to keep the output clear
session.verify = False
urllib3.disable_warnings( urllib3.exceptions.InsecureRequestWarning )

# This trick disables insecure request warnings, when not verifying certs
requests.packages.urllib3.disable_warnings( )

# To enable SSL cert checking (recommended for production)
# place the CIMP Tomcat certificate .pem file in the root of the project
# and uncomment the line below

# session.verify = 'changeme.pem'
# session.verify = 'sjds-cimp14.cisco.com-ECDSA.pem'

session.headers = { 
    'Content-Type': 'application/xml',
    'Accept': 'application/xml'
}

# Login the application user

body = (
f'''<session>
        <password>{ os.getenv( "CIMP_APPUSER_PASSWORD" ) }</password>
    </session>'''
)

try:
    resp = session.post( f'{ serviceUrl }/users/{ appUser }/sessions', data = body )
    resp.raise_for_status()
except Exception as err:
    print( f'\nError logging in application user: { err }' )
    sys.exit( 1 )

# Use the lxml ElementTree object to parse the response XML
message = etree.fromstring( resp.content )
appUserSessionKey = message.find( 'sessionKey').text

if DEBUG:
    print( '\n', etree.tostring( message, pretty_print = True, encoding = 'unicode' ) ) 

print( '\nApplication User login: SUCCESS\n' )

# Login the end user (forced)

try:
    resp = session.put( f'{ serviceUrl }/users/{ endUser }/session', headers = { 'Presence-Session-Key': appUserSessionKey } )
    resp.raise_for_status()
except Exception as err:
    print( f'\nError logging in end user: { err }' )
    sys.exit( 1 )

# Use the lxml ElementTree object to parse the response XML
message = etree.fromstring( resp.content )
endUserSessionKey = message.find( 'sessionKey').text

if DEBUG:
    print( '\n', etree.tostring( message, pretty_print = True, encoding = 'unicode' ) ) 

print( '\nEnd User login: SUCCESS\n' )

input( 'Press Enter to continue...' )

# Set device-level meeting presence for a 'foo-meeting' service to <busy><meeting>

setPresenceHeaders = {
    'Presence-Session-Key': endUserSessionKey,
    'Presence-Override': 'false',
    'Presence-Expiry': '86400'
}

body = (
f'''<presence entity="sip:{ endUser }@{ xmppDomain }">
    <person id="{ endUser }">
        <activities>
            <busy/>
            <meeting/>
        </activities>
    </person>
    <tuple id="foo-meeting">
        <source xmlns="urn:cisco:params:xml:ns:pidf:source">Presence Web Service</source>
        <servcaps>
            <text>true</text>
        </servcaps>
        <status>
            <basic>open</basic>
        </status>
    </tuple>
</presence>'''
)

try:
    resp = session.put( f'{ serviceUrl }/users/{ endUser }/presence/rich', data = body, headers = setPresenceHeaders )
    resp.raise_for_status()
except Exception as err:
    print( f'\nError setting presence to <busy><meeting>: { err }' )
    sys.exit( 1 )

print( '\nSet presence to <busy><meeting>: SUCCESS\n' )

input( 'Press Enter to continue...' )

# Set device-level meeting presence for a 'foo-meeting' service to <available>

body = (
f'''<presence entity="sip:{ endUser }@{ xmppDomain }">
    <person id="{ endUser }">
        <activities>
            <available/>
        </activities>
    </person>
    <tuple id="foo-meeting">
        <source xmlns="urn:cisco:params:xml:ns:pidf:source">Presence Web Service</source>
        <servcaps>
            <text>true</text>
        </servcaps>
        <status>
            <basic>open</basic>
        </status>
    </tuple>
</presence>'''
)

try:
    resp = session.put( f'{ serviceUrl }/users/{ endUser }/presence/rich', data = body, headers = setPresenceHeaders )
    resp.raise_for_status()
except Exception as err:
    print( f'\nError setting presence to <available>: { err }' )
    sys.exit( 1 )

print( '\nSet presence to <available>: SUCCESS\n' )

# Logout the end user

try:
    resp = session.delete( f'{ serviceUrl }/users/{ endUser }/session', headers = { 'Presence-Session-Key': endUserSessionKey } )
    resp.raise_for_status()
except Exception as err:
    print( f'\nError logging out end user: { err }' )
    sys.exit( 1 )

print( '\nEnd User logout: SUCCESS\n' )

# Logout the application user

try:
    resp = session.delete( f'{ serviceUrl }/users/{ appUser }/session', headers = { 'Presence-Session-Key': appUserSessionKey } )
    resp.raise_for_status()
except Exception as err:
    print( f'\nError logging out application user: { err }' )
    sys.exit( 1 )

print( '\nApplication User logout: SUCCESS\n' )

