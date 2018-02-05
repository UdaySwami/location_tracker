import logging
import traceback
from json import JSONDecodeError

from django.core.exceptions import ImproperlyConfigured, FieldError, ValidationError
from django.db.models import FieldDoesNotExist
from django.db.utils import IntegrityError
from django.http import JsonResponse, Http404
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError as RValidationError, PermissionDenied,\
    NotAuthenticated, AuthenticationFailed

from .exceptions import *
from .models import *

logger = logging.getLogger('django')


class Response:
    response_type = None
    status_type = "Failed"
    status_message = "Unknown Error"
    status_code = 1101
    item = None

    def get_response(self):
        return JsonResponse({
            "status": {
                "status_type": self.status_type,
                "status_message": self.status_message,
                "status_code": self.status_code
            },
            "item": self.item
        })

    def with_data(self, item=None, msg='Request Successful'):
        self.status_type = 'Success'
        self.status_code = 1001
        self.status_message = msg
        self.item = item
        return self.get_response()

    def __init__(self, response_type="Success", status_message="Success", status_type="Success", item=None):
        self.response_type = response_type
        logger.exception(response_type)
        if self.response_type == "Success":
            self.status_message = status_message
            self.status_code = 1001
            self.status_type = status_type
            self.item = item
        elif type(self.response_type) in [ValidationError, RValidationError]:
            self.status_message = "%s" % self.response_type
            self.status_code = 1102
            self.status_type = "Failed"
        elif type(self.response_type) == AttributeError:
            self.status_message = "%s" % self.response_type
            # raise self.response_type
            self.status_message = "Unknown error occurred (1104)"
            self.status_code = 1103
            self.status_type = "Failed"
            logger.exception(self.response_type)
        elif type(self.response_type) == FieldDoesNotExist:
            self.status_message = "%s" % self.response_type
            self.status_code = 1104
            self.status_type = "Failed"
        elif type(self.response_type) == JSONDecodeError:
            self.status_message = "Unknown error occurred (1106)"
            self.status_code = 1105
            self.status_type = "Failed"
        elif type(self.response_type) == User.DoesNotExist:
            self.status_message = "The user information does not exist in our system."
            self.status_code = 1106
            self.status_type = "Failed"
        elif type(self.response_type) == IntegrityError:
            self.status_message = "%s" % self.response_type
            self.status_code = 1107
            self.status_type = "Failed"
        elif type(self.response_type) == InvalidCredentials:
            self.status_message = "Invalid Username / Password provided. Please try again."
            self.status_code = 1108
            self.status_type = "Failed"
        elif type(self.response_type) == KeyError:
            self.status_message = "Unknown error occurred (1117)"
            self.status_code = 1109
            self.status_type = "Failed"
        elif type(self.response_type) == ValueError:
            self.status_message = "%s" % self.response_type
            self.status_message = "Missing parameters in request"
            self.status_code = 1110
            self.status_type = "Failed"
            logger.error("%s" % self.response_type)
        elif type(self.response_type) == TypeError:
            self.status_message = "%s" % self.response_type
            # raise self.response_type
            self.status_message = "Unknown error occurred (1123)"
            self.status_code = 1111
            self.status_type = "Failed"
            logger.error("%s" % self.response_type)
        elif type(self.response_type) == AssertionError:
            self.status_message = "%s" % self.response_type
            # raise self.response_type
            self.status_message = "Unknown error occurred (1124)"
            self.status_code = 1112
            self.status_type = "Failed"
        elif type(self.response_type) == ImproperlyConfigured:
            self.status_message = "%s" % self.response_type
            # raise self.response_type
            self.status_message = "Unknown error occurred (1125)"
            self.status_code = 1113
            self.status_type = "Failed"
        elif type(self.response_type) == PermissionDenied:
            self.status_message = "%s" % self.response_type
            # raise self.response_type
            self.status_code = 1114
            self.status_type = "Failed"
        elif type(self.response_type) == NotAuthenticated:
            self.status_message = "%s" % self.response_type
            # raise self.response_type
            self.status_code = 1115
            self.status_type = "Failed"
        elif type(self.response_type) == AuthenticationFailed:
            self.status_message = "Token Expired: Please Login Again"
            self.status_code = 1115
            self.status_type = "Failed"

        else:
            logger.error("Unable to process error: %s" % traceback.format_exc())
            logger.error("Error type is: %s" % type(response_type))
            pass


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    # if response is not None:
    #     response.data['status_code'] = response.status_code

    if isinstance(exc, Http404):
        return Response(context['view'].model.DoesNotExist("%s Does Not Exists" %
                                                           type(context[
                                                                    'view'].model).__name__)).get_response()
    return Response(exc).get_response()
