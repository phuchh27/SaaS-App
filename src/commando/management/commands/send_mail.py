from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Send a test email'

    def handle(self, *args, **options):
        self.send_test_email()

    def send_test_email(self):
        subject = 'Test Email Subject'
        message = 'This is a test email message.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['recipient@example.com']

        send_mail(subject, message, from_email, recipient_list)
