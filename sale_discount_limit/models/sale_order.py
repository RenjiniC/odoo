# -*- coding: utf-8 -*-
from odoo import models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        rec = float(self.env['ir.config_parameter'].sudo().get_param(
            'sale_discount_limit.discount_limit'))
        sale_order = self.env['sale.order'].search([])
        record_monthly = sale_order.filtered(
                                lambda s: s.partner_id == self.partner_id and
                                s.date_order.month == self.date_order.month
                                             )
        total_discount = (sum(record_monthly.order_line.mapped('price_unit')) -
                          sum(record_monthly.order_line.mapped('price_subtotal')
                              ))
        if total_discount > rec:
            raise UserError(
                _('Total discount of the month is exceed the limit'))
        else:
            return super().action_confirm()
