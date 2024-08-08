# from importlib.resources import _

from odoo import fields, models, api, _


class HospitalOp(models.Model):
    _name = "hospital.op"


    reference_no = fields.Char(string='New',required=True,readonly=True, default=lambda self: _('New'))
    datetime = fields.Datetime(string='DateAndTime')
    patient_id = fields. Many2one(comodel_name='res.partner', string="Patient")
    age = fields.Integer(related='patient_id.age')
    blood_group = fields.Selection(related='patient_id.blood_group')
    doctor_id = fields.Many2one(comodel_name='hr.employee', string="Doctor")
    token_no = fields.Integer(string='TokenNo')
    currency_id = fields.Many2one(comodel_name='res.currency')
    fee = fields.Monetary(related='doctor_id.hourly_cost', string='Fee', currency_field='currency_id')

    @api.model
    def create(self, vals):
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'hospital.patient') or _('New')
        res = super(HospitalOp, self).create(vals)
        return res
