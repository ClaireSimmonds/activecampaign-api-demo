import request_builders


def create_mailing_list(name, address, country):
    request = request_builders.ListAddRequest(
        name,
        address,
        country
    )

    response = request.make_post_request()
    return response.id


def create_contact(email, name_first, name_last, mailing_list_id):
    request = request_builders.ContactAddRequest(email, [mailing_list_id], first_name=name_first, last_name=name_last)

    response = request.make_post_request()
    return response.id


def create_html_message(mailing_list_id, subject, message_content, from_email, from_name, reply2):
    request = request_builders.BasicHTMLMessageAddRequest(
        [mailing_list_id],
        subject,
        message_content,
        from_email=from_email,
        from_name=from_name,
        reply2=reply2
    )

    response = request.make_post_request()
    return response.id


def create_single_campaign(name, send_date, mailing_list_id, message_id):
    request = request_builders.CampaignCreateRequest('single', name, send_date, [mailing_list_id], message_id)

    response = request.make_post_request()
    return response.id
