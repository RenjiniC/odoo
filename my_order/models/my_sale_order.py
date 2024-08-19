# -*- coding: utf-8 -*-
from odoo import fields, models, Command


class MySaleOrder(models.Model):
    _inherit = 'sale.order'

    def button_confirm(self):
        self.write({'invoice_line_ids': [Command.create({
                                       'product_id': rec.product_id.id,
                                       'price_unit': rec.product_id.lst_price
                                       }) for rec in self
                                  ]})
        self.action_post()
        return super(MySaleOrder, self).button_confirm()
