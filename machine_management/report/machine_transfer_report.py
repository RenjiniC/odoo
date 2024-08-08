# -*- coding: utf-8 -*-
from odoo import models, api


class MachineTransferReport(models.AbstractModel):
    _name = 'report.machine_management.report_machine_transfer'
    _description = 'get machine transfer details as report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['machine.transfer'].browse(
                                        [rec['id'] for rec in data['report']])
        return {
            'doc_ids': docids,
            'doc_model': 'machine.transfer',
            'docs': docs,
            'data': data,
        }
