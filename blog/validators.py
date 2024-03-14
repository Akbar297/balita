from django.core.exceptions import ValidationError


def validate_contact_form(data):
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')
    d = {
        'ok': False
    }
    if len(name) < 2:
        d['error'] = 'Name should be grater than 2 chars'
        return d

    if (email.count('@') != 1 or is_valid_email_name(email[:email.find('@')]) or email[email.find('@') + 1:].count(
            '.') != 1):
        d['error'] = 'Email is valid'

    if len(message) < 10:
        d['error'] = 'Message should be grater than 10 chars'
        return d

    if phone[:4] != '+998' or len(phone) != 13 or phone[1:].isnumeric():
        d['error'] = 'Phone number is...'
        return d
    d['ok'] = True
    return d


def is_valid_email_name(text):
    if not text[0].isalpha():
        return True
    for i in text:
        if i in ['&', '=', '_', "'", '+', '-', ',', '<', '>']:
            return True
    return False


def validate_uzb_number(number):
    if number[:4] != '+998' or len(number) != 13 or not number[1:].isnumeric():
        raise ValidationError('Phone number should be uzb number')
    return True
