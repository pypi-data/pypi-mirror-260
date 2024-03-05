import os
import click
from vagoncli.helpers import (
    api_generator,
    upload_multipart_object,
    upload_object,
)

@click.command()
@click.option(
    "--zip-file",
    "-z",
    "app_archive",
    help="Application Zip File [required]",
    required=True,
)
@click.option(
    "--app-id",
    "-i",
    "app_id",
    help="Streams Application ID [required]",
    type=int,
    required=True,
)
@click.option(
    "--exec",
    "-e",
    "executable",
    help="Application Main Executable File (.exe) [required]",
    required=True,
)
@click.option(
    "--app-version",
    "-v",
    "app_version",
    help="Name of the Application Version [required]",
    required=True,
)
def deploy(app_archive, app_id, executable, app_version):
    """[DEPRECATED] Deploy a New Version to an Existing Application
    """
    deploy_application_version(app_archive, app_id, executable, app_version)


@click.command()
@click.option(
    "--zip-file",
    "-z",
    "app_archive",
    help="Application Zip File [required]",
    required=True,
)
@click.option(
    "--app-id",
    "-i",
    "app_id",
    help="Streams Application ID [required]",
    type=int,
    required=True,
)
@click.option(
    "--exec",
    "-e",
    "executable",
    help="Application Main Executable File (.exe) [required]",
    required=True,
)
@click.option(
    "--app-version",
    "-v",
    "app_version",
    help="Name of the Application Version [required]",
    required=True,
)
def application_version(app_archive, app_id, executable, app_version):
    # method is not deprecated, but the deploy command is
    """Deploy a New Version to an Existing Application
    """
    deploy_application_version(app_archive, app_id, executable, app_version)

def deploy_application_version(app_archive, app_id, executable, app_version):
    if not os.path.exists(app_archive):
        click.echo(f"File {app_archive} does not exist.")
        return

    file_size = os.path.getsize(app_archive)
    file_name = os.path.basename(app_archive)

    # create Vendor Application Executable
    response = create_vendor_application_executable(
        file_name, file_size, app_id, executable
    )
    if response.status_code != 200:
        click.echo(f"Failed with status code: {response.status_code}")
        if response.text:
            click.echo(f"Response: {response.text}")
        return

    vendor_executuable_id = response.json().get("id")
    upload_urls = response.json().get("upload_urls")
    file_upload_id = response.json().get("file_upload_id")
    chunk_size = int(response.json().get("chunk_size")) * 2**20

    if not file_upload_id:
        upload_object(upload_urls, app_archive)
        response = finalize_vendor_application_executable(
            vendor_executuable_id, executable, app_version
        )
    else:
        parts = upload_multipart_object(upload_urls, app_archive, chunk_size)
        response = finalize_vendor_application_executable(
            vendor_executuable_id, executable, app_version, parts
        )

    if response.status_code != 200:
        click.echo(f"Failed with status code: {response.status_code}")
        if response.text:
            click.echo(f"Response: {response.text}")
   

def create_vendor_application_executable(
    file_name, file_size, vendor_app_id, executable
):
    path = "/app-stream-management/cli/executables"

    data = {
        "file_name": file_name,
        "file_size": file_size,
        "vendor_application_id": vendor_app_id,
        "executable_list": [executable],
    }

    return api_generator("POST", path, data)


def finalize_vendor_application_executable(
    vendor_executable_id, executable_name, app_version, parts=[]
):
    path = f"/app-stream-management/cli/executables/{vendor_executable_id}/complete"

    data = {
        "executable_name": executable_name,
        "version_name": app_version,
        "parts": parts,
    }

    return api_generator("POST", path, data)
