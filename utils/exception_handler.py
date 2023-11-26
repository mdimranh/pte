from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def handle_exception(exc, context):
    response = exception_handler(exc, context)  # Let DRF handle other exceptions first

    if isinstance(exc, IntegrityError):
        error_message = str(exc)  # Get the error message
        print(error_message)
        if 'unique constraint' in error_message.lower():
            field_name = error_message.split('key')[-1].split('(')[1].split(')')[0].capitalize()
            response = Response(
                {field_name: "Already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
    return response
