from django.shortcuts import render
from django.http import HttpResponse
from leakcheck import LeakCheckAPI
from django.conf import settings
from django.core.mail import send_mail


def index(request):
    return render(request, 'index.html')

def search(request):
    # return HttpResponse(f'<h1>test</h1>')
    KEY = ''
    # email = 'john33@gmail.com'
    email = request.GET['email']
    # return HttpResponse(f'<h1>{email}</h1>')
    api = LeakCheckAPI()
    # API key setting
    api.set_key(KEY)
    api.set_type("email")
    api.set_query(email)

    results = api.lookup() # list of dicts
    message = ''
    for result in results:
        emaiPass = result['line']
        sources = result['sources']
        message += f'email:pass = {emaiPass} | Found in the following Database(s): {sources}\n'

    if len(results) == 0:
        return render(request, 'fail.html')
            # return HttpResponse(f'<h1>This email was not found in any data breaches!</h1>')

    subject = 'Here is the breached data we found'
    # message = str(results)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list )
    recordLen = len(results)
    return render(request, 'success.html', {'recordLen': recordLen})
    # return HttpResponse(f'<h1>{len(results)} record(s) found. All passwords have been sent to your email</h1>')