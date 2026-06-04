from email.utils import formataddr, parseaddr

import requests

from CTFd.utils import get_app_config, get_config
from CTFd.utils.email.providers import EmailProvider


class MailjetEmailProvider(EmailProvider):
    @staticmethod
    def sendmail(addr, text, subject):
        ctf_name = get_config("ctf_name")
        mailfrom_addr = get_config("mailfrom_addr") or get_app_config("MAILFROM_ADDR")
        mailfrom_addr = formataddr((ctf_name, mailfrom_addr))
        from_name, from_email = parseaddr(mailfrom_addr)

        mailjet_base_url = get_config("mailjet_base_url") or get_app_config(
            "MAILJET_BASE_URL"
        )
        mailjet_apikey_public = get_config("mailjet_apikey_public") or get_app_config(
            "MAILJET_APIKEY_PUBLIC"
        )
        mailjet_apikey_private = get_config("mailjet_apikey_private") or get_app_config(
            "MAILJET_APIKEY_PRIVATE"
        )
        try:
            r = requests.post(
                mailjet_base_url.rstrip("/") + "/v3.1/send",
                auth=(mailjet_apikey_public, mailjet_apikey_private),
                json={
                    "Messages": [
                        {
                            "From": {
                                "Email": from_email,
                                "Name": from_name or ctf_name,
                            },
                            "To": [{"Email": addr}],
                            "Subject": subject,
                            "TextPart": text,
                        }
                    ]
                },
                timeout=10.0,
            )
        except requests.RequestException as e:
            return (
                False,
                "{error} exception occured while handling your request".format(
                    error=type(e).__name__
                ),
            )

        if r.status_code == 200:
            return True, "Email sent"
        else:
            return False, "Mailjet settings are incorrect"
