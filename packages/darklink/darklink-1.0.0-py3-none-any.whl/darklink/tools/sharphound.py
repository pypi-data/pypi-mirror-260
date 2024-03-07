import requests
import zipfile
import io
import re

import darklink.tools


class SharpHound(darklink.tools.Tool):
    """C# Data Collector for BloodHound."""

    @staticmethod
    def fetch(platform: str, arch: str):
        release_url = "https://api.github.com/repos/BloodHoundAD/SharpHound/releases/latest"

        response = requests.get(release_url)

        if not response.ok:
            raise Exception(response.text)

        for asset in response.json()["assets"]:
            if re.match(r"SharpHound-v\d+\.\d+\.\d+\.zip", asset["name"]):
                download_url = asset["browser_download_url"]
                break
        else:
            raise Exception("Could not find asset in GitHub release")

        response = requests.get(download_url)

        if not response.ok:
            raise Exception(response.text)

        z = zipfile.ZipFile(io.BytesIO(response.content))

        return "SharpHound.exe", z.read('SharpHound.exe')
