# -*- coding: utf-8 -*-
from odoo import fields, models


class MachineParts(models.Model):
    _name = "machine.part"
    _description = "Machine Parts"

    order_id = fields.Many2one(
                    comodel_name='machine.management',
                    string="Order Reference",
                    required=True, ondelete='cascade', index=True, copy=False)
    product_id = fields.Many2one(comodel_name='product.product',
                                 string="Parts Name",
                                 ondelete='restrict')
    product_uom_qty = fields.Float(
                                string="Quantity",
                                digits='Product Unit of Measure',
                                default=1.0,
                                store=True, readonly=False,
                                index='btree_not_null',
                                required=True)
    product_uom = fields.Many2one(
                                comodel_name='uom.uom',
                                string="Unit of Measure",
                                store=True, index='btree_not_null',
                                readonly=False)
