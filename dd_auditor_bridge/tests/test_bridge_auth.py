import hashlib
import hmac

from odoo.tests import common


class TestBridgeAuth(common.TransactionCase):

    def test_canonical_format(self):
        """Canonical payload must follow the exact v=1|org|email|ts contract."""
        canonical = self.env['account.move']._build_dd_auditor_canonical(7, 'bob@example.com', '1700000000')
        self.assertEqual(canonical, 'v=1|7|bob@example.com|1700000000')

    def test_hmac_is_sha256_hexdigest(self):
        """HMAC must be a deterministic SHA-256 hexdigest of the canonical payload."""
        secret = 'super-secret'
        canonical = 'v=1|7|bob@example.com|1700000000'
        token = self.env['account.move']._compute_dd_auditor_hmac(secret, canonical)

        expected = hmac.new(
            secret.encode(), canonical.encode(), hashlib.sha256
        ).hexdigest()

        self.assertEqual(token, expected)
        self.assertEqual(len(token), 64)

    def test_hmac_changes_with_secret(self):
        """A different secret must produce a different token."""
        canonical = 'v=1|7|bob@example.com|1700000000'
        token_a = self.env['account.move']._compute_dd_auditor_hmac('secret-a', canonical)
        token_b = self.env['account.move']._compute_dd_auditor_hmac('secret-b', canonical)
        self.assertNotEqual(token_a, token_b)

    def test_hmac_changes_with_payload(self):
        """A different canonical payload must produce a different token."""
        secret = 'super-secret'
        token_a = self.env['account.move']._compute_dd_auditor_hmac(
            secret, 'v=1|7|bob@example.com|1700000000')
        token_b = self.env['account.move']._compute_dd_auditor_hmac(
            secret, 'v=1|8|bob@example.com|1700000000')
        self.assertNotEqual(token_a, token_b)
