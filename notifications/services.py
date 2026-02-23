import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings


class BrevoEmailService:

    @staticmethod
    
    @staticmethod
    def send_email(to_email, subject, content):

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.BREVO_API_KEY

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to_email}],
            subject=subject,
            html_content=content,
            sender={"email": "ext_ramegowda.md@ext.wakefit.co"}
        )

        try:
            api_instance.send_transac_email(send_smtp_email)
            return True
        except ApiException as e:
            print("Brevo Error:", e)
            return False

