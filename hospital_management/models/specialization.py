from odoo import fields, models


class State(models.Model):
    _name = 'hospital.specialization'

    name = fields.Char('Name')