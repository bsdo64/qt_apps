# -*- coding: utf-8 -*-

# Resource object code
#
# Created by: The Resource Compiler for PyQt5 (Qt v5.10.1)
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore

qt_resource_data = b"\
\x00\x00\x01\x28\
\x00\
\x00\xbb\xd3\x78\x9c\xed\xd5\x31\x0a\x02\x31\x00\x45\xc1\x3e\xa7\
\xd8\xe3\xe4\x20\xda\x05\x16\x6c\xbc\xbe\xa5\xad\x88\xac\x79\x30\
\xdd\x32\x4d\x42\x96\xc7\x9f\xf7\xb5\xce\xe3\x79\x3e\xd6\xed\x98\
\xef\xef\x79\x0d\x8f\xeb\x8f\xc4\xf8\x47\x3c\xc6\x7f\xef\xb2\xd1\
\xf1\xfb\xfc\x14\x8c\x6b\xf1\xee\xf3\x2a\x18\xef\xcf\xda\xc1\x5d\
\xb6\x3c\x18\x37\x59\x3b\xb8\xcb\x96\x07\xe3\x26\x6b\x07\x77\xd9\
\xf2\x60\xdc\x64\xed\xe0\x2e\x5b\x1e\x8c\x9b\xac\x1d\xdc\x65\xcb\
\x83\x71\x93\xb5\x83\xbb\x6c\x79\x30\x6e\xb2\x76\x70\x97\x2d\x0f\
\xc6\x4d\xd6\x0e\xee\xb2\xe5\xc1\xb8\xc9\xda\xc1\x5d\xb6\x3c\x18\
\x37\x59\x3b\xb8\xcb\x96\x07\xe3\x26\x6b\x07\x77\xd9\xf2\x60\xdc\
\x64\xed\xe0\x2e\x5b\x1e\x8c\x9b\xac\x1d\xdc\x65\xcb\x83\x71\x93\
\xb5\x83\xbb\x6c\x79\x30\x6e\xb2\x76\x70\x97\x2d\x0f\xc6\x4d\xd6\
\x0e\xee\xb2\xe5\xc1\xb8\xc9\xda\xc1\x5d\xb6\x3c\x18\x37\x59\x3b\
\xb8\xcb\x96\x07\xe3\x26\x6b\x07\x77\xd9\xf2\x60\xdc\x64\xed\xe0\
\x2e\x5b\x1e\x8c\x9b\xac\x1d\xdc\x65\xcb\x83\x71\x93\xb5\x83\xbb\
\x6c\x79\x30\x6e\xb2\x76\x70\x97\x2d\x0f\xc6\x4d\xd6\x0e\xee\xb2\
\xe5\xc1\xb8\xc9\xda\xc1\x5d\xb6\x3c\x18\x37\x59\x3b\xb8\xcb\x96\
\x07\xe3\x26\x6b\x07\x77\xd9\xf2\x60\xfc\x75\x3d\x5b\xde\x0a\xe3\
\x4f\xf8\x05\x56\x37\x19\x2d\
"

qt_resource_name = b"\
\x00\x04\
\x00\x06\xd0\x25\
\x00\x66\
\x00\x69\x00\x6c\x00\x65\
\x00\x09\
\x07\xc7\xbb\x54\
\x00\x69\
\x00\x6e\x00\x70\x00\x75\x00\x74\x00\x2e\x00\x74\x00\x78\x00\x74\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x0e\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x0e\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x63\xda\x20\xea\xe1\
"

qt_version = QtCore.qVersion().split('.')
if qt_version < ['5', '8', '0']:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2

def qInitResources():
    QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()