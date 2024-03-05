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
__docformat__ = 'restructuredtext'

import ansar.create as ar
from .socketry import *

__all__ = [
	'ScopeOfService',
	'Published',
	'NotPublished',
	'Subscribed',
	'Available',
	'NotAvailable',
	'Delivered',
	'NotDelivered',
	'Clear',
	'Cleared',
	'Dropped',
	'DirectoryEnquiry',
	'DirectoryReconnect',
	'DirectoryScope',
	'DirectoryAncestry',
]

# Build the local published/subscribed objects.
#
ScopeOfService = ar.Enumeration(PROCESS=1, GROUP=2, HOST=3, LAN=4, WAN=5)

#
#
class Published(object):
	def __init__(self, published_name=None, declared_scope=ScopeOfService.WAN, listening_ipp=None):
		self.published_name = published_name
		self.declared_scope = declared_scope
		self.listening_ipp = listening_ipp or HostPort()

class NotPublished(object):
	def __init__(self, requested_name=None, reason=None):
		self.requested_name = requested_name
		self.reason = reason

class Subscribed(object):
	def __init__(self, subscribed_search=None, declared_scope=ScopeOfService.WAN):
		self.subscribed_search = subscribed_search
		self.declared_scope = declared_scope

# The actual service directory with listings and searches.
#

# Session messages to publish/listen controllers.
# Subscribe/client/calling/outbound end.
class Available(object):
	def __init__(self, key=None, agent_address=None):
		self.key = key
		self.agent_address = agent_address

class NotAvailable(object):
	def __init__(self, key=None, reason=None, agent_address=None):
		self.key = key
		self.reason = reason
		self.agent_address = agent_address

# Publish/service/answering/inbound end.
class Delivered(object):
	def __init__(self, key=None, agent_address=None):
		self.key = key
		self.agent_address = agent_address

class NotDelivered(object):
	def __init__(self, published_name=None, remote_address=None):
		self.published_name = published_name
		self.remote_address = remote_address

class Clear(object):
	def __init__(self, session=None, value=None):
		self.session = session
		self.value = value

class Cleared(object):
	def __init__(self, value=None):
		self.value = value

class Dropped(object):
	def __init__(self, reason=None):
		self.reason = reason

ENDING_SCHEMA = {
	'session': ar.Any,
	'value': ar.Any,
	'reason': str,
}

ar.bind(Clear, object_schema=ENDING_SCHEMA, copy_before_sending=False)
ar.bind(Cleared, object_schema=ENDING_SCHEMA, copy_before_sending=False)
ar.bind(Dropped, object_schema=ENDING_SCHEMA, copy_before_sending=False)

SHARED_SCHEMA = {
	#'key': ar.VectorOf(ar.Integer8()),
	'key': str,
	'name': str,
	'requested_name': str,
	'requested_search': str,
	'published_name': str,
	'subscribed_search': str,
	'published_name': str,
	'remote_address': ar.Address(),
	'session_address': ar.Address(),
	'declared_scope': ScopeOfService,
	'service_scope': ScopeOfService,
	'reason': ar.String(),
	'listening_ipp': ar.UserDefined(HostPort),
	'connecting_ipp': ar.UserDefined(HostPort),
	'parent_ipp': ar.UserDefined(HostPort),
	'child_ipp': ar.UserDefined(HostPort),
	'subscription': ar.UserDefined(Subscribed),
	'agent_address': ar.Address(),
	'address': ar.Address(),
}

ar.bind(Subscribed, object_schema=SHARED_SCHEMA)
ar.bind(Published, object_schema=SHARED_SCHEMA)
ar.bind(Available, object_schema=SHARED_SCHEMA)
ar.bind(NotAvailable, object_schema=SHARED_SCHEMA)
ar.bind(Delivered, object_schema=SHARED_SCHEMA)
ar.bind(NotDelivered, object_schema=SHARED_SCHEMA)

#
#
class DirectoryScope(object):
	def __init__(self, scope=None, connecting_ipp=None, method=None, started=None, connected=None, lfa=None):
		self.scope = scope
		self.connecting_ipp = connecting_ipp or HostPort()
		self.method = method
		self.started = started
		self.connected = connected
		self.lfa = lfa or [0, 0, 0]

DIRECTORY_SCOPE_SCHEMA = {
	'scope' : ScopeOfService,
	'connecting_ipp': ar.UserDefined(HostPort),
	'method': ar.Unicode(),
	'started': ar.WorldTime(),
	'connected': ar.WorldTime(),
	'lfa': ar.ArrayOf(ar.Integer8(), 3),
}

ar.bind(DirectoryScope, object_schema=DIRECTORY_SCOPE_SCHEMA)

#
#
class DirectoryEnquiry(object):
	def __init__(self, scope=None, lineage=None):
		self.scope = scope
		self.lineage = lineage or ar.default_vector()

DIRECTORY_ENQUIRY_SCHEMA = {
	'scope': ScopeOfService,
	'lineage': ar.VectorOf(DirectoryScope),
}

ar.bind(DirectoryEnquiry, object_schema=DIRECTORY_ENQUIRY_SCHEMA)

#
#
class DirectoryReconnect(object):
	def __init__(self, scope=None, connect_above=None):
		self.scope = scope
		self.connect_above = connect_above

DIRECTORY_RECONNECT_SCHEMA = {
	'scope': ScopeOfService,
	'connect_above': ar.Any(),
}

ar.bind(DirectoryReconnect, object_schema=DIRECTORY_RECONNECT_SCHEMA)

#
#
class DirectoryAncestry(object):
	def __init__(self, lineage=None):
		self.lineage = lineage or ar.default_vector()

DIRECTORY_ANCESTRY_SCHEMA = {
	'lineage': ar.VectorOf(DirectoryScope),
}

ar.bind(DirectoryAncestry, object_schema=DIRECTORY_ANCESTRY_SCHEMA)
