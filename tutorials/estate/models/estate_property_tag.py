from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _descriptopn = "Property Tag"

    name = fields.Char(String="Name", required="True")