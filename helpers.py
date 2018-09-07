import request_builders


def create_mailing_list(name, address, country):
    request = request_builders.ListAddRequest(
        name,
        address,
        country
    )

    _, response = request.make_post_request()

    if response['result_code']:
        return response['id']
    else:
        raise Exception(response['result_message'])


def create_contact(email, name_first, name_last, mailing_list_id):
    request = request_builders.ContactAddRequest(email, [mailing_list_id], first_name=name_first, last_name=name_last)

    _, response = request.make_post_request()

    if response['result_code']:
        return response['id']
    else:
        raise Exception(response['result_message'])


def create_html_message(mailing_list_id, subject, message_content, from_email, from_name, reply2):
    request = request_builders.BasicHTMLMessageAddRequest(
        [mailing_list_id],
        subject,
        message_content,
        from_email=from_email,
        from_name=from_name,
        reply2=reply2
    )

    _, response = request.make_post_request()

    if response['result_code']:
        return response['id']
    else:
        raise Exception(response['result_message'])


def create_single_campaign(name, send_date, mailing_list_id, message_id):
    request = request_builders.CampaignCreateRequest('single', name, send_date, [mailing_list_id], message_id)

    _, response = request.make_post_request()

    if response['result_code']:
        return response['id']
    else:
        raise Exception(response['result_message'])
