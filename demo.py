import argparse
import csv

from activecampaign.api import ActiveCampaignAPI


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-s',
        '--sender',
        help='Name of the sender of this campaign',
        required=True
    )

    parser.add_argument(
        '-se',
        '--sender_email',
        help='Email address for the sender of this campaign',
        required=True
    )

    parser.add_argument(
        '-sa',
        '--sender_address',
        help='Physical address for the sender of this campaign',
        required=True
    )

    parser.add_argument(
        '-sc',
        '--sender_city',
        help='City for the sender of this campaign',
        required=True
    )

    parser.add_argument(
        '-sz',
        '--sender_zip',
        help='City for the sender of this campaign',
        required=True
    )

    parser.add_argument(
        '-sc',
        '--sender_country',
        help='Country for the sender of this campaign',
        required=True
    )

    parser.add_argument(
        '-cpgn',
        '--campaign',
        help='Name of this email campaign',
        required=True
    )

    parser.add_argument(
        '-cd',
        '--campaign_date',
        help='Date and time (format: YYYY-MM-DD hh:mm:ss) when emails in this campaign should be scheduled for sending',
        required=True
    )

    parser.add_argument(
        '-sub',
        '--subject',
        help='Email subject for the campaign',
        required=True
    )

    parser.add_argument(
        '-hc',
        '--html',
        help='File containing HTML content to be used as the message body for the campaign',
        type=argparse.FileType('r'),
        required=True,
    )

    parser.add_argument(
        '-c',
        '--contacts',
        help='CSV file containing (email, first_name, last_name) for contacts who will receive the campaign',
        type=argparse.FileType('r'),
        required=True,
    )

    return parser.parse_args()


if __name__ == '__main__':
    api = ActiveCampaignAPI()

    args = get_args()

    # Create mailing list and add contacts
    mailing_list_id = api.create_mailing_list(
        '{} - Mailing List'.format(args.campaign),
        {
            'name': args.sender,
            'address': args.sender_address,
            'city': args.sender_city,
            'zip': args.sender_zip,
            'country': args.sender_country
        }
    )

    reader = csv.DictReader(args.contacts)
    for row in reader:
        api.create_contact(row['email'], [mailing_list_id], first_name=row['first_name'], last_name=row['last_name'])

    # Create an HTML message to send as part of the campaign
    message_id = api.create_html_message(
        [mailing_list_id],
        args.subject,
        args.html.read(),
        args.sender_email,
        args.sender,
        args.sender_email
    )

    # Create and schedule the campaign
    api.create_single_campaign(args.campaign, args.campaign_date, [mailing_list_id], message_id)
    print(
        'Campaign "{}" scheduled for delivery on {} was created successfully!'.format(
            args.campaign,
            args.campaign_date
        )
    )
