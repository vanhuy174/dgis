# -*- coding: utf-8 -*-
{
    'name': "custom_water",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mail',
                'base',
                'crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/bill.xml',
        'views/res_users.xml',
        'views/household.xml',
        'views/member_fam.xml',
        'data/sequence.xml',
        'views/address.xml',
        'report/bill_report.xml',
        'report/amount_of_water_report_graph.xml',
        'views/amount_of_water.xml',
        'views/res_company_inherit.xml',
        'views/res_partner_inherit.xml',
        'views/menu.xml',
        'security/custom_group_users.xml',
        'security/ir.model.access.csv',
        'security/user_record_rule.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}