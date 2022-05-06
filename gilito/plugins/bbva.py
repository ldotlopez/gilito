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


import logging
import os
import subprocess
import tempfile
from typing import List, Any
from gilito.typetools import as_currency, as_datetime, as_float

from gilito import UnmappedData, Transaction
from gilito.plugins import Mapper, Loader
from gilito.helpers.spreadsheet import spreadsheet_as_csv
from gilito.helpers.csv import load_csv

LOGGER = logging.getLogger(__name__)

FIELD_CONCEPTO = "Concepto"
FIELD_DISPONIBLE = "Disponible"
FIELD_F_VALOR = "F.Valor"
FIELD_FECHA = "Fecha"
FIELD_IMPORTE = "Importe"
FIELD_MOVIMIENTO = "Movimiento"
FIELD_OBSERVACIONES = "Observaciones"
FIELD_TARJETA = "Tarjeta"
FIELD_DIVISA = "Divisa"

REQUIRED_FIELDS = [
    FIELD_CONCEPTO,
    FIELD_FECHA,
    FIELD_IMPORTE,
]


def _as_d_m_Y_datetime(value):
    return as_datetime(value, "%d/%m/%Y")


_type_conversion_map = {
    FIELD_DISPONIBLE: as_float,
    FIELD_F_VALOR: _as_d_m_Y_datetime,
    FIELD_FECHA: _as_d_m_Y_datetime,
    FIELD_IMPORTE: as_float,
    FIELD_DIVISA: as_currency,
}


class Plugin(Loader, Mapper):
    def load(self, spreadsheet: bytes) -> UnmappedData:
        csv = spreadsheet_as_csv(spreadsheet)
        raw_data = load_csv(csv)
        parsed_data = _parse_bbva_csv(raw_data)

        return parsed_data

    def map(self, data: UnmappedData) -> List[Transaction]:
        def _map_item(raw_item):
            typed_item = self.map_to_native_types(
                item=raw_item, fns=_type_conversion_map
            )

            notes = [
                typed_item.get(FIELD_MOVIMIENTO),
                typed_item.get(FIELD_OBSERVACIONES),
            ]
            notes = " :: ".join([x for x in notes if x])

            return Transaction(
                date=typed_item[FIELD_FECHA],
                amount=typed_item[FIELD_IMPORTE],
                description=typed_item[FIELD_CONCEPTO],
                origin=typed_item.get(FIELD_TARJETA),
                currency=typed_item.get(FIELD_DIVISA),
                notes=notes or None,
            )

        return [_map_item(item) for item in data]


def _parse_bbva_csv(data: List[List[Any]]) -> UnmappedData:
    clean_data = []
    headers: List[str] = []

    for (idx, row) in enumerate(data):
        if headers:
            item = {headers[idx]: value for (idx, value) in enumerate(row)}
            item = {k: v for (k, v) in item.items() if k and v not in (None, "")}
            if _is_valid_item(item):
                clean_data.append(item)
                LOGGER.debug(f"data found at line {idx+1}")
            else:
                LOGGER.debug(f"invalid data found at line {idx+1}")

        if not headers and _is_headers_row(row):
            headers = row
            LOGGER.debug(f"headers found at line {idx+1}: {headers}")

    return clean_data  # type: ignore[return-value]


def _is_headers_row(row):
    return all([field in row for field in REQUIRED_FIELDS]) and row[0] == ""


def _is_valid_item(item):
    return all([item.get(field) for field in REQUIRED_FIELDS])
