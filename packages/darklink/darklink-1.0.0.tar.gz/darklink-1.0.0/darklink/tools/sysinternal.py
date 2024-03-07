import requests
import zipfile
import io

import darklink.tools


class AccessChk(darklink.tools.Tool):
    """AccessChk is a command-line tool for viewing the effective permissions on files, registry keys, services, processes, kernel objects, and more."""

    @staticmethod
    def fetch(platform: str, arch: str):
        url = "https://download.sysinternals.com/files/AccessChk.zip"

        response = requests.get(url)

        if not response.ok:
            raise Exception(response.text)

        z = zipfile.ZipFile(io.BytesIO(response.content))

        return "accesschk.exe", z.read('accesschk.exe')


class Procdump(darklink.tools.Tool):
    """This command-line utility is aimed at capturing process dumps of otherwise difficult to isolate and reproduce CPU spikes."""

    @staticmethod
    def fetch(platform: str, arch: str):
        url = "https://download.sysinternals.com/files/Procdump.zip"

        response = requests.get(url)

        if not response.ok:
            raise Exception(response.text)

        z = zipfile.ZipFile(io.BytesIO(response.content))

        return "procdump.exe", z.read('procdump.exe')


class PsExec(darklink.tools.Tool):
    """Execute processes on remote systems."""

    @staticmethod
    def fetch(platform: str, arch: str):
        url = "https://download.sysinternals.com/files/PSTools.zip"

        response = requests.get(url)

        if not response.ok:
            raise Exception(response.text)

        z = zipfile.ZipFile(io.BytesIO(response.content))

        return "PsExec.exe", z.read('PsExec.exe')
