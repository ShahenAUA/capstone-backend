from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework import status
from mobile_api.messages import VALIDATION_ERROR

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
