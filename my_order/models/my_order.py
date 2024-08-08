# -*- coding: utf-8 -*-
from odoo import fields, models


class MyOrder(models.Model):
    _name = "my.order"

    sale_id = fields.Many2one(comodel_name = 'sale.order',string="Sale Order")
    state= fields.Selection(related='sale_id.state')

    def transfer_action(self):
        # self.sale_id.write({'state': 'sale'})
        self.sale_id.action_confirm()
