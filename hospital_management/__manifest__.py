{
    'name': 'HOSPITAL MANAGEMENT',
    'depends': ['base', 'hr','hr_hourly_cost'],
    'version': '17.0.1.0',
    'application': 'True',

    'data': [

        'security/ir.model.access.csv',
        'view/op_sequence.xml',
        'view/op.xml',
        'view/doctor.xml',
        'view/patient.xml',
        'view/hospital_menu.xml',
        'view/specialization.xml',

    ],
}
