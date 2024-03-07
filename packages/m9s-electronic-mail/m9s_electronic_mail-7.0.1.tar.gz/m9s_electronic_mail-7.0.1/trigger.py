# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction


class Trigger(metaclass=PoolMeta):
    __name__ = 'ir.trigger'
    email_template = fields.Many2One('electronic.mail.template', 'Template')

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.action.selection.append(
            ('electronic.mail.template|mail_from_trigger', "Email Template"),
            )

    @staticmethod
    def default_model():
        model = Transaction().context.get('model', None)
        if model:
            return model
