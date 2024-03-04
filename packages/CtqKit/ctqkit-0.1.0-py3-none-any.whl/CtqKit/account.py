from typing import Optional


class Account:

    def __init__(
            self,
            login_key: Optional[str] = None,
            machine_name: Optional[str] = None,
            base_url: Optional[str] = None,
            base_login_url: Optional[str] = None,
    ):
        """
        account initialization

        Args:
            login_key:
                API Token under personal center on the web.
            machine_name:
                name of quantum computer.
            base_url:
                System API base url.
            base_login_url:
                System Login API url.

        Raises:
            Exception: throw an exception when login fails
        """
        self.login_key = login_key
        self.machine_name = machine_name
        self.token = None

        self.base_url = base_url or 'https://qc.zdxlz.com/api/quantum/'
        self.base_login_url = base_login_url or 'https://qc.zdxlz.com/api/oauth/token'
        self.login = self.log_in()

    def log_in(self):
        """

        :return:
        """
