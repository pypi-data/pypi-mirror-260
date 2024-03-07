# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.modules.company.tests import CompanyTestMixin
from trytond.tests.test_tryton import ModuleTestCase


class SalePosChannelTestCase(CompanyTestMixin, ModuleTestCase):
    "Test Sale Pos Channel module"
    module = 'sale_pos_channel'
    extras = ['sale_shipment_cost', 'commission', 'sale_payment_channel',
        'sale_margin']


del ModuleTestCase
