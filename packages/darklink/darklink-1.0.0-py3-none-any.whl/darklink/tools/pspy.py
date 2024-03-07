import requests

import darklink.tools


class pspy(darklink.tools.Tool):
    """Monitor linux processes without root permissions."""

    @staticmethod
    def fetch(platform: str, arch: str):
        arch = "64" if arch is None else arch

        url = f"https://github.com/DominicBreuker/pspy/releases/latest/download/pspy{arch}"

        response = requests.get(url)

        if not response.ok:
            raise Exception(response.text)

        return f"pspy{arch}", response.content
