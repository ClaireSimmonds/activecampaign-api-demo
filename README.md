# activecampaign-api-demo
Experimenting with the ActiveCampaign API to schedule and send a campaign to a list of contacts

## Usage

To execute, install requirements (installing into a virtualenv or similar is recommended) and provide the required
campaign configuration options:

```bash
$ python demo.py --sender "Your Name" --sender_email youremail@example.com --sender_address "123 S Fake St" \
--sender_city "Any City" --sender_state il --sender_zip "12345" --sender_country us --campaign "New Year Campaign" \
--campaign_date "2019-01-01 00:00:00" --subject "Happy New Year!" --html ./message-content.html --contacts ./contacts.csv
```

Provided CSV containing contact information must have the following columns: email, first_name, last_name

## Compatibility

Tested against Python 3.6.4.
