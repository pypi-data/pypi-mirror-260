import requests

import darklink.tools


class PrivescCheck(darklink.tools.Tool):
    """Privilege Escalation Enumeration Script for Windows."""

    @staticmethod
    def fetch(platform: str, arch: str):
        url = "https://raw.githubusercontent.com/itm4n/PrivescCheck/master/PrivescCheck.ps1"

        response = requests.get(url)

        if not response.ok:
            raise Exception(response.text)

        return "PrivescCheck.ps1", response.content
