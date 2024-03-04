import boto3
import requests

from praetorian_cli.sdk.account import verify_credentials, Account


class Chaos:

    def __init__(self, account: Account):
        self.account = account

    @verify_credentials
    def my_assets(self) -> []:
        resp = requests.post(f"{self.account.api}/my/assets", data={})
        return resp.json()

    @verify_credentials
    def my_jobs(self) -> []:
        resp = requests.post(f"{self.account.api}/my/jobs", data={})
        return resp.json()

    @verify_credentials
    def my_risks(self) -> []:
        resp = requests.post(f"{self.account.api}/my/risks", data={})
        return resp.json()

    @verify_credentials
    def trigger(self, capability: str, options: dict) -> {}:
        resp = requests.post(f"{self.account.api}/job/{capability}", data=options)
        return resp.json()

    @verify_credentials
    def upload(self, name: str) -> bool:
        with open(name, 'rb') as file:
            resp = requests.put(f"{self.account.api}/file/{name}", data=file, allow_redirects=True, headers=self.account.headers)
            return resp.status_code == requests.ok

    @verify_credentials
    def download(self, key: str) -> bool:
        resp = requests.get(f"{self.account.api}/file/{key}", allow_redirects=True, headers=self.account.headers)
        with open(key, 'wb') as file:
            file.write(resp.content)
        return resp.status_code == requests.ok
