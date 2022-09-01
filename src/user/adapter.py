from allauth.account.adapter import DefaultAccountAdapter

from user.tasks import celery_send_mail

class MyAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        msg = self.render_mail(template_prefix, email, context)
        celery_send_mail.delay(msg.subject, msg.body, msg.from_email, msg.to)