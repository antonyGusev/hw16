from lib import UARTConnector


class AuthController:
  def __init__(self, connector: UARTConnector):
    self._connector = connector

  def register(self, login: str, password: str) -> bool:
    response = self._connector.execute_command(f'register {login} {password}')

    # Registration is considered successful only when firmware confirms profile creation.
    return any('Profile Created' in line for line in response)

  def login(self, login: str, password: str) -> bool:
    response = self._connector.execute_command(f'login {login} {password}')

    # Login is considered successful only when firmware confirms session start.
    return any('Session Started' in line for line in response)
