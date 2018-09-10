from unittest import TestCase

from activecampaign import exc


class ActiveCampaignResponseErrorTestCase(TestCase):
    def test_type(self):
        self.assertIsInstance(exc.ActiveCampaignResponseError(), Exception)
