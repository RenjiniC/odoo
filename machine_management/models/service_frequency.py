# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ServiceFrequency(models.Model):
    _name = 'service.frequency'
    _description = "Service frequency"

    name = fields.Char(string='Name')
    number = fields.Integer()
    frequency = fields.Selection([('month', 'Month'), ('week', 'Week'),
                             ('day', 'Day'), ('year', 'Year')], required=True)
    days = fields.Integer(compute='_compute_no_of_days',
                          string='No of Days')
    total_days = fields.Integer(compute='_compute_total_days')

    @api.depends('frequency')
    def _compute_no_of_days(self):
        """To compute the Number of Days"""
        if self.frequency == 'month':
            self.days = 30
        if self.frequency == 'week':
            self.days = 7
        if self.frequency == 'year':
            self.days = 365
        if self.frequency == 'day':
            self.days = 1

    @api.depends('days')
    def _compute_total_days(self):
        """To compute the total Number of Days"""
        self.total_days = self.number * self.days
