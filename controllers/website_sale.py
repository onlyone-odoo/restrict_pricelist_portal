# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleRestrictedPricelists(WebsiteSale):
    @http.route(
        [
            "/shop",
            "/shop/page/<int:page>",
            '/shop/category/<model("product.public.category"):category>',
            '/shop/category/<model("product.public.category"):category>/page/<int:page>',
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=WebsiteSale.sitemap_shop,
    )
    def shop(
        self,
        page=0,
        category=None,
        search="",
        min_price=0.0,
        max_price=0.0,
        ppg=False,
        **post,
    ):
        # Llamar al método original
        response = super(WebsiteSaleRestrictedPricelists, self).shop(
            page=page,
            category=category,
            search=search,
            min_price=min_price,
            max_price=max_price,
            ppg=ppg,
            **post,
        )

        # Filtrar las listas de precios según allowed_pricelist_ids
        partner = request.env.user.partner_id
        allowed_pricelist_ids = partner.allowed_pricelist_ids.ids
        if allowed_pricelist_ids:
            max_allowed_id = max(allowed_pricelist_ids)
            # Filtrar las listas de precios disponibles
            available_pricelists = (
                request.env["product.pricelist"]
                .sudo()
                .search(
                    [
                        ("website_id", "in", (False, request.website.id)),
                        ("selectable", "=", True),
                        ("id", "<=", max_allowed_id),
                    ]
                )
            )
            response.qcontext["website_sale_pricelists"] = available_pricelists

            # Asegurarse de que la lista de precios actual sea válida
            current_pricelist = response.qcontext["pricelist"]
            if current_pricelist.id > max_allowed_id:
                response.qcontext["pricelist"] = (
                    available_pricelists[0]
                    if available_pricelists
                    else request.website.get_current_pricelist()
                )
                # Actualizar la sesión y el pedido con la lista válida
                request.session["website_sale_current_pl"] = response.qcontext[
                    "pricelist"
                ].id
                request.website.sale_get_order(update_pricelist=True)

        return response

    @http.route(
        ['/shop/change_pricelist/<model("product.pricelist"):pricelist>'],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def pricelist_change(self, pricelist, **post):
        # Validar que la lista seleccionada esté permitida si hay restricción
        partner = request.env.user.partner_id
        allowed_pricelist_ids = partner.allowed_pricelist_ids.ids
        if allowed_pricelist_ids:
            max_allowed_id = max(allowed_pricelist_ids)
            if pricelist.id > max_allowed_id:
                # Redirigir a la página de la tienda sin cambiar la lista
                return request.redirect(post.get("r", "/shop"))

        return super(WebsiteSaleRestrictedPricelists, self).pricelist_change(
            pricelist, **post
        )

    @http.route(
        ["/shop/pricelist"], type="http", auth="public", website=True, sitemap=False
    )
    def pricelist(self, promo, **post):
        # Validar el código de promoción si hay restricción
        partner = request.env.user.partner_id
        allowed_pricelist_ids = partner.allowed_pricelist_ids.ids
        if allowed_pricelist_ids and promo:
            max_allowed_id = max(allowed_pricelist_ids)
            pricelist_sudo = (
                request.env["product.pricelist"]
                .sudo()
                .search([("code", "=", promo)], limit=1)
            )
            if pricelist_sudo and pricelist_sudo.id > max_allowed_id:
                redirect = post.get("r", "/shop/cart")
                return request.redirect(f"{redirect}?code_not_available=1")

        return super(WebsiteSaleRestrictedPricelists, self).pricelist(promo, **post)

    def _prepare_product_values(self, product, category, search, **kwargs):
        values = super(WebsiteSaleRestrictedPricelists, self)._prepare_product_values(
            product, category, search, **kwargs
        )

        # Asegurar que el pricelist esté permitido si hay restricción
        partner = request.env.user.partner_id
        allowed_pricelist_ids = partner.allowed_pricelist_ids.ids
        if allowed_pricelist_ids:
            max_allowed_id = max(allowed_pricelist_ids)
            current_pricelist = values["pricelist"]
            available_pricelists = (
                request.env["product.pricelist"]
                .sudo()
                .search(
                    [
                        ("website_id", "in", (False, request.website.id)),
                        ("selectable", "=", True),
                        ("id", "<=", max_allowed_id),
                    ]
                )
            )
            if current_pricelist.id > max_allowed_id:
                values["pricelist"] = (
                    available_pricelists[0]
                    if available_pricelists
                    else request.website.get_current_pricelist()
                )
                # Actualizar la sesión y el pedido con la lista válida
                request.session["website_sale_current_pl"] = values["pricelist"].id
                request.website.sale_get_order(update_pricelist=True)
            values["website_sale_pricelists"] = available_pricelists

        return values
