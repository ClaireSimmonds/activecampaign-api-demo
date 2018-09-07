import requests

from config import config


API_PATH = '/admin/api.php'


class ActiveCampaignRequest:

    def __init__(self):
        self.base_url = config['AC_BASE_URL']
        self.request_url = self.base_url + API_PATH
        self.api_key = config['AC_API_KEY']
        self.api_output = config['OUTPUT_FORMAT']
        self.api_action = None

    @property
    def request_params(self):
        return {
            'api_key': self.api_key,
            'api_output': self.api_output,
            'api_action': self.api_action
        }

    @property
    def post_body(self):
        return {}

    @staticmethod
    def _format_mailing_lists(mailing_list_ids, body):
        for list_id in mailing_list_ids:
            body['p[{}]'.format(list_id)] = list_id

        return body

    def make_post_request(self):
        return requests.post(self.request_url, params=self.request_params, data=self.post_body)


class ListAddRequest(ActiveCampaignRequest):

    def __init__(self, name, sender_address, sender_country):
        super().__init__()
        self.api_action = 'list_add'
        self.name = name
        self.sender_address = sender_address
        self.sender_country = sender_country

    @property
    def post_body(self):
        return {
            'name': self.name,
            'sender_addr1': self.sender_address,
            'sender_country': self.sender_country
        }


class ContactAddRequest(ActiveCampaignRequest):

    def __init__(self, email, mailing_lists, first_name=None, last_name=None):
        super().__init__()
        self.api_action = 'contact_add'
        self.email = email
        self.mailing_lists = mailing_lists
        self.first_name = first_name
        self.last_name = last_name

    @property
    def post_body(self):
        body = {
            'email': self.email,
        }

        body.update(self._format_mailing_lists(self.mailing_lists, body))

        if self.first_name:
            body['first_name'] = self.first_name

        if self.last_name:
            body['last_name'] = self.last_name

        return body


class MessageAddRequest(ActiveCampaignRequest):

    def __init__(
            self,
            mailing_lists,
            subject,
            fromemail,
            fromname,
            reply2,
            priority=3,
            charset='utf-8',
            encoding='quoted-printable'
    ):
        super().__init__()
        self.api_action = 'message_add'
        self.mailing_lists = mailing_lists
        self.subject = subject
        self.fromemail = fromemail
        self.fromname = fromname
        self.reply2 = reply2
        self.priority = priority
        self.charset = charset
        self.encoding = encoding

    @property
    def post_body(self):
        body = {
            'subject': self.subject,
            'fromemail': self.fromemail,
            'fromname': self.fromname,
            'reply2': self.reply2,
            'priority': self.priority,
            'charset': self.charset,
            'encoding': self.encoding
        }

        body.update(self._format_mailing_lists(self.mailing_lists, body))

        return body


class BasicHTMLMessageAddRequest(MessageAddRequest):

    def __init__(self, mailing_lists, subject, fromemail, fromname, reply2, html_content, **kwargs):
        super().__init__(mailing_lists, subject, fromemail, fromname, reply2, **kwargs)
        self.html = html_content

    @property
    def post_body(self):
        body = super().post_body
        body['format'] = 'html'
        body['htmlconstructor'] = 'editor'
        body['html'] = self.html

        return body


class CampaignCreateRequest(ActiveCampaignRequest):

    def __init__(self, campaign_type, name, send_date, mailing_lists, message, status=1, public=1, track_links='all'):
        self.api_action = 'campaign_create'
        self.type = campaign_type
        self.name = name
        self.send_date = send_date
        self.mailing_lists = mailing_lists
        self.msg = message
        self.status = status
        self.public = public
        self.track_links = track_links

    @property
    def post_body(self):
        body = {
            'type': self.type,
            'name': self.name,
            'sdate': self.send_date,
            'status': self.status,
            'public': self.public,
            'tracklinks': self.track_links,
        }

        body.update(self._format_mailing_lists(self.mailing_lists, body))
        body['m[{}]'.format(self.msg)] = 100

        return body
