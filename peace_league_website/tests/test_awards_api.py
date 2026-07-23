"""
Unit tests for peace_league_website.api_awards

Seams under test:
1. verify_turnstile() — token validation paths
2. create_nomination() — field validation, Turnstile gate
3. cast_vote() — rate limiting

CRITICAL: frappe.request is a werkzeug LocalProxy that raises 'object is not bound'
when accessed outside a request context. We bypass this by directly manipulating
frappe.__dict__['request'] instead of using patch(), which would need getattr.

Run with: bench --site <site> run-tests --module peace_league_website.tests.test_awards_api
"""

import unittest
from unittest.mock import patch, MagicMock

import requests as _requests  # ensure in sys.modules for patch('requests.post')
import frappe
from frappe.tests import IntegrationTestCase

import peace_league_website.api_awards as api

MOD = 'peace_league_website.api_awards'


def _bind_request(**attrs):
    """Replace frappe.request (LocalProxy) with a MagicMock via __dict__.
    
    Returns a cleanup function. Bypasses patch() so getattr(frappe, 'request')
    returns the mock instead of the LocalProxy, avoiding 'object is not bound'.
    """
    bak = frappe.__dict__.get('request')
    mock = MagicMock()
    for k, v in attrs.items():
        setattr(mock, k, v)
    # Use MagicMock for .files so patch() can replace .files.get
    # (real dict's .get is read-only and patch on dict methods raises AttributeError)
    if 'files' not in attrs:
        mock.files = MagicMock()
    frappe.__dict__['request'] = mock

    def cleanup():
        if bak is not None:
            frappe.__dict__['request'] = bak
        else:
            del frappe.__dict__['request']

    return cleanup


