# -*- coding: utf-8 -*-
from odoo import fields, models


class MyContact(models.Model):
    _inherit = 'res.partner'

    is_only_ordered = fields.Boolean(string="Is Only Ordered", default=True)
