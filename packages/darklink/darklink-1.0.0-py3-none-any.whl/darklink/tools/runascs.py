import requests
import zipfile
import io

import darklink.tools


class RunasCs(darklink.tools.Tool):
    """RunasCs is an utility to run specific processes with different permissions than the user's current logon provides using explicit credentials."""

    @staticmethod
    def fetch(platform: str, arch: str):
        url = "https://github.com/antonioCoco/RunasCs/releases/latest/download/RunasCs.zip"

        response = requests.get(url)

        if not response.ok:
            raise Exception(response.text)

        z = zipfile.ZipFile(io.BytesIO(response.content))

        return "RunasCs.exe", z.read('RunasCs.exe')
