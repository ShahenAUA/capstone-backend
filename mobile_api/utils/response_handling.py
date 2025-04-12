import jwt
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from pet_welfare.settings import ACCESS_TOKEN_EXPIRED_STATUS_CODE, SECRET_KEY
from mobile_api.messages import VALIDATION_ERROR, MISSING_AUTH_CREDENTIALS, EXPIRED_AUTH_CREDENTIALS, INVALID_AUTH_CREDENTIALS

def construct_response(message=None, data=None, status=status.HTTP_200_OK):
    response_content = {}
    if message is not None:
        response_content['message'] = message
    
    if data is not None:
        if isinstance(data, dict):
            response_content.update(data)
        else:
            response_content = data

    return Response(response_content, status=status)

def construct_error(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR, identifier=None):
    return Response({
        'statusCode': status,
        'errors': [
            {
                'message': message,
                'identifier': identifier
            }
        ]
    }, status=status)

def handle_validation_error(error):
    try:
        errors = {}
        for field, messages in error.detail.items():
            if field not in errors:
                errors[field] = []
            
            if isinstance(messages, str):  
                messages = [messages]

            errors[field].extend(messages)
        
        errors_list = [{'identifier': field, 'message': ' '.join(messages)} for field, messages in errors.items()]

        return Response({
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'errors': errors_list
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'errors': [{'identifier': None, 'message': VALIDATION_ERROR}]
        }, status=status.HTTP_400_BAD_REQUEST)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, NotAuthenticated):
        return Response({
            'statusCode': status.HTTP_401_UNAUTHORIZED,
            'errors': [
                {
                    'message': MISSING_AUTH_CREDENTIALS,
                    'identifier': 'Authorization'
                }
            ]
        }, status=status.HTTP_401_UNAUTHORIZED)
    elif isinstance(exc, AuthenticationFailed):
        auth_header = context['request'].headers.get('Authorization', None)
        
        if auth_header:
            token = auth_header.split()[1]
            try:
                jwt.decode(token, algorithms=['HS256'], key=SECRET_KEY, options={"verify_signature": True})
                
            except jwt.ExpiredSignatureError:
                return Response({
                    'statusCode': ACCESS_TOKEN_EXPIRED_STATUS_CODE,
                    'errors': [
                        {
                            'message': EXPIRED_AUTH_CREDENTIALS,
                            'identifier': 'Authorization'
                        }
                    ]
                }, status=ACCESS_TOKEN_EXPIRED_STATUS_CODE)
            # except Exception as e:
            except (jwt.InvalidSignatureError, jwt.DecodeError, jwt.InvalidTokenError) as e:
                pass # this will pass to invalid case
        
        response = Response({
            'statusCode': status.HTTP_401_UNAUTHORIZED,
            'errors': [
                {
                    'message': INVALID_AUTH_CREDENTIALS,
                    'identifier': 'Authorization'
                }
            ]
        }, status=status.HTTP_401_UNAUTHORIZED)
    elif isinstance(exc, PermissionDenied):
        return construct_error(
            message=str(exc), 
            status=status.HTTP_403_FORBIDDEN
        )
    else:
        response = exception_handler(exc, context)
        
    return response
