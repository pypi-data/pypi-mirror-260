import hmac
import json
import hashlib
import os
import time
import click
import requests

from vagoncli.constants import VAGON_API_BASE_URL

API_KEY = None
API_SECRET = None


def get_hmac(path, method, body):
    api_key, api_secret = get_credentials()
    current_time = current_milli_time()
    payload = f"{api_key}{method}{path}{current_time}mysupernonce{body}"
    signature = hmac.new(
        api_secret.encode(), payload.encode(), hashlib.sha256
    ).hexdigest()
    return f"HMAC {api_key}:{signature}:mysupernonce:{current_time}"


def current_milli_time():
    return round(time.time() * 1000)


def upload_object(upload_urls, file_name):
    click.echo("Uploading object...")
    click.echo(f"0% complete")
    response = requests.put(upload_urls[0], data=open(file_name, "rb"))
    if response.status_code == 200:
        click.echo(f"100% complete")
        click.echo("Upload complete.")
        return True
    else:
        click.echo("Upload failed.")
        return False


def upload_multipart_object(upload_urls, file_name, chunk_size):
    click.echo("Uploading object...")
    click.echo(f"0% complete")
    with open(file_name, "rb") as f:
        part_number = 1
        parts = []
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            response = requests.put(upload_urls[part_number - 1], data=chunk)
            if response.status_code == 200:
                click.echo(f"{int((part_number / len(upload_urls)) * 100)}% complete")
            else:
                click.echo("Upload failed.")
                raise Exception("Multipart Upload failed.")
            parts.append({"part_number": part_number, "etag": response.headers["ETag"]})
            part_number += 1
        click.echo("Upload complete.")
        return parts


def get_credentials():
    global API_KEY, API_SECRET

    if API_KEY and API_SECRET:
        return API_KEY, API_SECRET
    credentials_file = os.path.expanduser("~/.vagon/credentials")
    if not os.path.exists(credentials_file):
        click.echo(
            "Credentials file does not exist. Please run 'vagon-cli configure' to create it."
        )
        raise click.Abort()

    with open(credentials_file, "r") as file:
        credentials = json.load(file)
        default_credentials = credentials.get("default")
        if not default_credentials:
            click.echo(
                "No default credentials found in the credentials file. Please run 'vagon-cli configure' to create them."
            )
            raise click.Abort()
        API_KEY = default_credentials.get("api_key")
        API_SECRET = default_credentials.get("api_secret")
        return API_KEY, API_SECRET


def api_generator(method, path, data=""):
    url = VAGON_API_BASE_URL + path

    if data != "":
        data = json.dumps(data)


    headers = {
        "Authorization": get_hmac(path, method, data),
        "Content-Type": "application/json",
    }

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, data=data)
    elif method == "PUT":
        response = requests.put(url, headers=headers, data=data)
    return response
