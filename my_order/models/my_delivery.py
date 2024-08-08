# -*- coding: utf-8 -*-
from odoo import fields, models


class MyDelivery(models.Model):
    _inherit = 'stock.picking'

    sale_person = fields.Many2one(comodel_name='res.users', string="Sale Person")

    def button_validate(self):
        self.sale_person = self.sale_id.user_id.id
        return super(MyDelivery, self).button_validate()

