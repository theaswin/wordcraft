import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape

class XLSXReportController(http.Controller):
    @http.route('/xlsx_reports', type='http', auth='user', csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_name, token='ads'):
        """ Return data to python file passed from the javascript"""
        session_unique_id = request.session.uid
        report_object = request.env[model].with_user(session_unique_id)
        options = json.loads(options)
        try:
            if output_format == 'xlsx':
                xlsx_data = report_object.get_xlsx_report(options)
                response = request.make_response(
                    xlsx_data,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition', content_disposition(f"{report_name}.xlsx"))
                    ]
                )
                response.set_cookie('fileToken', token)
                return response
        except Exception as e:
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': str(e)
            }
            return request.make_response(html_escape(json.dumps(error)))
