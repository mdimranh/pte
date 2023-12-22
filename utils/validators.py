from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from jsonschema import validate


@deconstructible
class JsonValidator:
    # schema = {}
    message = _("Enter a valid value.")
    code = "invalid"
    inverse_match = False

    def __init__(
        self, schema=None, message=None, code=None, inverse_match=None, flags=None
    ):
        self.schema = schema

    def __call__(self, value):
        try:
            validate(instance=value, schema=self.schema)
        except:
            raise ValidationError("Invalid data.")