from odoo import fields,models

class EstateProperty(models.Model):
    _name = "estate.property"

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    expected_price = fields.Float("Expected price", required=True)
    selling_price=fields.Float("Selling price")
    bedrooms=fields.Float("Bedrooms")


