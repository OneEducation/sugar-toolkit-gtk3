# Copyright (C) 2007, Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import dbus
import dbus.service

from sugar.objects.objecttype import ObjectType

_REGISTRY_IFACE = "org.laptop.ObjectTypeRegistry"
_REGISTRY_PATH = "/org/laptop/ObjectTypeRegistry"

class ObjectTypeRegistry(dbus.service.Object):
    def __init__(self):
        bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(self._REGISTRY_IFACE, bus=bus)
        dbus.service.Object.__init__(self, bus_name, self._REGISTRY_PATH)

        self._types = {}

        self._add_primitive('Text', _('Text'), 'object-text',
                            [ 'text/rtf' ])
        self._add_primitive('Image', _('Image'), 'object-image',
                            [ 'image/png' ])

    def _add_primitive(self, type_id, name, icon, mime_types):
        object_type = ObjectType(type_id, name, icon, mime_types)
        self._types.add(object_type)

    def _get_type_for_mime(self, mime_type):
        for object_type in self._types.values():
            if mime_type in object_type.mime_types:
                return object_type

    @dbus.service.method(_CLIPBOARD_DBUS_INTERFACE,
                         in_signature="s", out_signature="a{sv}")
    def GetType(self, type_id):
        if self._types.has_key(type_id):
            return self._types[type_id].to_dict()
        else:
            return []

    @dbus.service.method(_CLIPBOARD_DBUS_INTERFACE,
                         in_signature="s", out_signature="a{sv}")
    def GetTypeForMIME(self, mime_type):
        object_type = self._get_type_for_mime(mime_type)
        if object_type:
            return object_type.to_dict()
        else:
            return []