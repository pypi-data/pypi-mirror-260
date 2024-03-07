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

from .socketry import *

__all__ = [
	'ANSAR_DIRECTORY_PORT',
	'ANSAR_PRODUCT_PORT',
	'ANSAR_LOCAL_ADDRESS',
	'ANSAR_LAN_ADDRESS',
	'ANSAR_LOCAL_DIRECTORY',
	'ANSAR_LOCAL_PRODUCT',
	'ANSAR_LAN_DIRECTORY',
	'ANSAR_LAN_PRODUCT',
]

ANSAR_DIRECTORY_PORT = 32176
ANSAR_PRODUCT_PORT = ANSAR_DIRECTORY_PORT + 1
ANSAR_LOCAL_ADDRESS = '127.0.0.1'
ANSAR_LAN_ADDRESS = '192.168.1.176'

ANSAR_LOCAL_DIRECTORY = HostPort(ANSAR_LOCAL_ADDRESS, ANSAR_DIRECTORY_PORT)
ANSAR_LOCAL_PRODUCT = HostPort(ANSAR_LOCAL_ADDRESS, ANSAR_PRODUCT_PORT)
ANSAR_LAN_DIRECTORY = HostPort(ANSAR_LAN_ADDRESS, ANSAR_DIRECTORY_PORT)
ANSAR_LAN_PRODUCT = HostPort(ANSAR_LAN_ADDRESS, ANSAR_PRODUCT_PORT)
