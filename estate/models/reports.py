from odoo import api, models


class EstatePropertyReport(models.AbstractModel):
    _name = 'report.estate.report_property_view'
    _description = ''

    @api.model
    def _get_report_values(self, docids, data=None):
        print('the report fired')
        docs = self.env['estate.property'].browse(docids)
        return {
            'doc_ids': [docs.ids],
            'doc_model': '',
            'docs': docs,
            'data': [data],  # You can include additional data here
        }