#!/usr/bin/env python3
"""
Module to handle signals: email, 
"""
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created



@receiver(reset_password_token_created)
def handle_reset_password_token_created(
        sender, instance, reset_password_token, *args, **kwargs):
    """
    Handle the signal when a password reset token is created. This function
    sends an email to the user with a link to reset their password.
    """
    user = reset_password_token.user

    context = {
        'current_user': user,
        'username': user.first_name,
        'email': user.email,
        # to be set to frontend url after
        'reset_password_url': '{}?token={}'.format(
            instance.request.build_absolute_uri(
                reverse('password_reset:reset-password-confirm')
            ),
            reset_password_token.key
        )
    }

    email_html_message = render_to_string(
        'email/password_reset_email.html', context)
    email_plaintext_message = render_to_string(
        'email/password_reset_email.txt', context)

    msg = EmailMultiAlternatives(
        "Password Reset for aceit.com",
        email_plaintext_message,
        None,
        [user.email]
    )
    msg.attach_alternative(email_html_message, 'text/html')

    msg.send()
