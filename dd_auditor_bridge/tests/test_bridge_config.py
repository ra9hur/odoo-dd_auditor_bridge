import werkzeug.urls

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged('post_install', '-at_install')
class TestBridgeConfig(AccountTestInvoicingCommon):

    def setUp(self):
        super().setUp()
        self.icp = self.env['ir.config_parameter'].sudo()
        self.bridge_partner = self.env['res.partner'].create({'name': 'D&D Test Vendor'})
        self.move = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.bridge_partner.id,
            'invoice_line_ids': [(0, 0, {
                'name': 'D&D audit line',
                'quantity': 1,
                'price_unit': 120.0,
            })],
        })
        # Ensure a clean, deterministic configuration baseline.
        self.icp.set_param('dd_auditor_bridge.enable_dd_auditor', True)
        self.icp.set_param('dd_auditor_bridge.hmac_secret', 'test-secret')
        self.icp.set_param('dd_auditor_bridge.app_url', 'https://dd-auditor-api.example.com')

    def tearDown(self):
        self.icp.set_param('dd_auditor_bridge.enable_dd_auditor', False)
        self.icp.set_param('dd_auditor_bridge.hmac_secret', False)
        self.icp.set_param('dd_auditor_bridge.app_url', False)
        super().tearDown()

    def test_disabled_integration_raises(self):
        self.icp.set_param('dd_auditor_bridge.enable_dd_auditor', False)
        with self.assertRaises(UserError):
            self.move.action_redirect_to_dd_auditor()

    def test_missing_secret_raises(self):
        self.icp.set_param('dd_auditor_bridge.hmac_secret', False)
        with self.assertRaises(UserError):
            self.move.action_redirect_to_dd_auditor()

    def test_missing_app_url_raises(self):
        # No fallback to localhost: a missing URL must raise a config error.
        self.icp.set_param('dd_auditor_bridge.app_url', False)
        with self.assertRaises(UserError):
            self.move.action_redirect_to_dd_auditor()

    def test_blank_app_url_raises(self):
        # Whitespace-only URL must be treated as missing.
        self.icp.set_param('dd_auditor_bridge.app_url', '   ')
        with self.assertRaises(UserError):
            self.move.action_redirect_to_dd_auditor()

    def test_success_returns_signed_url(self):
        action = self.move.action_redirect_to_dd_auditor()
        self.assertEqual(action['type'], 'ir.actions.act_url')
        self.assertEqual(action['target'], 'new')

        url = action['url']
        self.assertTrue(url.startswith(
            'https://dd-auditor-api.example.com/api/v1/auth/odoo/callback?'
        ))

        query = url.split('?', 1)[1]
        params = werkzeug.urls.url_decode(query)

        # Token must be the exact HMAC of the canonical payload.
        canonical = self.env['account.move']._build_dd_auditor_canonical(
            self.move.company_id.id,
            self.env.user.email,
            params['ts'],
        )
        expected_token = self.env['account.move']._compute_dd_auditor_hmac(
            'test-secret', canonical
        )
        self.assertEqual(params['token'], expected_token)
        self.assertEqual(params['v'], '1')
        self.assertEqual(params['odoo_org_id'], str(self.move.company_id.id))
        self.assertEqual(params['email'], self.env.user.email)