class TestTurnstileVerification(IntegrationTestCase):
    """Token validation — 6 paths. Uses _bind_request for remoteip tests."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_verify_skips_when_no_secret(self):
        with patch.object(api, 'TURNSTILE_SECRET_KEY', ''):
            self.assertTrue(api.verify_turnstile('token'))

    def test_verify_fails_when_token_missing(self):
        with patch.object(api, 'TURNSTILE_SECRET_KEY', '0x4-key'):
            self.assertFalse(api.verify_turnstile(''))

    def test_verify_fails_when_token_none(self):
        with patch.object(api, 'TURNSTILE_SECRET_KEY', '0x4-key'):
            self.assertFalse(api.verify_turnstile(None))

    def test_verify_passes_on_valid_response(self):
        cleanup = _bind_request(remote_addr='192.168.1.1')
        self.addCleanup(cleanup)
        with patch.object(api, 'TURNSTILE_SECRET_KEY', '0x4-key'):
            with patch('requests.post') as mock_post:
                mock_post.return_value.json.return_value = {'success': True}
                self.assertTrue(api.verify_turnstile('valid'))
                mock_post.assert_called_once()
                args = mock_post.call_args
                self.assertIn('siteverify', args[0][0])
                self.assertEqual(args[1]['data']['secret'], '0x4-key')
                self.assertEqual(args[1]['data']['response'], 'valid')

    def test_verify_fails_on_cloudflare_error(self):
        cleanup = _bind_request(remote_addr='192.168.1.1')
        self.addCleanup(cleanup)
        with patch.object(api, 'TURNSTILE_SECRET_KEY', '0x4-key'):
            with patch('requests.post') as mock_post:
                mock_post.return_value.json.return_value = {
                    'success': False, 'error-codes': ['invalid-input-response']}
                self.assertFalse(api.verify_turnstile('bad'))

    def test_verify_passes_on_network_timeout(self):
        cleanup = _bind_request(remote_addr='192.168.1.1')
        self.addCleanup(cleanup)
        with patch.object(api, 'TURNSTILE_SECRET_KEY', '0x4-key'):
            with patch('requests.post') as mock_post:
                mock_post.side_effect = Exception('timeout')
                self.assertTrue(api.verify_turnstile('token'))


class TestNominationSecurity(IntegrationTestCase):
    """Field validation — uses _bind_request at class level so frappe.request.files works."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Bind a mock request so frappe.request.files can be patched without triggering LocalProxy
        cls._req_cleanup = _bind_request(remote_addr='127.0.0.1', headers={})

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, '_req_cleanup'):
            cls._req_cleanup()
        super().tearDownClass()

    def _patches(self, form_overrides, has_photo=True):
        """Return form_dict patch + optional files.get patch (now safe because __dict__ bypasses LocalProxy)."""
        base = {
            'nominee_name': 'Test', 'category': 'test-cat',
            'description': 'Good work.', 'terms': '1', 'public_consent': '1',
        }
        base.update(form_overrides)
        ctx = [patch(f'{MOD}.frappe.form_dict', base)]
        if has_photo:
            photo = MagicMock()
            photo.read.return_value = b'img'
            photo.filename = 't.jpg'
            ctx.append(patch(f'{MOD}.frappe.request.files.get',
                             return_value=photo, create=True))
        return ctx

    def test_requires_name(self):
        [fd] = self._patches({'nominee_name': ''}, has_photo=False)
        with fd:
            self.assertEqual(api.create_nomination()['status'], 'error')

    def test_requires_category(self):
        [fd] = self._patches({'category': ''}, has_photo=False)
        with fd:
            self.assertEqual(api.create_nomination()['status'], 'error')

    def test_requires_description(self):
        [fd] = self._patches({'description': ''}, has_photo=False)
        with fd:
            self.assertEqual(api.create_nomination()['status'], 'error')

    def test_requires_photo(self):
        [fd] = self._patches({}, has_photo=False)
        with fd:
            self.assertEqual(api.create_nomination()['status'], 'error')

    def test_requires_terms(self):
        [fd, pf] = self._patches({'terms': ''})
        with fd, pf:
            self.assertEqual(api.create_nomination()['status'], 'error')

    def test_requires_consent(self):
        [fd, pf] = self._patches({'public_consent': ''})
        with fd, pf:
            self.assertEqual(api.create_nomination()['status'], 'error')

    def test_rejects_long_description(self):
        [fd] = self._patches({'description': 'x' * 501}, has_photo=False)
        with fd:
            self.assertEqual(api.create_nomination()['status'], 'error')

    def test_turnstile_blocks_when_configured(self):
        with patch.object(api, 'TURNSTILE_SECRET_KEY', '0x4-key'):
            with patch(f'{MOD}.frappe.db.get_value',
                       return_value='Real Category', create=True):
                [fd, pf] = self._patches(
                    {'cf-turnstile-response': ''}, has_photo=True)
                with fd, pf:
                    result = api.create_nomination()
                    self.assertEqual(result['status'], 'error')


class TestVoteSecurity(IntegrationTestCase):
    """Vote rate limiting — cast_vote needs frappe.request which _bind_request provides."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._req_cleanup = _bind_request(remote_addr='10.0.0.200',
                                          headers={'User-Agent': 'pytest'})

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, '_req_cleanup'):
            cls._req_cleanup()
        super().tearDownClass()

    def test_rate_limit_after_20_attempts(self):
        # Mock TURNSTILE_SECRET_KEY to empty so verify_turnstile() passes (dev fallback)
        # Mock now() to return a datetime (has .timestamp()) + cache.get to return 20
        mock_now = MagicMock()
        mock_now.timestamp.return_value = 1_700_000_000
        with patch.object(api, 'TURNSTILE_SECRET_KEY', ''):
            with patch(f'{MOD}.now', return_value=mock_now, create=True):
                with patch(f'{MOD}.frappe.cache.get', return_value=20, create=True):
                    result = api.cast_vote(nominee_id='x', category_slug='y')
                    self.assertEqual(result['status'], 'error')
                    self.assertIn('Too many', result.get('message', ''))


if __name__ == '__main__':
    unittest.main()
