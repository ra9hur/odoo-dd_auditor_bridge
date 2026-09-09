import hashlib
import hmac
import time
import werkzeug.urls
from odoo import models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_redirect_to_dd_auditor(self):
        self.ensure_one()
        icp = self.env['ir.config_parameter'].sudo()

        if not icp.get_param('dd_auditor_bridge.enable_dd_auditor'):
            raise UserError("D&D Auditor Integration is disabled by the administrator.")

        secret_key = icp.get_param('dd_auditor_bridge.hmac_secret')
        app_base_url = icp.get_param('dd_auditor_bridge.app_url') or "http://localhost:3001"
        if not secret_key:
            raise UserError("Integration config error: missing HMAC secret key.")

        ts = str(int(time.time()))
        user = self.env.user
        company = self.company_id

        # EXACT canonical payload — must match backend verification
        canonical = f"v=1|{company.id}|{user.email}|{ts}"
        token = hmac.new(secret_key.encode(), canonical.encode(), hashlib.sha256).hexdigest()

        params = {
            'v': '1',
            'token': token,
            'ts': ts,
            'odoo_org_id': str(company.id),
            'odoo_org_name': company.name,
            'email': user.email,
            'name': user.name,
        }

        return {
            'type': 'ir.actions.act_url',
            'url': f"{app_base_url}/api/v1/auth/odoo/callback?{werkzeug.urls.url_encode(params)}",
            'target': 'new',
        }