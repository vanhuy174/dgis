from odoo import api, fields, models

class Employee(models.Model):
    _name = 'cmsw.employee'
    _inherit = "res.partner"
    _description = 'Employee'



