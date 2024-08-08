# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields, models, api, _, Command
from odoo.exceptions import UserError
from odoo.fields import Date

SERVICE_STATE = [
    ('open', "Open"),
    ('started', "Started"),
    ('done', "Done"),
    ('cancel', "Cancel")
]


class MachineService(models.Model):
    _name = "machine.service"
    _description = "Machine Services"
    _inherit = ['mail.thread']
    _rec_name = "reference_no"

    reference_no = fields.Char(string='Reference', readonly=True,
                               default=lambda self: _('New'))
    machine_name_id = fields.Many2one('machine.management',
                                      tracking=True,
                                      required=True)
    customer_id = fields.Many2one(related='machine_name_id.customer_id')
    company_id = fields.Many2one(related='machine_name_id.company_id')
    date = fields.Date(string='Date',
                       help="Service Date of machine",
                       required=True)
    description = fields.Char('Description')
    internal_notes = fields.Char('Internal Notes')
    tech_person_ids = fields.Many2many(comodel_name='res.users',
                                       string="Tech Person")
    parts_consumed = fields.One2many(
                            related='machine_name_id.product_order_line_ids',
                            string='Parts Consumed')
    state = fields.Selection(selection=SERVICE_STATE, string="Status",
                             required=True,
                             copy=False,
                             index=True,
                             default='open',
                             tracking=True)
    service_frequency_id = fields.Many2one(
                             related='machine_name_id.service_frequency_id',
                             string='Service Frequency')
    last_service_date = fields.Date(related='machine_name_id.last_service_date')
    active = fields.Boolean(string='active',
                            default=True)

    @api.model_create_multi
    def create(self, vals_list):
        """To create the sequence number"""
        for vals in vals_list:
            if vals.get('reference_no', _('New')) == _('New'):
                vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                    'service') or _('New')
        return super(MachineService, self).create(vals_list)

    def start_case_action(self):
        self.write({'state': 'started'})

    def close_case_action(self):
        self.write({'state': 'done'})
        template = self.env.ref('machine_management.email_template_service')
        template.send_mail(self.id, force_send=True)

    def create_invoice_action(self):
        """Create invoice for the machine service, add a small amount as a
        service charge by default and add the consumed parts and their price
        in the invoice"""
        for record in self:
            if record.env['account.move'].search([('state', '=', 'draft'),
                                                  ('partner_id', '=',
                                                   record.customer_id.id)]):
                val = record.env['account.move'].search([
                                                    ('state', '=', 'draft'),
                                                    ('partner_id', '=',
                                                     record.customer_id.id)],
                                                     limit=1)
                val.write({
                    'invoice_line_ids': [Command.create({
                        'name': 'Service Charge',
                        'price_unit': 100.0})] + [Command.create({
                                       'product_id': rec.product_id.id,
                                       'price_unit': rec.product_id.lst_price
                                       }) for rec in
                                  record.parts_consumed
                                  ]})
            else:
                service_invoice = record.env['account.move'].create([{
                    'move_type': 'out_invoice',
                    'invoice_date': fields.Date.today(),
                    'partner_id': record.customer_id.id,
                    'currency_id': record.machine_name_id.currency_id.id,
                    'amount_total': record.machine_name_id.parts_ids.product_id.
                    lst_price,
                    'invoice_line_ids': [Command.create({
                        'name': 'Service Charge',
                        'price_unit': 100.0})] + [Command.create(
                         {'product_id': rec.product_id.id,
                          'quantity': rec.product_uom_qty,
                          'price_unit': rec.product_id.lst_price * rec.product_uom_qty
                          }) for rec in record.parts_consumed
                                        ]},
                ])
                service_invoice.action_post()

    def service_schedule(self):
        """To create reccurring service for a machine"""
        service = self.search([], order='id desc')
        for rec in service.mapped('machine_name_id'):
            var = service.filtered(lambda s: s.machine_name_id == rec)[0]
            if (var.date < Date.today()) and (var.state == 'done'):
                var.create({
                        'machine_name_id': var.machine_name_id.id,
                        'state': 'open',
                        'date': var.date + timedelta(
                                var.service_frequency_id.total_days),
                         })

    def action_archive(self):
        """Only Manager can archive the machine service"""
        if self.user_has_groups('machine_management.machine_tech_person_access'):
            raise UserError(_('Only Manager can archive the machine service'))
        else:
            return super().action_archive()
