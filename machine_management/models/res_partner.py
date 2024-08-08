# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    machine_name_ids = fields.One2many('machine.management',
                                       'customer_id',
                                       string='Machines')
    customer_machine_count = fields.Integer(
                                    string="Machines",
                                    compute='_compute_customer_machine_count')

    def _compute_customer_machine_count(self):
        """ To count the number of machines of customer"""
        for new in self:
            new.customer_machine_count = (self.env['machine.management'].
                                          search_count(
                [('machine_name_id', '=', new.machine_name)]))

    def customer_machine(self):
        """ Returns the machines"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'machine.management',
            'view_mode': 'tree,form',
            'view_type': 'tree',
            'domain': [('customer_id.name', '=', self.name)],
        }

    def action_archive(self):
        """ Archive the machines of a customer while archiving the
        corresponding customer"""
        res = super().action_archive()
        if not self.active:
            for rec in self.machine_name_ids:
                rec.action_archive()
        return res

    def action_unarchive(self):
        """ Un-archive the machines of a customer while un-archiving the
        corresponding customer"""
        res = super().action_unarchive()
        if self.active:
            for rec in self.machine_name_ids.search([
                 ('active', '=', False), ('customer_id', '=', self.id)]):
                rec.action_unarchive()
        return res
