import requests

import darklink.tools


class LaZagne(darklink.tools.Tool):
    """The LaZagne project is an open source application used to retrieve lots of passwords stored on a local computer."""

    @staticmethod
    def fetch(platform: str, arch: str):
        url = "https://github.com/AlessandroZ/LaZagne/releases/latest/download/LaZagne.exe"

        response = requests.get(url)

        if not response.ok:
            raise Exception(response.text)

        return "LaZagne.exe", response.content
