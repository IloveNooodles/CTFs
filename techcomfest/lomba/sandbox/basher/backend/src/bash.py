from subprocess import Popen, PIPE, STDOUT
import string


class Bash:
    def __init__(self, user_input: str):
        self.program = "/bin/bash"
        self.user_input = user_input

    @property
    def read(self):
        return self._bashHandler(self.user_input)

    def _check(self, user_input):
        for char in string.ascii_letters+string.digits:
            if char in user_input:
                return False
        return True

    def _bashHandler(self, user_input):
        with Popen(self.program.split(), stdout=PIPE, stdin=PIPE, stderr=STDOUT) as p:
            if self._check(user_input):
                stdout = p.communicate(input=user_input.encode())[0]
                return stdout.decode()
            else:
                return 'bad hacker!!!'
