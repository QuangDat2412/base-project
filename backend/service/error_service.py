from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError, AuthenticationFailed

class ErrorService:
    @staticmethod
    def not_found_error(message):
        raise NotFound(detail=message)

    @staticmethod
    def permission_denied_error(message):
        raise PermissionDenied(detail=message)

    @staticmethod
    def validation_error(errors):
        raise ValidationError(detail=errors)

    @staticmethod
    def authentication_error(message):
        raise AuthenticationFailed(detail=message)
