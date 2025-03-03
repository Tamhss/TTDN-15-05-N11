# -*- coding: utf-8 -*-
{
    'name': "QLVB",

    'summary': """Hệ thống quản lý văn bản và điều hành""",

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
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        # security
        'security/ir.model.access.csv',

        # seed data
        'data/phong_ban_data.xml',
        'data/chuc_vu_data.xml',
        'data/nhan_vien_data.xml',
        'data/lich_su_cong_tac_data.xml',
        'data/chung_chi_data.xml',

        'data/document_agency_level_data.xml',
        'data/document_external_agency_data.xml',
        'data/document_field_data.xml',
        'data/document_internal_department_data.xml',
        'data/document_job_position_data.xml',
        'data/document_priority_level_data.xml',
        'data/document_security_level_data.xml',
        'data/document_public_holiday_data.xml',
        'data/document_register_data.xml',
        'data/document_type_data.xml',
        'data/document_year.xml',
        # seq
        'data/seq/document_seq.xml',

        # view
        'views/document_category.xml',
        'views/document_incoming.xml',
        'views/document_outgoing.xml',
        'views/document_report.xml',
        'views/document_sign.xml',
        'views/document_workflow.xml',

        'views/document_agency_level.xml',
        'views/document_external_agency.xml',
        'views/document_field.xml',
        'views/document_internal_department.xml',
        'views/document_job_position.xml',
        'views/document_priority_level.xml',
        'views/document_public_holiday.xml',
        'views/document_register.xml',
        'views/document_security_level.xml',
        'views/document_type.xml',
        'views/document_year.xml',
        'views/document_incoming_filter.xml',
        
        'security/ir.model.access.csv',
        'views/nhan_vien.xml',
        'views/phong_ban.xml',
        'views/chuc_vu.xml',
        'views/chung_chi.xml',
        'views/lich_su_cong_tac.xml',

        'views/menu.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
