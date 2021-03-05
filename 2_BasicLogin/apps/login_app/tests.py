from django.test import TestCase

"""
Below is my planned testing regime for this app, which I have
done manually.   Really, I need to build a set of automated tests
for this to make sure that everything works.   This is something
for later.
"""

"""
Mark
Mark_john_wilson@yahoo.co.uk
2_banana

1 – Login when the account has not been setup with invalid credentials.   The response form should contain “Please enter a correct username and password”:
	Templates Tested:   login.py

2 – Register a new user, but follow a slightly invalid/adjusted link.   The response should contain “Invalid user or activation token…”:
	Templates Tested:   register.html, activation_sent.py, activation_invalid.py, 

3 – Register a new user, with correct credentials.   It should return a page containing “Activation link sent”.   When you follow the link, it should just log you in.:
	Templates Tested:   register.html, activation_sent.py, activation_request.html

4 – Log out.   It should return “You have successfully logged out”.
	Templates Tested:   logged_out.html

5 – Login with a valid account.   It should take you to the ‘frontend’:
	Templates Tested:   login.html,

6 – Changed the logged in user’s password to 3_banana.   It should return a page saying “Password changed”:
	Templates Tested:   password_change_form.html, password_change_done.html

7 – Request a password reset, but follow a slightly invalid/adjusted link.   It should return “The password reset link was invalid”:
	Templates Tested:   password_reset_confirm.html

8 – Request a password reset, follow the link and change the password to 4_banana.   Check the email subject and content are consistent with the Email Templates:
	Templates Tested:   password_reset_form.html, password_reset_done.html, 
	Email Templates:     password_reset_email.html, password_reset_subject.html

"""