# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2010 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import socket
import string
import time
import datetime
try:
    from hashlib import sha1
except ImportError:
    from sha import sha as sha1
import hmac
import re
import sys

# forban internal junk
sys.path.append('.')
import fid

class message:

    def __init__(self,name="notset", uuid=None, port="12555", timestamp=None,
    auth=None, destination=["ff02::1","255.255.255.255", ]):
            
            self.name       = name
            self.uuid       = uuid
            self.port       = port
            self.count      = 0
            self.destination = destination

    def gen (self):
            self.payload    = "forban;name;" + self.name + ";"
            myid = fid.manage()
            self.payload    = self.payload + "uuid;" + myid.get()

# the HMAC value is currently useless as the URL is built on
# on the source address of the packet. TBU

    def auth(self,key=None):

        if key is None:
            self.payload = self.payload
        else:
            auth = hmac.new(key, self.payload, sha1)
            self.payload = self.payload + ";hmac;" + auth.hexdigest()

    def get (self):
            return self.payload

    def send(self):
        for destination in self.destination:
           
            if socket.has_ipv6 and re.search(":", destination):
                sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                # Required on some version of MacOS X while sending IPv6 UDP
                # datagram
                sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
           
            try:
                sock.sendto(self.payload, (destination, int(self.port)))
            except socket.error, msg:
                continue
        sock.close()



def managetest():
   
    msg = message()
    msg.gen()
    msg.auth()
    print msg.get()
    msg.send()
    msg.auth("forbankey")
    print msg.get()

if __name__ == "__main__":
                                       
    managetest()

