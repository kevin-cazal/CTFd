from CTFd.utils.email.providers.mailjet import MailjetEmailProvider


def sendmail(addr, text, subject):
    return MailjetEmailProvider.sendmail(addr, text, subject)
