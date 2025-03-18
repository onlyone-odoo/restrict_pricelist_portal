# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo import _  # Importamos _ desde odoo
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
        response = super(WebsiteSaleRestrictedPricelists, self).shop(
            page=page,
            category=category,
            search=search,
            min_price=min_price,
            max_price=max_price,
            ppg=ppg,
            **post,
        )

        partner = request.env.user.partner_id
        allowed_pricelist_ids = partner.allowed_pricelist_ids.ids
        if allowed_pricelist_ids:
            max_allowed_id = max(allowed_pricelist_ids)
            current_pricelist = response.qcontext["pricelist"]
            if current_pricelist.id > max_allowed_id:
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
                response.qcontext["pricelist"] = (
                    available_pricelists[0]
                    if available_pricelists
                    else request.website.get_current_pricelist()
                )
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
        partner = request.env.user.partner_id
        allowed_pricelist_ids = partner.allowed_pricelist_ids.ids
        if allowed_pricelist_ids:
            max_allowed_id = max(allowed_pricelist_ids)
            if pricelist.id > max_allowed_id:
                request.session["website_sale_warning"] = (
                    _(
                        "No tiene habilitada la lista de precios '%s'. Por favor, seleccione una lista permitida."
                    )
                    % pricelist.name
                )
                return request.redirect(post.get("r", "/shop"))

        if "website_sale_warning" in request.session:
            del request.session["website_sale_warning"]
        return super(WebsiteSaleRestrictedPricelists, self).pricelist_change(
            pricelist, **post
        )

    @http.route(
        ["/shop/pricelist"], type="http", auth="public", website=True, sitemap=False
    )
    def pricelist(self, promo, **post):
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
                request.session["website_sale_warning"] = _(
                    "El código '%s' corresponde a la lista de precios '%s', que no tiene habilitada."
                ) % (promo, pricelist_sudo.name)
                redirect = post.get("r", "/shop/cart")
                return request.redirect(f"{redirect}?code_not_available=1")

        if "website_sale_warning" in request.session:
            del request.session["website_sale_warning"]
        return super(WebsiteSaleRestrictedPricelists, self).pricelist(promo, **post)

    def _prepare_product_values(self, product, category, search, **kwargs):
        values = super(WebsiteSaleRestrictedPricelists, self)._prepare_product_values(
            product, category, search, **kwargs
        )

        partner = request.env.user.partner_id
        allowed_pricelist_ids = partner.allowed_pricelist_ids.ids
        if allowed_pricelist_ids:
            max_allowed_id = max(allowed_pricelist_ids)
            current_pricelist = values["pricelist"]
            if current_pricelist.id > max_allowed_id:
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
                values["pricelist"] = (
                    available_pricelists[0]
                    if available_pricelists
                    else request.website.get_current_pricelist()
                )
                request.session["website_sale_current_pl"] = values["pricelist"].id
                request.website.sale_get_order(update_pricelist=True)

        return values
