# Author: Scott Woods <scott.18.ansar@gmail.com.com>
# MIT License
#
# Copyright (c) 2022, 2023 Scott Woods
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

""".

.
"""
__docformat__ = 'restructuredtext'

__all__ = [
	'DirectorySettings',
	'procedure_blank',
	'procedure_directory',
]

import sys
import os
import stat
import signal
import errno
import datetime
import calendar
import tempfile
import uuid
import re
import ansar.create as ar
from ansar.create.procedure import DEFAULT_HOME, DEFAULT_GROUP, HOME, GROUP
from ansar.create.procedure import open_home, open_role, role_status
from .directory_if import *


# Per-command arguments as required.
# e.g. command-line parameters specific to create.
class DirectorySettings(object):
	def __init__(self, group_name=None, home_path=None, directory_enquiry=None, directory_connect=None, connect_file=None):
		self.group_name = group_name
		self.home_path = home_path
		self.directory_enquiry = directory_enquiry
		self.directory_connect = directory_connect
		self.connect_file = connect_file

DIRECTORY_SETTINGS_SCHEMA = {
	'group_name': ar.Unicode(),
	'home_path': ar.Unicode(),
	'directory_enquiry': ScopeOfService,
	'directory_connect': ScopeOfService,
	'connect_file': ar.Unicode(),
}

ar.bind(DirectorySettings, object_schema=DIRECTORY_SETTINGS_SCHEMA)

#
#
def procedure_blank(self, blank):
	return None

#
#
def procedure_directory(self, directory, group, home):
	group = ar.word_argument_2(group, directory.group_name, DEFAULT_GROUP, GROUP)
	home = ar.word_argument_2(home, directory.home_path, DEFAULT_HOME, HOME)

	if '.' in group:
		e = ar.Rejected(group_name=(group, f'no-dots name'))
		raise ar.Incomplete(e)
	group_role = f'group.{group}'

	hb = open_home(home)

	_, running = role_status(self, hb, [group_role])
	if running:
		e = ar.Failed(group_start=(f'group "{group}" is already running', None))
		raise ar.Incomplete(e)

	settings = []
	if directory.directory_enquiry:		# Inspect directory up to explicit level.
		s = ScopeOfService.to_name(directory.directory_enquiry)
		settings.append(f'--directory-enquiry={s}')

	elif directory.directory_connect:	# Assignment of new connection.
		if not directory.connect_file:
			e = ar.Rejected(connect_with_no_file=('missing connection details', None))
			raise ar.Incomplete(e)
		s = ScopeOfService.to_name(directory.directory_connect)
		p = os.path.abspath(directory.connect_file)
		settings.append(f'--directory-connect={s}')
		settings.append(f'--connect-file={p}')

	else:	# Default full-scope inspection.
		s = ScopeOfService.to_name(ScopeOfService.WAN)
		settings.append(f'--directory-enquiry={s}')

	try:
		a = self.create(ar.Process, 'ansar-group',	
					origin=ar.POINT_OF_ORIGIN.RUN_ORIGIN,
					home_path=hb.home_path, role_name=group_role, subrole=False,
					settings=settings)

		# Wait for Ack from new process to verify that
		# framework is operational.
		m = self.select(ar.Completed, ar.Stop)
		if isinstance(m, ar.Stop):
			# Honor the slim chance of a control-c before
			# the framework can respond.
			self.send(m, a)
			m = self.select(ar.Completed)

		# Process.
		def ipp_text(ipp):
			s = f'{ipp.host}:{ipp.port}'
			return s

		def lfa_text(lfa):
			s = f'{lfa[0]}/{lfa[1]}/{lfa[2]}'
			return s

		value = m.value
		if isinstance(value, ar.Ack):	   # New instance established itself.
			pass
		elif isinstance(value, DirectoryAncestry):
			for d in reversed(value.lineage):
				scope = ScopeOfService.to_name(d.scope) if d.scope else '?'
				ipp = ipp_text(d.connecting_ipp) if d.connecting_ipp.host else 'DISABLED'
				method = d.method if d.connecting_ipp.host else '-'
				started = ar.world_to_text(d.started) if d.started else '-'
				connected = ar.world_to_text(d.connected) if d.connected else '-'
				sc = f'{started}'
				lfa = lfa_text(d.lfa)
				ar.output_line(f'{scope:6} {ipp:20} {method:26} {sc:26} {lfa}')
		elif isinstance(value, DirectoryReconnect):
			return value
		elif isinstance(value, ar.Faulted):
			raise ar.Incomplete(value)
		elif isinstance(value, ar.LockedOut):
			e = ar.Failed(role_lock=(None, f'"{group_role}" already running as <{value.pid}>'))
			raise ar.Incomplete(e)
		else:
			e = ar.Failed(role_execute=(value, f'unexpected response from "{group_role}" (ansar-group)'))
			raise ar.Incomplete(e)
	finally:
		pass

	return None
