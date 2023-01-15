from .bash import Bash
import json


class Handler(object):
    @classmethod
    async def handler(self, websocket):
        self.websocket = websocket
        async for message in websocket:
            try:
                await self._processMessage(message)
            except Exception:
                event = {
                    "type": "error",
                    "message": f"something wrong"
                }
                await self.websocket.send(json.dumps(event))

    @classmethod
    async def _processMessage(self, message):
        event = json.loads(message)
        match event['type']:
            case "command":
                user_command = event['input']
                stdout = Bash(user_command).read
                event = {
                    "status": "success",
                    "stdout": stdout,
                }
                await self.websocket.send(json.dumps(event))
            case default:
                event = {
                    "status": "error",
                    "message": f"error event {default} not found!"
                }
                await self.websocket.send(json.dumps(event))
