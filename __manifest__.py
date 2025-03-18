{
    "name": "Restricción de Listas de Precios por Usuario Portal",
    "summary": "Restringe las listas de precios seleccionables en el portal según allowed_pricelist_ids",
    "author": "Be OnlyOne",
    "maintainers": ["onlyone-odoo"],
    "website": "https://onlyone.odoo.com/",
    "license": "AGPL-3",
    "category": "Website",
    "version": "17.0.3.1.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": ["website_sale", "portal"],
    "data": [
        "views/res_partner_views.xml",
        "views/tempaltes.xml",
    ],
}
