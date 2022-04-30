import csv
import io
import logging
from typing import Dict, List

from gilito import LogBook, Transaction, mappers

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
    return mappers.as_datetime(value, "%d/%m/%Y")


type_conversion_map = {
    FIELD_DISPONIBLE: mappers.as_float,
    FIELD_F_VALOR: _as_d_m_Y_datetime,
    FIELD_FECHA: _as_d_m_Y_datetime,
    FIELD_IMPORTE: mappers.as_float,
    FIELD_DIVISA: mappers.as_currency,
}


class Mapper(mappers.Mapper):
    def map(self, rows: List[Dict[str, str]]) -> LogBook:
        bbva_data = self._filter_raw_csv(rows)
        native_data = [convert_data_types(item) for item in bbva_data]
        transactions = [self._convert_row(item) for item in native_data]

        return LogBook(transactions=transactions)

    def _convert_row(self, item):
        notes = [item.get(FIELD_MOVIMIENTO), item.get(FIELD_OBSERVACIONES)]
        notes = " :: ".join([x for x in notes if x])

        return Transaction(
            date=item[FIELD_FECHA],
            amount=item[FIELD_IMPORTE],
            description=item[FIELD_CONCEPTO],
            origin=item.get(FIELD_TARJETA),
            currency=item.get(FIELD_DIVISA),
            notes=notes or None,
        )

    def _filter_raw_csv(self, csvdata):
        fh = io.StringIO(csvdata)
        reader = csv.reader(fh)

        data = []
        headers = []
        for (idx, row) in enumerate(reader):
            if headers:
                item = {headers[idx]: value for (idx, value) in enumerate(row)}
                item = {k: v for (k, v) in item.items() if k and v not in (None, "")}
                if is_valid_item(item):
                    data.append(item)
                    LOGGER.debug(f"data found at line {idx+1}")
                else:
                    LOGGER.debug(f"invalid data found at line {idx+1}")

            if not headers and is_headers_row(row):
                headers = row
                LOGGER.debug(f"headers found at line {idx+1}: {headers}")

        return data


def is_headers_row(row):
    return all([field in row for field in REQUIRED_FIELDS]) and row[0] == ""


def is_valid_item(item):
    return all([item.get(field) for field in REQUIRED_FIELDS])


def convert_data_types(item):
    return mappers.map_to_native_types(item=item, fns=type_conversion_map)
