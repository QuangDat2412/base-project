from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotFound,
    PermissionDenied,
    ValidationError,
    MethodNotAllowed
)
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, AuthenticationFailed):
        response = Response(
            {
                'status_code': status.HTTP_401_UNAUTHORIZED,
                'message': 'Authentication failed',
                'errors': []
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    elif isinstance(exc, ValidationError):
        print(exc)
        response = Response(
            {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Bad request',
                'errors': str(exc.detail)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    elif isinstance(exc, PermissionDenied):
        response = Response(
            {
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'Permission denied',
                'errors': []
            },
            status=status.HTTP_403_FORBIDDEN
        )
    elif isinstance(exc, NotFound):
        response = Response(
            {
                'status_code': status.HTTP_404_NOT_FOUND,
                'message': 'Not found',
                'errors': []
            },
            status=status.HTTP_404_NOT_FOUND
        )
    elif isinstance(exc, MethodNotAllowed):
        response = Response(
            {
                'status_code': status.HTTP_405_METHOD_NOT_ALLOWED,
                'message': 'Method not allowed',
                'errors': []
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    return response