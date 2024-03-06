from zeep import Client

from nmbrs.service.service import Service


class AuthService(Service):
    """
    A class responsible for handling authentication for Nmbrs services.
    """

    def __init__(self, sandbox: bool) -> None:
        """
        Constructor method for AuthService class.

        Initializes AuthService instance with authentication details and settings.

        :param sandbox: A boolean indicating whether to use the sandbox environment.
        """
        super().__init__()
        self.sandbox = sandbox
        self.auth_header: dict | None = None

        # Initialize nmbrs services
        base_uri = self.nmbrs_base_uri
        if sandbox:
            base_uri = self.nmbrs_sandbox_base_uri
        self.debtor_service = Client(f"{base_uri}{self.debtor_uri}")
        self.sso_service = Client(f"{base_uri}{self.sso_uri}")

    def set_auth_header(self, auth_header: dict) -> None:
        """
        Method to set the authentication.

        :param auth_header: A dictionary containing authentication details.
        """
        self.auth_header = auth_header

    def authenticate_using_standard_token(self, username: str, token: str) -> dict:
        """
        Generate authentication header for standard token-based authentication.

        :param username: A dictionary containing authentication details.
        :param token:
        :return: Authentication header with domain information.
        """
        env = self.debtor_service.service.Environment_Get(
            _soapheaders={"AuthHeader": {"Username": username, "Token": token}}
        )
        return {
            "AuthHeaderWithDomain": {
                "Username": username,
                "Token": token,
                "Domain": env.SubDomain,
            }
        }
