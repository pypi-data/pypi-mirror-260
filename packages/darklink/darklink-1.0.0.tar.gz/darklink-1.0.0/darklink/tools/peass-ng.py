import requests

import darklink.tools


class winPEAS(darklink.tools.Tool):
    """Windows local Privilege Escalation Awesome Script."""

    @staticmethod
    def fetch(platform: str, arch: str):
        url = "https://github.com/carlospolop/PEASS-ng/releases/latest/download/winPEASany.exe"

        response = requests.get(url)

        if not response.ok:
            raise Exception(response.text)

        return "winPEASany.exe", response.content


class linPEAS(darklink.tools.Tool):
    """Linux local Privilege Escalation Awesome Script."""

    @staticmethod
    def fetch(platform: str, arch: str):
        url = "https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh"

        response = requests.get(url)

        if not response.ok:
            raise Exception(response.text)

        return "linpeas.sh", response.content
