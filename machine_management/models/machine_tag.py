# -*- coding: utf-8 -*-
from odoo import fields, models


class MachineTag(models.Model):
    _name = 'machine.tag'
    _description = "Machine Tag"

    name = fields.Char('Name')
