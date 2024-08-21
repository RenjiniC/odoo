# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class MachineList(http.Controller):
    @http.route('/machines', type="json", auth="public")
    def new_machine(self):
        machines = request.env['machine.management'].search_read([], ['id', 'machine_name', 'image', 'purchase_value', 'machine_tag_ids', 'machine_type_id', 'currency_id'], order='id desc')
        return machines



# machines = request.env['machine.management'].search([], order='id desc')
#         machine_data_list = []
#         print(machines)
#         for machine in machines:
#             machine_data = {
#                 'machine': machine.machine_name,
#                 'image': machine.image,
#                 'purchase_value': machine.purchase_value,
#                 'machine_tags': machine.machine_tag_ids,
#                 'machine_type': machine.machine_type_id.name,
#                 'currency_id': machine.currency_id,
#             }
#             machine_data_list.append(machine_data)
#         # data_list = {
#         #             'data': machine_data_list,
#         #     }
#         # print(machine_data_list)
#         # res = http.Response(template='machine_management.machine_list',
#         #                     qcontext=machine_data_list)
#         # return res.render()
#         return machine_data_list
