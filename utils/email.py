# -*- coding: utf-8 -*-

import sys


from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template import Context
from django.template.loader import render_to_string



def check_for_required_mail_params(mail_dict):
    required_params = ['recipient_list', 'from_email', 'message', 'subject']

    assert_msg = "A required parameter for sending email is not specified"

    for mail_param_key in required_params:
        assert mail_param_key in mail_dict, assert_msg


def convert_mail_params_to_unicode(mail_dict):
    keys = ['from_email',
            'subject',
            'message',
            'message_html',
            'cc',
            'bcc',
            'reply_to']

    for key in keys:
        if mail_dict.get(key):
            if isinstance(mail_dict.get(key), str):
                mail_dict[key] = mail_dict.get(key).decode('utf8', 'ignore')

    recipient_list = [recipient.decode('utf8', 'ignore')
                      for recipient in mail_dict['recipient_list']
                      if isinstance(recipient, basestring)]

    mail_dict['recipient_list'] = recipient_list
    return mail_dict


def send_mail(mail_params, label=None):
    '''
    @param mail_params: Dict with recipient_list, from_email, subject, message,
    message_html, cc, bcc, reply_to
    @param label: Usually directory name inside templates/email/
    '''
    check_for_required_mail_params(mail_params)

    mail_params = convert_mail_params_to_unicode(mail_params)
    subject = mail_params['subject']
    message = mail_params['message']
    from_email = mail_params['from_email']
    recipients = mail_params['recipient_list']
    mail_obj = EmailMultiAlternatives(subject=subject,
                                      body=message,
                                      from_email=from_email,
                                      to=recipients)
    mail_obj.content_subtype = "plain"
    if mail_params.get('message_html'):
        mail_obj.attach_alternative(mail_params['message_html'], "text/html")
        # Handle attachements later

    status = mail_obj.send()
    return status


def send_templated_email(label,
                         to,
                         attachments=None,
                         context=None):

    recipients = to
    if not isinstance(to, (list, tuple)):
        recipients = [to]

    full_context = Context()
    full_context.update({} or context)

    mail = {}

    # In future, If subject is more than one line join them
    # Templates are loaded from template directory
    mail['subject'] = render_to_string('email/{}/subject.txt'.format(label))

    mail['message'] = render_to_string('email/{}/message.txt'.format(label),
                                       context_instance=full_context)
    mail['message_html'] = render_to_string(
        'email/{}/message.html'.format(label),
        context_instance=full_context
    )
    mail['recipient_list'] = recipients
    mail['from_email'] = settings.EMAIL_HOST_USER
    if label == 'registration':
        mail['from_email'] = 'sales@shieldsquare.com'
    mail['attachments'] = attachments

    try:
        return send_mail(mail, label=label)
    except Exception, e:
        msg = u"sending email failed\n"
        msg += u"params: {}".format(mail)
        msg += unicode(e)

#        Move this to logger
        print >> sys.stderr, e