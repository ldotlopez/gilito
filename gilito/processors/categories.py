from gilito import processors
from gilito.models import Category, Transaction

CATEGORIES = [
    ("Hogar", ["Charter consum"]),
    ("Agua", ["facsa"]),
    ("Ahorro", ["traspaso periódico a meta"]),
    ("Electricidad", ["iberdrola", "adeudo de iberdrola"]),
    ("Gas", ["gas natural"]),
    ("Seguros", ["axa aurora vida"]),
    ("Transporte", ["Bici-cas"]),
    ("Vehículos", ["feu vert", "Compaãia valenciana"]),
    ("Hipoteca", ["Cargo por amortizacion de prestamo/credito"]),
    ("Hogar", ["adeudo cdad prop cl guitarrista fortea 17"]),
    ("Mejoras casa", ["bricomart", "leroy merlin"]),
    ("Nómina", ["abono de nómina"]),
    ("Salud", ["Tabarca psicologia"]),
    ("Estética", ["Tamara velazquez"]),
    ("Telecomunicaciones", ["Adeudo pepe mobile, s.l.u."]),
    (
        "Jarana",
        [
            "15 tapas cb",
            "cafe frappe",
            "cafeteria comertel",
            "cafeteria el sabroson",
            "canaya",
            "cocteleria absentia",
            "copa y corte s.l",
            "cru vineria sl",
            "el jardi dels sentits",
            "frankfurt 87",
            "justeatspai",
            "la garnatxa",
            "la griferia",
            "m top gastrobar cb",
            "malabar hosteleria cb",
            "mi cafe",
            "panaderia 365",
            "restaurante eleazar",
            "restaurante uji",
        ],
    ),
]


class Processor(processors.Processor):
    def process_one(self, transaction: Transaction) -> Transaction:

        description = transaction.description.lower()
        if notes := transaction.notes:
            notes = notes.lower()  # type: ignore[union-attr]
        else:
            notes = ""

        for (category, needles) in CATEGORIES:
            for needle in needles:
                needle = needle.lower()
                if needle in description or needle in notes:
                    transaction.category = Category(name=category)
                    return transaction

        return transaction
