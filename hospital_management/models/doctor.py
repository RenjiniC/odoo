from odoo import fields, models


class Doctor(models.Model):
    _inherit = 'hr.employee'

    # specialization = fields.Many2many([('general_surgen','General-Surgen'),('pediatric','Pediatric'),('gynecologist','Gynecologist'),('neuro_surgen','Neuro-Surgen')])
    specialization = fields.Many2many('hospital.specialization')