# Author: Scott Woods <scott.18.ansar@gmail.com.com>
# MIT License
#
# Copyright (c) 2017-2023 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Tools and runtime for asynchronous programming.

Repo: git@github.com:mr-ansar/ansar-connect.git
Branch: main
Commit: b9682f6a1b7d0fee0e0d257ef117744fab5958a2
Version: 0.1.77 (2024-03-07@16:48:39+NZDT)
"""

from ansar.create import *

#bind = bind_any
#create = create_object

from .socketry import HostPort, LocalPort
from .socketry import ScopeOfIP, local_private_public
from .socketry import Blob, CreateFrame
from .socketry import Listening, NotListening, Accepted, NotAccepted, StopListening
from .socketry import Connected, NotConnected
from .socketry import Close, Closed, Abandoned
from .transporting import listen, connect, stop_listen

from .plumbing import RETRY_LOCAL, RETRY_PRIVATE, RETRY_PUBLIC
from .plumbing import ip_retry

from .directory_if import ScopeOfService
from .directory_if import Published, NotPublished, Subscribed
from .directory_if import Available, NotAvailable, Delivered, NotDelivered
from .directory_if import Clear, Cleared, Dropped
from .directory_if import DirectoryEnquiry, DirectoryReconnect, DirectoryScope, DirectoryAncestry

from .directory import ServiceDirectory
from .directory import RouteByRelay, InboundByRelay, OpenLoop
from .directory import publish, subscribe
from .directory import clear, retract
from .directory import key_service

from .networking_if import UseAddress, NoAddress, GlareTimer
from .networking import ConnectToAddress, ListenAtAddress
from .networking import SubscribeToListing, PublishAListing
from .grouping import GroupTable, GroupUpdate, AddressGroup, GroupTimer, GroupObject

from .node import NodeSettings, node_settings
from .node import node_passing, sub_node_passing
from .node import create_node, NodeProperties

from .model import CONTACT_TYPE, CONTACT_DEVICE
from .model import EmailAddress, PhoneNumber
from .model import Login, PII
from .model import CloudAccount, AccountFrame, DirectoryDevice, AccountDeveloper, AccountOwner
from .model import AccountDirectory, DirectoryFrame, CloudAccess
from .model import CloudLookup, CloudRedirect, CloudAssignment, YourCloud
from .model import RelayLookup, RelayRedirect, RelayAssignment, YourRelay, CloseRelay

from .product import ProductLookup, YourProduct

from .foh import SignUp, ExportAccount
from .foh import AccountInformation
from .foh import ExportDevice, DeviceAccess
