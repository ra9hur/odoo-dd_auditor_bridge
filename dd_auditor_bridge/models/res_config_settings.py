from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cfg_enable_dd_auditor = fields.Boolean(
        string="Enable D&D Auditor Integration",
        config_parameter='dd_auditor_bridge.enable_dd_auditor',
        default=False,
    )
    dd_hmac_secret = fields.Char(
        string="D&D Auditor HMAC Secret",
        help="Shared HMAC secret. Must match ODOO_HMAC_SECRET in the D&D Auditor backend.",
        config_parameter='dd_auditor_bridge.hmac_secret',
    )
    dd_app_url = fields.Char(
        string="D&D Auditor App URL",
        help="Base URL of the D&D Auditor API, e.g. https://dd-auditor-api.onrender.com",
        config_parameter='dd_auditor_bridge.app_url',
    )