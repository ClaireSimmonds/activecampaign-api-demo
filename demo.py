import helpers


if __name__ == '__main__':
    # Create mailing list
    mailing_list_id = helpers.create_mailing_list('Demo Mailing List', '123 S Fake St, Chicago, IL 60606', 'us')

    # Add contacts to the mailing list
    contact_data = [
        ('csimmonds814+acdemo1@gmail.com', 'Claire', 'Test1', mailing_list_id),
        ('csimmonds814+acdemo2@gmail.com', 'Claire', 'Test2', mailing_list_id),
    ]
    contact_ids = [helpers.create_contact(*contact) for contact in contact_data]

    # Create an HTML message to send as part of the campaign
    subject = 'ActiveCampaign API Demo'
    message_html = '<html><body>This is only a test!</body></html>'
    sender = 'csimmonds814@gmail.com'
    message_id = helpers.create_html_message(
        mailing_list_id,
        subject,
        message_html,
        sender,
        'Claire Simmonds',
        sender
    )

    # Create and schedule the campaign
    campaign = 'API Demo'
    campaign_delivery = '2018-09-08 13:00:00'
    campaign_id = helpers.create_single_campaign(campaign, campaign_delivery, mailing_list_id, message_id)

    print('Campaign "{}" scheduled for delivery on {} was created successfully!'.format(campaign, campaign_delivery))
