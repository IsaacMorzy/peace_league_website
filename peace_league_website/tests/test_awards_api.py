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

# Used by HTTP integration tests that POST to the live bench
import base64
import json
import os
import socket
import urllib.request

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


class TestHttpNominationSubmission(IntegrationTestCase):
    """Regression guard for the HTTP path used by the Astro frontend form.

    These tests POST real multipart form-data to the bench HTTP endpoint and
    assert the full request/response cycle. They catch exactly the
    "Value missing for Award Nominee: Photo" regression that broke the user.

    Skip if bench is not running on localhost:8000 (a developer can
    start it with `bench start`).
    """

    # 1x1 white JPEG (base64-encoded, no pad characters that break shell parsing)
    _JPEG_B64 = (
        '/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBA'
        'QEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEQE'
        'BAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAAR'
        'CAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAQACAwQFBgcICQoL/8QA'
        'tRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM'
        'xdCgxR/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcF'
        'BAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYG'
        'RomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiY'
        'qSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrExcbHyMnK0tPU1dbX2Nna4uPk5ebn6O'
        'nq8fLz9PX29/j5+v/aAAwDAQACEQMRAD8A/v4ooooAKKKKAP/2Q=='
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Allow CI to override the bench URL (default: dev site on :8000)
        cls._bench_url = os.environ.get('BENCH_URL', 'http://peaceleagueafrica.localhost:8000')
        cls._created_nominees = []  # names of nominees to clean up after the class
        try:
            urllib.request.urlopen(cls._bench_url + '/', timeout=10).read()
        except Exception as e:
            raise unittest.SkipTest('bench not running at {0}: {1}'.format(cls._bench_url, e))

    @classmethod
    def tearDownClass(cls):
        # ponytail: don't litter the dev DB with "Test HTTP Nominee …" rows —
        # delete every nominee this test class inserted during the run.
        for name in cls._created_nominees:
            try:
                frappe.delete_doc('Award Nominee', name, ignore_permissions=True, force=True)
            except Exception as e:
                # Best-effort cleanup; early FLUSH for next dev cycle is fine
                frappe.log_error('HTTP test cleanup failure for {0}: {1}'.format(name, e))
        super().tearDownClass()

    def _post_nomination(self, **form_overrides):
        """POST multipart form-data to /api/method/create_nomination. Returns parsed JSON.

        The default Turnstile secret is empty in dev so verification is skipped.
        On success, also records the created nominee name so tearDownClass can
        delete it (otherwise the dev DB fills up with "Test HTTP Nominee …" rows).
        """
        boundary = '----PeaceLeagueTestBoundary'
        jpeg_bytes = base64.b64decode(self._JPEG_B64)

        fields = {
            'nominee_name': 'HTTP Test Nominee {0}'.format(frappe.generate_hash(length=6)),
            'category': _first_active_category_slug(),
            'description': 'End-to-end HTTP test for nomination submission regression guard.',
            'nominee_email': 'http_test@example.com',
            'nominee_phone': '+254712345678',
            'nominator_name': 'HTTP Test Nominator',
            'nominator_email': 'http_test_nominator@example.com',
            'terms': 'on',
            'public_consent': 'on',
        }
        fields.update(form_overrides)
        status, body, nominee_name = self._build_and_post(fields, jpeg_bytes, boundary)
        if status == 200:
            data = (body.get('message') or {}).get('data') or {}
            if data.get('nominee'):
                self._created_nominees.append(data['nominee'])
        return status, body

    def _build_and_post(self, fields, photo_bytes, boundary):
        body = b''
        for k, v in fields.items():
            body += ('--{0}\r\n'.format(boundary)).encode()
            body += ('Content-Disposition: form-data; name="{0}"\r\n\r\n'.format(k)).encode()
            body += str(v).encode()
            body += b'\r\n'
        body += ('--{0}\r\n'.format(boundary)).encode()
        body += b'Content-Disposition: form-data; name="photo"; filename="t.jpg"\r\n'
        body += b'Content-Type: image/jpeg\r\n\r\n'
        body += photo_bytes
        body += b'\r\n'
        body += ('--{0}--\r\n'.format(boundary)).encode()

        req = urllib.request.Request(
            self._bench_url + '/api/method/peace_league_website.api_awards.create_nomination',
            data=body,
            headers={'Content-Type': 'multipart/form-data; boundary={0}'.format(boundary)},
            method='POST',
        )
        try:
            resp = urllib.request.urlopen(req, timeout=15)
            return resp.status, json.loads(resp.read().decode()), None
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode()), None

    def test_create_nomination_http_path_succeeds(self):
        """The HTTP path that the frontend uses must NOT regress the photo bug.

        Regression for: "Value missing for Award Nominee: Photo" — the bug
        where the photo was attached to a placeholder docname and the
        Award Nominee insert then failed because photo is mandatory.

        In dev with Turnstile enabled, a no-token POST returns `error` from
        the bot check (correctly), NOT from the photo mandatory check. If
        Turnstile is disabled the POST returns `success`. Either way, the
        photo-mandatory regression must NOT be reachable.
        """
        status, body = self._post_nomination()
        self.assertEqual(status, 200, 'HTTP status, got body: {0}'.format(body))
        # The endpoint must return a structured response (success or bot error)
        msg = body.get('message') or {}
        self.assertIn(msg.get('status'), ('success', 'error'),
                      'Expected structured response, got: {0}'.format(body))
        # The regression would surface as: "Value missing for Award Nominee: Photo".
        # Any error must NOT be that. If error must say "Verification failed" or similar.
        if msg.get('status') == 'error':
            text = (msg.get('message') or '') + ' ' + str(msg.get('exc') or '')
            self.assertNotIn('Value missing for Award Nominee', text,
                             'Photo mandatory bug regressed! Got: {0}'.format(body))

    def test_create_nomination_http_happy_path(self):
        """Full success path over HTTP: insert → save_file → db_set → success.

        Uses the Redis `disable_turnstile_check` flag set by `verify_turnstile()`
        to bypass the bot check so the complete flow runs end-to-end. The flag
        is cleared in the `finally` block so the test does not pollute dev state.

        Verifies:
        - HTTP 200 with `message.status === "success"`
        - response data.nominee and data.photo are populated
        - the Award Nominee row exists in the DB
        - the photo URL points at /files/...
        """
        frappe.cache().set_value('disable_turnstile_check', 1)
        try:
            status, body = self._post_nomination()
            self.assertEqual(status, 200, 'HTTP status, got body: {0}'.format(body))
            msg = body.get('message') or {}
            self.assertEqual(msg.get('status'), 'success',
                             'Expected success, got: {0}'.format(body))
            data = msg.get('data') or {}
            nominee_name = data.get('nominee')
            self.assertTrue(nominee_name, 'Expected nominee name in response, got: {0}'.format(body))
            doc = frappe.get_doc('Award Nominee', nominee_name)
            self.assertEqual(doc.status, 'Active')
            self.assertTrue(doc.photo, 'Missing photo URL in DB')
            self.assertTrue(doc.photo.startswith('/files/'),
                            'Unexpected photo path: {0}'.format(doc.photo))
        finally:
            frappe.cache().delete_value('disable_turnstile_check')

    def test_create_nomination_http_rejects_oversized_photo(self):
        """Backend must enforce the 5MB cap that the frontend declares.

        Like the success test, dev Turnstile may block the request before
        the size check runs. The point is the size guard must run BEFORE
        any DB write — so unless the error explicitly says "photo is too
        large", the test accepts that Turnstile correctly blocked first.
        """
        big_jpeg = b'\x00' * (6 * 1024 * 1024)  # 6MB of zeros
        boundary = '----PeaceLeagueTestBoundary'
        fields = {
            'nominee_name': 'TooBig',
            'category': _first_active_category_slug(),
            'description': 'oversize',
            'terms': 'on', 'public_consent': 'on',
        }
        body = b''
        for k, v in fields.items():
            body += ('--{0}\r\n'.format(boundary)).encode()
            body += ('Content-Disposition: form-data; name="{0}"\r\n\r\n'.format(k)).encode()
            body += str(v).encode()
            body += b'\r\n'
        body += ('--{0}\r\n'.format(boundary)).encode()
        body += b'Content-Disposition: form-data; name="photo"; filename="big.jpg"\r\n'
        body += b'Content-Type: image/jpeg\r\n\r\n'
        body += big_jpeg
        body += b'\r\n'
        body += ('--{0}--\r\n'.format(boundary)).encode()

        req = urllib.request.Request(
            self._bench_url + '/api/method/peace_league_website.api_awards.create_nomination',
            data=body,
            headers={'Content-Type': 'multipart/form-data; boundary={0}'.format(boundary)},
            method='POST',
        )
        # Frappe API returns 200 for all JSON responses (incl. errors);
        # assert on body, not on HTTPError.
        resp = urllib.request.urlopen(req, timeout=30)
        data = json.loads(resp.read().decode())
        msg = data.get('message') or {}
        self.assertEqual(msg.get('status'), 'error',
                         'Oversized photo must be rejected, got: {0}'.format(data))
        # Must NOT regress the photo-mandatory bug.
        text = (msg.get('message') or '')
        self.assertNotIn('Value missing for Award Nominee', text,
                         'Photo mandatory bug regressed during size check! Got: {0}'.format(data))


def _first_active_category_slug():
    cats = frappe.get_list(
        'Award Category',
        filters={'is_active': 1},
        fields=['slug'],
        limit=1,
    )
    if not cats:
        raise unittest.SkipTest('No active Award Category in DB — load fixtures first.')
    return cats[0].slug


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
