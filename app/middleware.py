from django.shortcuts import redirect
from django.urls import reverse


class AuthenticationMiddleware:
    """AuthenticationMiddleware checks if request is authenticated or not"""
    def __init__(self, get_response):
        self.get_response = get_response
        self.exclude_urls = [reverse('homepage'),
                             reverse('login'),
                             reverse('register'),
                             reverse('logout')]

    def __call__(self, request):
        if not request.user.is_authenticated and request.path not in self.exclude_urls:
            return redirect('login')

        response = self.get_response(request)
        return response
