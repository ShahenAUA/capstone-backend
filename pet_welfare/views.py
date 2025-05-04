from django.http import HttpResponse

def healthcheck_view(request):
    html_content = '''
    <!DOCTYPE html>
    <html lang="hy">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Health Check</title>
    </head>
    <body>
        <h1>OK</h1>
    </body>
    </html>
    '''
    return HttpResponse(html_content)
