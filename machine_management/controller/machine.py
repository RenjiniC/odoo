# # -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class MachineList(http.Controller):
    @http.route('/machines', type="json", auth="public")
    def new_machine(self):
        machines = request.env['machine_management'].search([], limit=4)
        machine_data_list = []
        for machine in machines:
            machine_data = {
                'machine': machine.machine_name_id
            }
            machine_data_list.append(machine_data)
            data_list = {
                'data': machine_data_list
            }
            res = http.Response(template='machine_management.machine_list',
                                qcontext=data_list)
        return res.render()
