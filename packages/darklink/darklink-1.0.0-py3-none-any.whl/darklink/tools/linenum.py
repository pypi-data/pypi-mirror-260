import requests

import darklink.tools


class LinEnum(darklink.tools.Tool):
    """Scripted Local Linux Enumeration & Privilege Escalation Checks."""

    @staticmethod
    def fetch(platform: str, arch: str):
        url = "https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"

        response = requests.get(url)

        if not response.ok:
            raise Exception(response.text)

        return "LinEnum.sh", response.content
