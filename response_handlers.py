

class ActiveCampaignResponseError(Exception):
    pass


class ActiveCampaignPostResponse():

    def __init__(self, item_id, result_code, status_code, result_message):
        self.id = item_id
        self.result_code = result_code
        self.status_code = status_code
        self.result_message = result_message

        if not result_code:
            raise ActiveCampaignResponseError(self.result_message)
