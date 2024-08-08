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

    def action_pdf(self):
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
        data = {'date': self.read()[0], 'report': report}
        return self.env.ref(
            'machine_management.action_report_machine_transfer').report_action(
                                                            None, data=data)
    def action_xlsx(self):
        print('action_xlsx')
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
        # for record in report:
        #     record['id']
        docs = self.env['machine.transfer'].browse(
                                        [record['id'] for record in report])
        print(docs.read())
        data = docs.read()
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'example.xlsx.wizard',
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
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('C2:I2', 'MACHINE TRANSFER REPORT', head)
        sheet.write('A4', 'Machine Name', cell_format)
        sheet.write('B4', 'Reference no', cell_format)
        sheet.write('C4', 'Transfer Type', cell_format)
        sheet.write('D4', 'Date', cell_format)
        sheet.write('E4', 'Customer', cell_format)
        for i, rec in enumerate(data['report'], start=5):
            sheet.write(f'A{i}', rec, txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
