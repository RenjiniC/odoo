# -*- coding: utf-8 -*-
from odoo import models, fields


class TransferWizard(models.TransientModel):
    _name = 'transfer.wizard'

    name = fields.Char(string='name')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    customer_id = fields.Many2one('res.partner', 'Customer')
    transfer_type = fields.Selection([('install', 'Install'),
                                      ('remove', 'Remove')],
                                     'Transfer Type')
    machine_name_id = fields.Many2one('machine.management', 'Machine')

    def action_done(self):
        print('hai')
