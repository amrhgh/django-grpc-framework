from rest_framework.authentication import TokenAuthentication
from rest_framework import HTTP_HEADER_ENCODING, exceptions


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class GrpcTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        meta_data = dict(request.context.invocation_metadata())
        meta_data = {k.lower(): v for k, v in meta_data.items()}
        token = meta_data.get(self.authenticate_header(request).lower())

        if not token:
            return None

        return self.authenticate_credentials(token)
