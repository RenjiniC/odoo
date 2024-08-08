# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class MachineTransfer(models.Model):
    _name = "machine.transfer"
    _description = "Machine Transfer"
    _inherit = "mail.thread"
    _rec_name = "reference_no"

    reference_no = fields.Char(string='Reference', readonly=True,
                               default=lambda self: _('New'))
    machine_name_id = fields.Many2one('machine.management',
                                      ondelete='restrict',
                                      tracking=True,
                                      required=True)
    alternate_ids = fields.Many2many('machine.management',
                                     string='wing_alternate_rel',
                                     compute='_compute_alternate_ids')
    machine_serial_no = fields.Char(related='machine_name_id.machine_serial_no')
    company = fields.Many2one(related='machine_name_id.company_id')
    transfer_date = fields.Date(string='Date',
                                tracking=True)
    transfer_type = fields.Selection([('install', 'Install'),
                                      ('remove', 'Remove')])
    customer_id = fields.Many2one(comodel_name='res.partner',
                                  string='Customer',
                                  tracking=True, )
    internal_notes = fields.Char(string='Internal Notes')
    active = fields.Boolean(string='active', default=True)

    @api.model_create_multi
    def create(self, vals_list):
        """ Create the sequence number"""
        for vals in vals_list:
            if vals.get('reference_no', _('New')) == _('New'):
                vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                    'transfer') or _('New')
        return super(MachineTransfer, self).create(vals_list)

    def service_create(self):
        self.env['machine.service'].create([{
                    'machine_name_id': self.machine_name_id.id,
                    'state': 'open',
                    'date': self.transfer_date + timedelta(
                        self.machine_name_id.service_frequency_id.total_days),
                     }])

    def transfer_action(self):
        """Returns the form view of the corresponding machine and change,
        change the customer to the customer given in the transfer form
        and change the state in to in-service"""
        self.machine_name_id.write({'customer_id': self.customer_id.id,
                                    'state': 'in_service'})
        services = self.env['machine.service'].search([])
        new = services.mapped('machine_name_id').ids
        if self.machine_name_id.id not in new:
            self.service_create()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'machine.management',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.machine_name_id.id,
        }

    @api.depends('transfer_type')
    def _compute_alternate_ids(self):
        """To show the active state machines if the activity type is installed
        and show the in-service machines when activity type is removed"""
        for rec in self:
            rec.alternate_ids = False
            if rec.transfer_type == 'install':
                alternate_id = rec.env['machine.management'].search(
                        [('state', '=', 'active')])
            else:
                alternate_id = rec.env['machine.management'].search(
                   [('state', '=', 'in_service')])
            rec.alternate_ids = alternate_id.ids
