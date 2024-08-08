# -*- coding: utf-8 -*-
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

MACHINE_STATE = [
    ('active', "Active"),
    ('in_service', "In Service"),
]


class MachineManagement(models.Model):
    _name = "machine.management"
    _description = "Machine Management"
    _inherit = "mail.thread"
    _rec_name = "machine_name"

    reference_no = fields.Char(string='Reference', readonly=True,
                               default=lambda self: _('New'))
    machine_name = fields.Char(string='Machine Name', help="Machine Name")
    machine_serial_no = fields.Char(string='Serial No',
                                    required=True)
    date_of_purchase = fields.Date(string='Date',
                                   help="Purchase Date of machine",
                                   required=True)
    currency_id = fields.Many2one(comodel_name='res.currency',
                                  compute='_compute_currency_id')
    purchase_value = fields.Monetary(string='Purchase Value',
                                     currency_field='currency_id',
                                     tracking=True, widget='monetary',
                                     help="Purchase Amount of machine")
    image = fields.Binary(widget="image", help="Image of the Machine")
    instruction = fields.Html(string='Instructions',
                              help="Instructions regarding the machine")
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer',
                                  required=True,
                                  tracking=True,
                                  help="Name of the customer of the machine")
    company_id = fields.Many2one(comodel_name='res.company', string='Company',
                                 help="Name of the company")
    machine_type_id = fields.Many2one('machine.type')
    state = fields.Selection(selection=MACHINE_STATE, string="Status",
                             required=True,
                             copy=False,
                             index=True,
                             default='active',
                             tracking=True)
    description = fields.Char('Description',
                              help="Description of the Machine")
    warranty = fields.Selection([('yes', 'YES'), ('no', 'No')],
                                tracking=True, help="Warranty of the machine")
    machine_transfer_count = fields.Integer(
                            string="Machine Transfer",
                            compute='_compute_machine_transfer_count'
                            )
    machine_case_count = fields.Integer(
                            string="Machine Service",
                            compute='_compute_machine_case_count'
                            )
    product_order_line_ids = fields.One2many('machine.part',
                                             'order_id',
                                             string="Order Lines")
    parts_ids = fields.One2many('machine.part',
                                'product_id',
                                string="parts")
    machine_tag_ids = fields.Many2many('machine.tag')
    machine_age = fields.Integer(compute="_compute_machine_age", store=True)
    active = fields.Boolean(string='active', default=True)
    last_service_date = fields.Date(compute='_compute_last_service_date')
    service_frequency_id = fields.Many2one(comodel_name='service.frequency',
                                           required=True,
                                           string='Schedule Service every')

    @api.model_create_multi
    def create(self, vals_list):
        """To create the sequence number"""
        for vals in vals_list:
            if vals.get('reference_no', _('New')) == _('New'):
                vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                    'machine') or _('New')
        return super(MachineManagement, self).create(vals_list)

    @api.constrains('purchase_value')
    def _check_values(self):
        """Purchase value validation"""
        if self.purchase_value <= 0.0:
            raise ValidationError(_('Purchase Values should greater than 0.'))

    @api.constrains('machine_serial_no')
    def _check_serial_no(self):
        """serial number validation"""
        for rec in self:
            domain = [('machine_serial_no', '=', rec.machine_serial_no)]
            count = self.search_count(domain)
            if count > 1:
                raise ValidationError(_("The Serial No should be unique"))

    @api.depends('company_id')
    def _compute_currency_id(self):
        """To compute the currency_id"""
        main_company = self.env['res.company']._get_main_company()
        for template in self:
            template.currency_id = (template.company_id.sudo().currency_id.id or
                                    main_company.currency_id.id)

    @staticmethod
    def redirect_new(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'machine.transfer',
            'view_mode': 'tree',
            'view_type': 'form',
        }

    def _compute_machine_transfer_count(self):
        """Show the count of transfer count of the machine"""
        for new in self:
            new.machine_transfer_count = \
                (self.env['machine.transfer'].search_count(
                 [('machine_name_id', '=', new.machine_name)]))

    def transfer_history(self):
        """To show the transfer of the machine"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'machine.transfer',
            'view_mode': 'tree,form',
            'view_type': 'tree',
            'domain': [('machine_name_id', '=', self.machine_name)],
        }

    @api.depends('date_of_purchase')
    def _compute_machine_age(self):
        """To compute the age of the machine from the date of purchase"""
        for record in self:
            if (record.date_of_purchase and
                    record.date_of_purchase <= fields.Date.today() - timedelta(
                        days=1)):
                record.machine_age = relativedelta(
                    fields.Date.from_string(fields.Date.today()),
                    fields.Date.from_string(record.date_of_purchase)).years

            elif (record.date_of_purchase and
                  record.date_of_purchase >= fields.Date.today()):
                record.machine_age = relativedelta(
                    fields.Date.from_string(fields.Date.today()),
                    fields.Date.from_string(record.date_of_purchase)).years
                record.machine_age = 0

    @staticmethod
    def redirect_service_new(self):
        """Returns the service page"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'machine.service',
            'view_mode': 'form',
            'view_type': 'form',
        }

    def _compute_machine_case_count(self):
        """to count the machine case count"""
        for new in self:
            new.machine_case_count = (self.env['machine.service'].search_count(
                [('machine_name_id', '=', new.machine_name)]))

    def case_history(self):
        """to show all the case history"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'machine.service',
            'view_mode': 'tree,form',
            'view_type': 'tree',
            'domain': [('machine_name_id', '=', self.machine_name)],
        }

    def _compute_last_service_date(self):
        for rec in self:
            rec.last_service_date = self.env['machine.service'].search(
                [('machine_name_id', '=', self.machine_name),
                 ('state', '=', 'done')], order='id desc', limit=1).date

    def action_archive(self):
        """Only active state machine can archive"""
        record = self.env['machine.transfer'].search(
            [('machine_name_id', '=', self.machine_name)])
        service = self.env['machine.service'].search(
            [('machine_name_id', '=', self.machine_name)])
        if self.state == 'in_service':
            raise ValidationError("In Service state machines can not archive")
        else:
            for rec in record:
                rec.action_archive()
            for new in service:
                if new.state == 'open':
                    new.state = 'cancel'
        return super().action_archive()

    def action_unarchive(self):
        """ Un archive the machine transfers of the Machines while un archiving
        the corresponding Machine"""
        record = self.env['machine.transfer'].search(
            [('active', '=', False),
             ('machine_name_id', '=', self.machine_name)])
        for rec in record:
            rec.action_unarchive()
        return super().action_unarchive()
