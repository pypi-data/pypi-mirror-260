from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from zippy_form.models import Account
from .utils import ACCOUNT_STATUS
from rest_framework import status
from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework.exceptions import ValidationError


class IsAccountActive(BasePermission):
    """
    Permission To Check If Account Is Active
    """

    def has_permission(self, request, view):
        if 'ZF-SECRET-KEY' not in request.headers:
            raise AuthenticationFailed({"status": "permission_error", "detail": "Secret Key Required"},
                                       status.HTTP_401_UNAUTHORIZED)

        account_id = request.headers['ZF-SECRET-KEY']
        try:
            account = Account.objects.filter(id=account_id).first()

            if account is None:
                raise AuthenticationFailed({"status": "permission_error", "detail": "Invalid Secret Key"},
                                           status.HTTP_401_UNAUTHORIZED)
            elif account.status != ACCOUNT_STATUS[1][0]:
                raise AuthenticationFailed({"status": "permission_error", "detail": "Account Not Active"},
                                           status.HTTP_401_UNAUTHORIZED)
            else:
                return True
        except Exception as e:
            raise AuthenticationFailed({"status": "permission_error", "detail": "Invalid Secret Key"},
                                       status.HTTP_401_UNAUTHORIZED)


class ZippyPermission(BasePermission):
    """
    Zippy Form Permission
    """

    def has_permission(self, request, view):
        if hasattr(settings, 'ZF_PERMISSION'):
            if 'ZF-SECRET-KEY' not in request.headers:
                raise AuthenticationFailed({"status": "permission_error", "detail": "Secret Key Required"},
                                           status.HTTP_401_UNAUTHORIZED)
            account_id = request.headers['ZF-SECRET-KEY']
            callback_function = import_string(settings.ZF_PERMISSION)

            # Call the callback function with the required arguments
            callback_function_response = callback_function(account_id)

            permission_has_error = callback_function_response.get("has_error", False)
            if permission_has_error:
                permission_status = callback_function_response.get("status", "error")
                permission_status_code = callback_function_response.get("status_code", 400)
                permission__status_msg = callback_function_response.get("msg", "")

                raise ValidationError(
                    {
                        "status": permission_status,
                        "detail": permission__status_msg
                    },
                    permission_status_code)

            return True
