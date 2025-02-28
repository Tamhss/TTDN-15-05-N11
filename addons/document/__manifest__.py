# -*- coding: utf-8 -*-
{
    'name': "Quản lý văn bản",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/document_category.xml',
        'views/document_incoming.xml',
        'views/document_outgoing.xml',
        'views/document_report.xml',
        'views/document_sign.xml',
        'views/document_workflow.xml',

        'views/document_agency_level.xml',
        'views/document_external_agency.xml',
        'views/document_internal_department.xml',
        'views/document_job_position.xml',
        'views/document_priority_level.xml',
        'views/document_public_holiday.xml',
        'views/document_register.xml',
        
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
