from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class CustomPasswordValidator():

    def __init__(self, min_length=8):
        self.min_length = min_length
        self.special_characters = "!@#%&*_+-"

    def validate(self, password, user=None):
        
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least one digit'))
        if not any(char.isalpha() for char in password):
            raise ValidationError(_('Password must contain at least one letter'))
        if not any(char in self.special_characters for char in password):
            raise ValidationError(_(f'Password must contain at least one special character {self.special_characters}'))
        if len(password) < self.min_length:
            raise ValidationError(_(f'Password must be at least {self.min_length} characters long'))

    def get_help_text(self):
        return f"Password must be {self.min_length} characters, contain a digit, a letter and a special character {self.special_characters}"
