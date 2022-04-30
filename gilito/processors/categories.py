from gilito import processors
from gilito.models import Category, Transaction
from gilito.processors import Contains, Or

CATEGORIES = [
    ("Hogar", Contains("Charter consum")),
    ("Agua", Contains("facsa")),
    ("Ahorro", Contains("traspaso periódico a meta")),
    ("Electricidad", Or([Contains("iberdrola"), Contains("adeudo de iberdrola")])),
    ("Gas", Contains("gas natural")),
    ("Seguros", Contains("axa aurora vida")),
    ("Transporte", Contains("Bici-cas")),
    ("Vehículos", Or([Contains("feu vert"), Contains("Compaãia valenciana")])),
    ("Hipoteca", Contains("Cargo por amortizacion de prestamo/credito")),
    ("Hogar", Contains("adeudo cdad prop cl guitarrista fortea 17")),
    ("Mejoras casa", Or([Contains("bricomart"), Contains("leroy merlin")])),
    ("Nómina", Contains("abono de nómina")),
    ("Salud", Contains("Tabarca psicologia")),
    ("Estética", Contains("Tamara velazquez")),
    ("Telecomunicaciones", Contains("Adeudo pepe mobile, s.l.u.")),
    (
        "Jarana",
        Or(
            [
                Contains("15 tapas cb"),
                Contains("cafe frappe"),
                Contains("cafeteria comertel"),
                Contains("cafeteria el sabroson"),
                Contains("canaya"),
                Contains("cocteleria absentia"),
                Contains("copa y corte s.l"),
                Contains("cru vineria sl"),
                Contains("el jardi dels sentits"),
                Contains("frankfurt 87"),
                Contains("justeatspai"),
                Contains("la garnatxa"),
                Contains("la griferia"),
                Contains("m top gastrobar cb"),
                Contains("malabar hosteleria cb"),
                Contains("mi cafe"),
                Contains("panaderia 365"),
                Contains("restaurante eleazar"),
                Contains("restaurante uji"),
            ]
        ),
    ),
]


class Processor(processors.Processor):
    def process_one(self, transaction: Transaction) -> Transaction:
        for (category, f) in CATEGORIES:
            if f.matches(transaction):
                transaction.category = Category(name=category)

        return transaction
