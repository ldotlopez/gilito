# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Luis López <luis@cuarentaydos.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.


from datetime import datetime


def as_float(value):
    if isinstance(value, float):
        return value

    return float(value.replace(",", "."))


def as_datetime(value, fmt):
    if isinstance(value, datetime):
        return value
    return datetime.strptime(value, "%d/%m/%Y")


def as_currency(value):
    iso_4217 = {"€": "EUR"}
    if value not in iso_4217:
        return value

    return iso_4217[value]
