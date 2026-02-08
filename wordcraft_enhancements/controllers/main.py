from odoo import http
from odoo.http import request
import requests
import logging

_logger = logging.getLogger(__name__)


class WordcraftSaleFetch(http.Controller):

    @http.route(
        "/api/fetch/sale_orders",
        type="json",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def fetch_sale_orders(self, limit=5, offset=0):

        ODOO_URL = "https://erp.wordcraftgroup.com/jsonrpc"
        DB = "wordcraftgroup"
        USERNAME = "9895569340"
        PASSWORD = "123456"

        # ------------------------------------------------
        # 1️⃣ LOGIN
        # ------------------------------------------------
        login_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "login",
                "args": [DB, USERNAME, PASSWORD]
            },
            "id": 1
        }

        uid = requests.post(ODOO_URL, json=login_payload, timeout=3000).json().get("result")
        if not uid:
            return {"error": "Login failed"}

        _logger.info("✅ Logged in | uid=%s", uid)

        # ------------------------------------------------
        # 2️⃣ GET ALL SALE.ORDER FIELDS
        # ------------------------------------------------
        fields_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    DB,
                    uid,
                    PASSWORD,
                    "sale.order",
                    "fields_get",
                    [],
                    {"attributes": ["type"]}
                ]
            }
        }

        sale_order_fields = list(
            requests.post(ODOO_URL, json=fields_payload, timeout=3000)
            .json()
            .get("result", {})
            .keys()
        )

        # ------------------------------------------------
        # 3️⃣ FETCH SALE ORDERS (ALL FIELDS)
        # ------------------------------------------------
        orders_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    DB,
                    uid,
                    PASSWORD,
                    "sale.order",
                    "search_read",
                    [
                        [["invoice_status", "in", ["no", "to invoice"]]],
                        sale_order_fields
                    ]
                ],
                "kwargs": {
                    "limit": limit,
                    "offset": offset,
                    "order": "id asc"
                }
            },
            "id": 2
        }

        sale_orders = requests.post(
            ODOO_URL, json=orders_payload, timeout=3000
        ).json().get("result", [])

        _logger.info("📦 Sale orders fetched: %s", len(sale_orders))

        # ------------------------------------------------
        # 4️⃣ GET ALL SALE.ORDER.LINE FIELDS
        # ------------------------------------------------
        line_fields_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    DB,
                    uid,
                    PASSWORD,
                    "sale.order.line",
                    "fields_get",
                    [],
                    {"attributes": ["type"]}
                ]
            }
        }

        sale_line_fields = list(
            requests.post(ODOO_URL, json=line_fields_payload, timeout=3000)
            .json()
            .get("result", {})
            .keys()
        )

        # ------------------------------------------------
        # 5️⃣ FETCH ORDER LINES FOR EACH ORDER
        # ------------------------------------------------
        final_result = []

        for order in sale_orders:

            lines_payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute_kw",
                    "args": [
                        DB,
                        uid,
                        PASSWORD,
                        "sale.order.line",
                        "search_read",
                        [
                            [["order_id", "=", order["id"]]],
                            sale_line_fields
                        ]
                    ]
                }
            }

            order_lines = requests.post(
                ODOO_URL, json=lines_payload, timeout=3000
            ).json().get("result", [])

            full_order = {
                "sale_order": order,
                "order_lines": order_lines
            }

            final_result.append(full_order)

            # ------------------------------------------------
            # 6️⃣ PRINT FULL DATA IN TERMINAL
            # ------------------------------------------------
            
            print("========================================")
            for i in final_result:
                print(i)
                break

