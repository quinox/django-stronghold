from django.contrib.auth.decorators import user_passes_test
from stronghold import conf, utils


class LoginRequiredMiddleware(object):
    """
    Restrict access to users that for which STRONGHOLD_USER_TEST_FUNC returns
    True. Default is to check if the user is authenticated.

    View is deemed to be public if the @public decorator is applied to the view

    View is also deemed to be Public if listed in in django settings in the
    STRONGHOLD_PUBLIC_URLS dictionary
    each url in STRONGHOLD_PUBLIC_URLS must be a valid regex

    """

    def __init__(self, *args, **kwargs):
        if args:
            # Django 1.10 and up
            self.get_response = args[0]

        self.public_view_urls = getattr(conf, 'STRONGHOLD_PUBLIC_URLS', ())

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('Processing view.')
        if conf.STRONGHOLD_USER_TEST_FUNC(request.user) \
                or utils.is_view_func_public(view_func) \
                or self.is_public_url(request.path_info):
            return None

        decorator = user_passes_test(conf.STRONGHOLD_USER_TEST_FUNC)
        return decorator(view_func)(request, *view_args, **view_kwargs)

    def is_public_url(self, url):
        return any(public_url.match(url) for public_url in self.public_view_urls)

    def __call__(self, request):
        # Django 1.10 and up
        return self.get_response(request)
