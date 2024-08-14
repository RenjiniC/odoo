# -*- coding: utf-8 -*-
import io
import json
import xlsxwriter
from odoo import models, fields
from odoo.tools import date_utils


class TransferWizard(models.TransientModel):
    _name = 'transfer.wizard'

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    customer_id = fields.Many2one('res.partner', 'Customer')
    transfer_type = fields.Selection([('install', 'Install'),
                                      ('remove', 'Remove')],
                                     'Transfer Type')
    machine_name_id = fields.Many2one('machine.management',
                                      'Machine')

    def get_data(self):
        query = """select * from machine_transfer"""
        record = []
        if self.from_date:
            query += " where transfer_date >= %s"
            record.append(self.from_date)
        if self.to_date:
            query += " AND transfer_date <= %s"
            record.append(self.to_date)
        if self.transfer_type:
            query += " AND transfer_type = %s"
            record.append(self.transfer_type)
        if self.customer_id.id:
            query += " AND customer_id = %s"
            record.append(self.customer_id.id)
        if self.machine_name_id.id:
            query += " AND machine_name_id = %s"
            record.append(self.machine_name_id.id)
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
             'align': 'center', 'color': 'red', 'border': 2})
        head = workbook.add_format(
            {'align': 'center', 'bold': True,
             'font_size': '20px', 'color': 'blue', 'border': 2})
        content_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'border': 2})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('A3:J4', 'MACHINE TRANSFER REPORT', head)
        sheet.merge_range('A5:B6', 'Machine Name', cell_format)
        sheet.merge_range('C5:D6', 'Reference no', cell_format)
        sheet.merge_range('E5:F6', 'Transfer Type', cell_format)
        sheet.merge_range('G5:H6', 'Date', cell_format)
        sheet.merge_range('I5:J6', 'Customer', cell_format)
        for i, rec in enumerate(data, start=7):
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
