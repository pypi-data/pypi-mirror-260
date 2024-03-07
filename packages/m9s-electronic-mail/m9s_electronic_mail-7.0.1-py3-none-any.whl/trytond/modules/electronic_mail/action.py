# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond import backend
from trytond.model import fields
from trytond.pool import PoolMeta


class ActionReport(metaclass=PoolMeta):
    __name__ = 'ir.action.report'
    email_filename = fields.Char('Email File Name', translate=True,
        help='File name e-mail attachment without extension. '
        'eg. sale_${record.reference}')


class ActionWizard(metaclass=PoolMeta):
    __name__ = 'ir.action.wizard'
    template = fields.One2Many("electronic.mail.template", 'wizard', 'Template')
