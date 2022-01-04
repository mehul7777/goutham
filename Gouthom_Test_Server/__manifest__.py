# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Goutham Project',
    'version': '1.0',
    'author': 'Mehul Darji',
    'category': 'Project',
    'summary': 'Goutham Project',
    'description': "For Test Server",
    'website': 'https://www.odoo.com',
    'depends': [
        'base', 'product', 'sale', 'purchase', 'project', 'crm', 'account', 'hr', 'sale_project'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/Customers_Import_view.xml',
        'wizard/Products_Import_view.xml',
        'wizard/Vendor_Pricelist_Import_view.xml',
        'wizard/Sale_Order_Import_view.xml',
        'wizard/Purchase_Order_Import_view.xml',
        'wizard/CRM_Import_view.xml',
        'wizard/Analytic_Account_Import_view.xml',
        'wizard/Project_Project_Import_view.xml',
        'wizard/Project_Task_Import_view.xml',
        'wizard/Timesheets_Import_view.xml',
        'wizard/Hr_Employees_Import_view.xml',
        'wizard/Chart_of_Accounts_Import_view.xml',
        'wizard/Customer_Invoices_Import_view.xml',
        'wizard/Vendor_Bills_Import_view.xml',
        'views/Inherit_Template_view.xml',
        'views/inherit_res_partner.xml',
        'views/Inherit_sale_order_view.xml',
        'views/Inherit_crm_view.xml',
        'views/Inherit_analytic_account_view.xml',
        'views/Inherit_project_project_view.xml',
        'views/Inherit_Project_Task_view.xml',
        'views/Inherit_hr_employee_view.xml',
        'views/Inherit_Account_Move_view.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
