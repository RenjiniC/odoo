{
    'name': 'MACHINE MANAGEMENT',
    'depends': ['base','mail','product','web'],
    'version': '17.0.6.0',
    'application': True,
    'license': 'LGPL-3',
    'summery': 'Machine Management',
    'category': '',
    'author': 'Renjini',
    'sequence': 11,

    'data': [
             'security/res_groups.xml',
             'security/ir_rules.xml',
             'security/ir.model.access.csv',
             'report/ir_actions_report.xml',
             'report/machine_transfer_report.xml',
             'data/machine_type_data.xml',
             'data/machine_tag_data.xml',
             'data/service_frequency_data.xml',
             'data/email_template_data.xml',
             'data/ir_cron_data.xml',
             'wizard/transfer_wizard_view.xml',
             'view/machine_views.xml',
             'view/machine_menu.xml',
             'view/machine_reference_sequence.xml',
             'view/machine_type_menu.xml',
             'view/machine_transfer_views.xml',
             'view/machine_tag_menu.xml',
             'view/res_partner_view.xml',
             'view/machine_service_views.xml',
             'view/service_frequency_views.xml',
             'view/machine_report_menu.xml',
             'view/dynamic_snippet.xml',
             # 'view/dynamic_snippet_template.xml',


    ],
    'assets': {
            'web.assets_backend': [
                '/machine_management/static/src/js/action_manager.js',
            ],
            'web.assets_frontend': [
                    'machine_management/static/src/js/dynamic_snippet.js',
                    # 'machine_management/static/src/xml/home_template.xml',
                    'machine_management/static/src/xml/machine_snippet_templates.xml'

                ],
        },
}
