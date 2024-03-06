from nmbrs.service.auth_service import AuthService
from nmbrs.service.company_service import CompanyService
from nmbrs.service.debtor_service import DebtorService
from nmbrs.service.employee_service import EmployeeService


class NmbrsSoapAPI:
    """
    A class representing the Nmbrs SOAP API.

    This class provides an interface to interact with various Nmbrs SOAP API services.
    """

    def __init__(self, sandbox: bool = True):
        """
        Constructor method for NmbrsSoapAPI class.

        Initializes NmbrsSoapAPI instance with authentication details and settings.

        :param auth: A dictionary containing authentication details.
        :param auth_type: A string representing the type of authentication (default: "token").
        :param sandbox: A boolean indicating whether to use the sandbox environment (default: True).
        """
        self.sandbox = sandbox

        self.auth_header: dict | None = None
        self.auth_service: AuthService = AuthService()
        self.debtor_service: DebtorService | None = None
        self.company_service: CompanyService | None = None
        self.employee_service: EmployeeService | None = None

    def auth_standard_token(self, username: str, token: str) -> None:
        # Setup auth
        self.auth_header = self.auth_service.authenticate_using_standard_token(username, token)

        if self.auth_header is None:
            # Throw custom exception to the user
            pass

        # Initialize other classes
        self.debtor_service: DebtorService = DebtorService(
            self.auth_header, self.sandbox
        )
        self.company_service: CompanyService = CompanyService(
            self.auth_header, self.sandbox
        )
        self.employee_service: EmployeeService = EmployeeService(
            self.auth_header, self.sandbox
        )
