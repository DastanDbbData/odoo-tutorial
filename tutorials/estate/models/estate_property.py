from odoo import models, fields, api
from datetime import timedelta, date

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    # Basisinformationen
    name = fields.Char(required=True, string="Title")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    
    # Verfügbarkeit und Preis
    date_availability = fields.Date(
        string="Available From",
        default=lambda self: date.today() + timedelta(days=90),
        copy=False
    )
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    
    # Property Details
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )

    total_area = fields.Integer(
        string = "Total Area (sqm)",
        compute = "_compute_total_area",
        store = True
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    best_price = fields.Float(
        string = "Best Offer",
        compute = "_compute_best_price",
        store = True
    )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    # Property Type (Many2one zu estate.property.type)
    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Property Type",
    )
    buyer_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        copy=False
    )
    salesperson_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        copy=False
    )

    #Property Tag Many2Many
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string="Tags"
    )

    #Property Offer One2Many
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string="Offers"
    )
    
    # Status / Workflow
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='new',
        string="Status"
    )
