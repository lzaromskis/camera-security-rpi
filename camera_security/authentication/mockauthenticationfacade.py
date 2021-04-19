from typing import Optional

from camera_security.authentication.authenticationfacade import AuthenticationFacade


class MockAuthenticationFacade(AuthenticationFacade):

    def __init__(self):
        pass

    def IsAuthenticated(self, secret: str) -> bool:
        return True

    def Authenticate(self, password: str) -> Optional[str]:
        return "secret"

    def ChangePassword(self, new_password: str):
        pass

    def IsPasswordValid(self, password: str) -> bool:
        return True