from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_review_email(name, email, review):
    context = {"name": name, "email": email, "review": review}

    email_subject = "Thank You for Your Review"
    email_body = render_to_string("email_message.txt", context)

    email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [
            email,
        ],
    )

    return email.send(fail_silently=False)
