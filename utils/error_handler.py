from django import http
from django.core.mail import get_connection, send_mail
from django.template import (Context, loader, TemplateDoesNotExist)
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def server_error_500(request, template_name='500.html'):
    connection = get_connection(host='smtp.gmail.com',
                                port=587,
                                username='noreply.shieldsquare@gmail.com',
                                password='ssMailer@123')
    send_mail('Django Internal Error-500', 'A 500 error occurred in the server', 'noreply.shieldsquare@gmail.com', ['admin-dev-team@shieldsquare.com'], connection = connection, fail_silently=False)
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return http.HttpResponseServerError('<h1>Server Error (500)</h1>', content_type='text/html')
    return http.HttpResponseServerError(template.render(Context({})))

def exception_raiser_view(request):
    raise Exception('TEST')
