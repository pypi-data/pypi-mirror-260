# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


class User(metaclass=PoolMeta):
    __name__ = "res.user"
    signature_html = fields.Text('Signature HTML')

    @classmethod
    def __setup__(cls):
        super(User, cls).__setup__()
        if not cls._preferences_fields:
            cls._preferences_fields = []
        cls._preferences_fields.append('signature_html')
