# -*- coding: utf-8 -*-
import io
import json
import xlsxwriter
from odoo import models, fields
from odoo.tools import date_utils


class TransferWizard(models.TransientModel):
    _name = 'transfer.wizard'

    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    customer_id = fields.Many2one('res.partner', 'Customer',
                                  required=True)

    transfer_type = fields.Selection([('install', 'Install'),
                                      ('remove', 'Remove')],
                                     'Transfer Type',
                                     required=True)

    machine_name_id = fields.Many2one('machine.management',
                                      'Machine',
                                      required=True)

    def get_data(self):
        query = """select * from machine_transfer where transfer_date between %s and %s
                        AND transfer_type = %s
                        AND customer_id = %s
                        AND machine_name_id = %s
                        """
        record = [self.from_date,
                  self.to_date,
                  self.transfer_type,
                  self.customer_id.id,
                  self.machine_name_id.id]
        self.env.cr.execute(query, tuple(record))
        report = self.env.cr.dictfetchall()
        return report

    def action_pdf(self):
        report = self.get_data()
        data = {'date': self.read()[0], 'report': report}
        return self.env.ref(
            'machine_management.action_report_machine_transfer').report_action(
            None, data=data)

    def action_xlsx(self):
        report = self.get_data()
        docs = self.env['machine.transfer'].browse(
            [record['id'] for record in report])
        data = docs.read()
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'transfer.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px','bold': True,
             'align': 'center', 'color': 'red'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True,
             'font_size': '20px', 'color': 'blue'})
        content_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('A3:K4', 'MACHINE TRANSFER REPORT', head)
        sheet.merge_range('A6:B6', 'Machine Name', cell_format)
        sheet.merge_range('C6:D6', 'Reference no', cell_format)
        sheet.merge_range('E6:F6', 'Transfer Type', cell_format)
        sheet.merge_range('G6:H6', 'Date', cell_format)
        sheet.merge_range('I6:J6', 'Customer', cell_format)
        for i, rec in enumerate(data, start=8):
            sheet.merge_range(f'A{i}:B{i}', rec['machine_name_id'][1],
                              content_format)
            sheet.merge_range(f'C{i}:D{i}', rec['reference_no'],
                              content_format)
            sheet.merge_range(f'E{i}:F{i}', rec['transfer_type'],
                              content_format)
            sheet.merge_range(f'G{i}:H{i}', rec['transfer_date'],
                              content_format)
            sheet.merge_range(f'I{i}:J{i}', rec['customer_id'][1],
                              content_format)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
