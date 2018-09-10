import requests

from activecampaign import exc
from config import config


API_PATH = '/admin/api.php'


class ActiveCampaignAPI:
    def __init__(self):
        """Initializes an ActiveCampaignAPI object with necessary basic configurations"""
        self.base_url = config['AC_BASE_URL']
        self.request_url = self.base_url + API_PATH
        self.api_key = config['AC_API_KEY']
        self.api_output = config['OUTPUT_FORMAT']

    @property
    def params(self):
        """Returns parameters that should be included in all requests

        :return: A dictionary containing request parameters common to all requests
        :rtype: dict
        """
        return {
            'api_key': self.api_key,
            'api_output': self.api_output
        }

    def create_mailing_list(self, name, address, country):
        """Creates a mailing list

        Corresponds to the ActiveCampaign API's `list_add` action.

        :param name: Name to assign the mailing list
        :type name: str
        :param address: Physical address of the sender associated with this mailing list
        :type address: str
        :param country: Country code for the sender associated with this mailing list
        :type country: str

        :return: Returns the id of the created mailing list
        :rtype: int
        """
        body = {
            'name': name,
            'sender_addr1': address,
            'sender_country': country
        }

        response = self._make_post_request('list_add', body)
        return response['id']

    def create_contact(self, email, mailing_lists, first_name=None, last_name=None):
        """Creates a contact and associates with one or more mailing lists

        Corresponds to the ActiveCampaign API's `contact_add` action.

        :param email: Email address of the contact
        :type email: str
        :param mailing_lists: Mailing lists this contact should be associated with
        :type mailing_lists: list[int]
        :param first_name: First name of the contact (optional)
        :type first_name: str
        :param last_name: Last name of the contact (optional)
        :type last_name: str

        :return: Returns the id of the created contact
        :rtype: int
        """

        body = {
            'email': email,
        }

        if first_name:
            body['first_name'] = first_name

        if last_name:
            body['last_name'] = last_name

        body.update(self._format_mailing_lists(mailing_lists, body))

        response = self._make_post_request('contact_add', body)
        return response['id']

    def create_html_message(self, mailing_lists, subject, message_content, from_email, from_name, reply_to, priority=3):
        """Creates a message comprised of HTML content

        Corresponds to the ActiveCampaign API's `message_add` action.

        :param mailing_lists: Mailing lists this message should be associated with
        :type mailing_lists: list[int]
        :param subject: Subject of the email message
        :type subject: str
        :param message_content: HTML content of the email message
        :type message_content: str
        :param from_email: Email address used in the `from` section of the email
        :type from_email: str
        :param from_name: Name used in the `from` section of the email
        :type from_name: str
        :param reply_to: Email address that shoul be used in the `reply-to` section of the email
        :type reply_to: str
        :param priority: Value indicating the priority of the message, 1=high, 5=low
        :type priority: int

        :return: Returns the id of the created message
        :rtype: int
        """
        body = {
            'subject': subject,
            'fromemail': from_email,
            'fromname': from_name,
            'reply2': reply_to,
            'html': message_content,
            'priority': priority,
            'format': 'html',
            'htmlconstructor': 'editor',
            'charset': 'utf-8',
            'encoding': 'quoted-printable'
        }

        body.update(self._format_mailing_lists(mailing_lists, body))

        response = self._make_post_request('message_add', body)
        return response['id']

    def create_single_campaign(self, name, send_date, mailing_lists, message):
        """Creates a new "single"-type Campaign

        Corresponds to the ActiveCampaign API's `campaign_create` action.

        :param name: Name of the campaign
        :type name: str
        :param send_date: Date string (format: YYYY-MM-DD hh:mm:ss) representing the date and time the campaign should
            be sent
        :type send_date: str
        :param mailing_lists: Mailing lists that the campaign should be directed to
        :type mailing_lists: list[int]
        :param message: Message to be sent as part of the campaign
        :type message: int

        :return: Returns the id of the created campaign
        :rtype: int
        """
        body = {
            'type': 'single',
            'name': name,
            'sdate': send_date,
            'status': 1,
            'public': 1,
            'tracklinks': 'all',
        }

        body.update(self._format_mailing_lists(mailing_lists, body))
        body['m[{}]'.format(message)] = 100

        response = self._make_post_request('campaign_create', body)
        return response['id']

    def _make_post_request(self, action, body):
        """Submits a POST request to the ActiveCampaign API

        :param action: API action to be performed
        :type action: str
        :param body: POST body
        :type body: str

        :return: Returns the JSON response body for the submitted POST request
        :rtype: dict

        :raises exc.ActiveCampaignResponseError: if the returned JSON data's `result_message` attribute evaluates to a
            False-y value
        """
        params = {'api_action': action}
        params.update(self.params)

        response = requests.post(self.request_url, params=params, data=body)
        response_body = response.json()

        if not response_body['result_code']:
            raise exc.ActiveCampaignResponseError(response_body['result_message'])
        else:
            return response_body

    @staticmethod
    def _format_mailing_lists(mailing_list_ids, body):
        """Formats mailing list attributes for submission to the ActiveCampaign API

        :param mailing_list_ids: Mailing list IDs to be converted to the proper ActiveCampaign submission format
        :type mailing_list_ids: list[int]
        :param body: POST body that the formatted IDs should be added to
        :type body: dict

        :return: Returns the modified POST body, including mailing list IDs
        :rtype: dict
        """
        for list_id in mailing_list_ids:
            body['p[{}]'.format(list_id)] = list_id

        return body
