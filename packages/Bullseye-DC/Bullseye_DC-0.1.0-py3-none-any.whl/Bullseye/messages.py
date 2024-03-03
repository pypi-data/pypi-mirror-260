MUST_SOLVE_CAPTCHA = """\
=======================================================================
UPDATE: Discord switched from reCAPTCHA to hCaptcha, so this won't
work anymore. You'll probably have to log in through the website first.
=======================================================================
You must solve a CAPTCHA challenge.
You will be guided through the steps necessary to complete the challenge.
Press enter to start the challenge...
"""

INVALID_CAPTCHA = """\
The CAPTCHA token was not accepted.
This can happen even when all CAPTCHA challenges are successfully completed.
This is a known issue: https://github.com/taylordotfish/librecaptcha/issues/7
Sometimes, if you continue to solve CAPTCHAs, one will eventually be accepted.
However, this doesn't always seem to be the case. Please see the issue link
above if you'd like to help.
"""

SUCCESSFUL_REGISTRATION = """\
You have successfully registered.
You should verify your email address with the "verify" command.
"""

ENTER_VERIFICATION_LINK = """\
Enter the verification link you received by email.
The email should contain a link that looks like this:
https://discordapp.com/verify?token=<token>"
"""

ENTER_NEW_LOCATION_LINK = """\
Enter the new location verification link you received by email.
The email should contain a link that looks like this:
https://discordapp.com/authorize-ip#token=<token>"

If the link in the email starts with "https://click.discord.com"
instead, visit that link in your browser with JavaScript disabled.
It should redirect to a link that looks like the one above.
"""
