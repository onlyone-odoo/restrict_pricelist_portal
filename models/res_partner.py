# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    allowed_pricelist_ids = fields.Many2many(
        "product.pricelist",
        string="Listas de precios permitidas",
        help="Listas de precios que este contacto puede seleccionar en el portal.",
    )
