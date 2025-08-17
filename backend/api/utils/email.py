import os
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from decouple import config

def send_verification_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verify_url = request.build_absolute_uri(
        reverse("verify-email", kwargs={"uidb64": uid, "token": token})
    )

    subject = "Verify Your SkillSwap Account"
    text = f"Click this link to verify your email: {verify_url}"
    html = f"""
        <html>
            <body>
                <h2>Welcome to SkillSwap, {user.username}!</h2>
                <p>Please verify your email address by clicking the link below:</p>
                <a href="{verify_url}">Verify My Email</a>
            </body>
        </html>
    """

    email = EmailMultiAlternatives(subject, text, config("EMAIL_HOST_USER"), [user.email])
    email.attach_alternative(html, "text/html")
    email.send()
