# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond import backend
from trytond.pool import PoolMeta


class Activity(metaclass=PoolMeta):
    __name__ = "activity.activity"

    @classmethod
    def __setup__(cls):
        super(Activity, cls).__setup__()
        # TODO change required to state required
        cls.employee.required = False

    @classmethod
    def __register__(cls, module_name):
        table = backend.TableHandler(cls, module_name)

        super(Activity, cls).__register__(module_name)
        table.not_null_action('employee', 'remove')
