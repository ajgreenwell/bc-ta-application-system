from django.shortcuts import render


def handle_bad_request(request, app, expected_method):
    context = { 
        'expected_method': expected_method,
        'received_method': request.method
    }
    return render(request, f'{app}/bad_request.html', context)
 