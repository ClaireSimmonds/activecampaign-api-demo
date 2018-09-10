import responses
from unittest import TestCase
from unittest.mock import patch

from activecampaign.api import ActiveCampaignAPI
from activecampaign.exc import ActiveCampaignResponseError

from config import config


class ActiveCampaignAPITestCase(TestCase):
    def setUp(self):
        config['AC_API_KEY'] = 'mysupersecretkey'
        config['AC_BASE_URL'] = 'https://myaccount.api-us1.com'

        self.api = ActiveCampaignAPI()


class ActiveCampaignAPIMockedRequestTestCase(ActiveCampaignAPITestCase):
    def setUp(self):
        super().setUp()
        self.mock_make_post_request = patch.object(self.api, '_make_post_request', return_value={'id': 1}).start()

    def doCleanups(self):
        self.mock_make_post_request.stop()


class ActiveCampaignAPIInitTestCase(ActiveCampaignAPITestCase):
    def test_values_set_from_config(self):
        self.assertEqual(self.api.base_url, 'https://myaccount.api-us1.com')
        self.assertEqual(self.api.request_url, 'https://myaccount.api-us1.com/admin/api.php')
        self.assertEqual(self.api.api_key, 'mysupersecretkey')
        self.assertEqual(self.api.api_output, 'json')


class ActiveCampaignAPIParamsTestCase(ActiveCampaignAPITestCase):
    def test_return_value(self):
        self.assertDictEqual(self.api.params, {'api_key': 'mysupersecretkey', 'api_output': 'json'})


class ActiveCampaignAPICreateMailingListTestCase(ActiveCampaignAPIMockedRequestTestCase):
    def setUp(self):
        super().setUp()
        self.sender = sender_data = {
            'name': 'test person',
            'address': '123 S Fake St',
            'city': 'Chicago',
            'zip': '60606',
            'country': 'us'
        }

    def test_expected_call_args(self):
        self.api.create_mailing_list('test list', self.sender)
        expected_post_body = {
            'name': 'test list',
            'sender_name': 'test person',
            'sender_addr1': '123 S Fake St',
            'sender_city': 'Chicago',
            'sender_zip': '60606',
            'sender_country': 'us'
        }
        self.mock_make_post_request.assert_called_once_with('list_add', expected_post_body)

    def test_returns_id(self):
        self.assertEqual(self.api.create_mailing_list('test list', self.sender), 1)


class ActiveCampaignAPICreateContactTestCase(ActiveCampaignAPIMockedRequestTestCase):
    def test_expected_call_args(self):
        self.api.create_contact('person@example.com', [1])
        expected_post_body = {
            'email': 'person@example.com',
            'p[1]': 1
        }
        self.mock_make_post_request.assert_called_once_with('contact_add', expected_post_body)

    def test_optional_arguments_included(self):
        self.api.create_contact('person@example.com', [1], 'Person', 'Test')
        expected_post_body = {
            'email': 'person@example.com',
            'first_name': 'Person',
            'last_name': 'Test',
            'p[1]': 1,
        }
        self.mock_make_post_request.assert_called_once_with('contact_add', expected_post_body)

    def test_returns_id(self):
        self.assertEqual(self.api.create_contact('person@example.com', [1]), 1)


class ActiveCampaignAPICreateHTMLMessageTestCase(ActiveCampaignAPIMockedRequestTestCase):
    def test_expected_call_args(self):
        self.api.create_html_message(
            [1],
            'test',
            '<html><body>test</body></html>',
            'test@example.com',
            'Test Person',
            'test@example.com'
        )

        expected_post_body = {
            'subject': 'test',
            'fromemail': 'test@example.com',
            'fromname': 'Test Person',
            'reply2': 'test@example.com',
            'html': '<html><body>test</body></html>',
            'priority': 3,
            'format': 'html',
            'htmlconstructor': 'editor',
            'charset': 'utf-8',
            'encoding': 'quoted-printable',
            'p[1]': 1
        }

        self.mock_make_post_request.assert_called_once_with('message_add', expected_post_body)

    def test_optional_priority(self):
        self.api.create_html_message(
            [1],
            'test',
            '<html><body>test</body></html>',
            'test@example.com',
            'Test Person',
            'test@example.com',
            priority=1
        )

        expected_post_body = {
            'subject': 'test',
            'fromemail': 'test@example.com',
            'fromname': 'Test Person',
            'reply2': 'test@example.com',
            'html': '<html><body>test</body></html>',
            'priority': 1,
            'format': 'html',
            'htmlconstructor': 'editor',
            'charset': 'utf-8',
            'encoding': 'quoted-printable',
            'p[1]': 1
        }

        self.mock_make_post_request.assert_called_once_with('message_add', expected_post_body)

    def test_returns_id(self):
        rval = self.api.create_html_message(
            [1],
            'test',
            '<html><body>test</body></html>',
            'test@example.com',
            'Test Person',
            'test@example.com',
        )
        self.assertEqual(rval, 1)


class ActiveCampaignAPICreateSingleCampaignTestCase(ActiveCampaignAPIMockedRequestTestCase):
    def test_expected_call_args(self):
        self.api.create_single_campaign('Test Campaign', '2018-09-09 13:00:00', [1], 1)

        expected_post_body = {
            'type': 'single',
            'name': 'Test Campaign',
            'sdate': '2018-09-09 13:00:00',
            'status': 1,
            'public': 1,
            'tracklinks': 'all',
            'p[1]': 1,
            'm[1]': 100
        }

        self.mock_make_post_request.assert_called_once_with('campaign_create', expected_post_body)

    def test_returns_id(self):
        self.assertEqual(self.api.create_single_campaign('Test Campaign', '2018-09-09 13:00:00', [1], 1), 1)


class ActiveCampaignAPIMakePostRequestTestCase(ActiveCampaignAPITestCase):
    @responses.activate
    def test_request_structure(self):
        expected_params = {
            'api_action': 'some_action',
            'api_key': 'mysupersecretkey',
            'api_output': 'json'
        }

        expected_body = {'key1': 'value1'}

        responses.add(
            responses.POST,
            self.api.request_url,
            json={'id': 1, 'result_code': 1, 'result_message': 'testing'},
            status=200
        )

        with patch('requests.post') as mock_post:
            self.api._make_post_request('some_action', expected_body)

        mock_post.assert_called_once_with(self.api.request_url, params=expected_params, data=expected_body)

    @responses.activate
    def test_raises_error_if_response_code_falsey(self):
        expected_response = {'id': 1, 'result_code': 0, 'result_message': 'error'}

        responses.add(
            responses.POST,
            self.api.request_url,
            json=expected_response,
            status=200
        )

        with self.assertRaisesRegex(ActiveCampaignResponseError, 'error'):
            self.api._make_post_request('some_action', {'key1': 'value1'})

    @responses.activate
    def test_returns_response(self):
        expected_response = {'id': 1, 'result_code': 1, 'result_message': 'testing'}

        responses.add(
            responses.POST,
            self.api.request_url,
            json=expected_response,
            status=200
        )

        response = self.api._make_post_request('some_action', {'key1': 'value1'})
        self.assertDictEqual(response, expected_response)


class ActiveCampaignAPIFormatMailingListsTestCase(ActiveCampaignAPITestCase):
    def test_return_value_formatted(self):
        body_formatted = self.api._format_mailing_lists([1, 2], {'key1': 'value1'})
        self.assertDictEqual(body_formatted, {'key1': 'value1', 'p[1]': 1, 'p[2]': 2})
