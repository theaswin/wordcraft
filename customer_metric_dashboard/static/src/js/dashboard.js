/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class CustomerMetricDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.session = useService("session");

        this.state = useState({
            user_data: {
                name: "",
                job_title: "",
                image_url: ""
            },
            metrics_data: {
                customer_count: 0,
                payment_amount: "SAR 0.00",
                quotation_count: 0,
                quotation_amount: "SAR 0.00",
                sale_count: 0,
                sale_amount: "SAR 0.00",
                paid_invoice_count: 0,
                paid_invoice_amount: "SAR 0.00",
                unpaid_invoice_count: 0,
                unpaid_invoice_amount: "SAR 0.00",
                payment_count: 0,
            },
        });

        onWillStart(async () => {
            await this._fetch_metrics_data();
        });
    }

    async _fetch_metrics_data() {
        try {
            const res = await this.orm.call("customer.metric.dashboard", "get_dashboard_data", []);
            this.state.metrics_data = res;
            this.state.user_data = {
                name: res.user_name,
                job_title: res.user_job_title,
                image_url: `/web/image?model=res.partner&id=${res.user_partner_id}&field=image_1920`
            };
        } catch (error) {
            console.error("Error fetching dashboard data:", error);
        }
    }

    _onDashboardActionClick(ev) {
        const target = ev.currentTarget;
        const model = target.dataset.model;
        const domainStr = target.getAttribute('data-domain') || '[]';
        const title = target.dataset.name;

        // Replace placeholder with actual UID and parse string to array
        const domain = JSON.parse(domainStr.replace(/USER_ID/g, this.session.user_context.uid || this.session.uid));

        this.action.doAction({
            name: title,
            type: 'ir.actions.act_window',
            res_model: model,
            domain: domain,
            views: [[false, 'list'], [false, 'form']],
            target: 'current'
        });
    }
}

CustomerMetricDashboard.template = "customer_metric_dashboard.CustomerMetricDashboardTemplate";

registry.category("actions").add("customer_metric_dashboard_tag", CustomerMetricDashboard);
