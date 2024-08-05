from odoo import fields, models


class Patient(models.Model):
    _inherit = 'res.partner'

    blood_group = fields.Selection([('a+','A+'),('a-','A-'),('b+','B+'),('b-','B-'),('ab+','AB+'),('ab-','AB-'),('o+','O+'),('o-','O-')])
    date_of_birth = fields.Date(string='DOB')
    age = fields.Integer(string="Age")
    gender = fields.Selection([('male', 'Male'),('female', 'Female'),])


