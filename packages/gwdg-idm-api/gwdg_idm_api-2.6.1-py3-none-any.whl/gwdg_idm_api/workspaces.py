import json

from .models import IDMRequest
from .util import BadJsonError


class Workspaces(IDMRequest):
    api_suffix: str = "/Workspaces"

    def get_workspaces_json(self):
        request_url = f"{self.api_url}{self.api_suffix}"
        resp = self.get_request(request_url)
        try:
            json_resp = json.loads(resp.text)
        except json.decoder.JSONDecodeError:
            raise BadJsonError(resp.text)
        return json_resp
