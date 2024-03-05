import os
import click
from vagoncli.helpers import api_generator, upload_multipart_object


@click.command()
@click.option(
    "--name",
    "-n",
    "app_name",
    help="Application Name",
    required=True,
)
@click.option(
    "--zip-file",
    "-z",
    "app_archive",
    help="Application Zip File",
    required=True,
)
@click.option(
    "--exec",
    "-e",
    "executable",
    help="Application Main Executable File (.exe)",
    required=True,
)
@click.option(
    "--performance",
    "-p",
    "machine_type_id",
    help="Application Performance Selection",
    required=True,
    type=int,
)
@click.option(
    "--cursor",
    "-c",
    "key_mapping_selection",
    help="Key Mapping Selection. Options: mouse / 360",
    show_default=True,
    required=False,
    default="mouse",
)

def create_application(
    app_name, app_archive, executable, machine_type_id, key_mapping_selection
):
    """Create a New Application.

    Uploaded application file will be deployed as a new Application.
    """

    if not os.path.exists(app_archive):
        click.echo(f"File {app_archive} does not exist.")
        return

    file_size = os.path.getsize(app_archive)
    file_name = os.path.basename(app_archive)

    create_application_response = create_vendor_application(
        file_name, file_size, executable
    )

    if create_application_response.status_code != 200:
        click.echo(
            f"Failed with status code: {create_application_response.status_code}"
        )
        if create_application_response.text:
            click.echo(f"Response: {create_application_response.text}")
        return

    
    create_app_response_json = create_application_response.json()
    vendor_application_id = create_app_response_json.get("vendor_application_id")
    upload_urls = create_app_response_json.get("upload_urls")
    file_upload_id = create_app_response_json.get("file_upload_id")
    chunk_size = int(create_app_response_json.get("chunk_size")) * 2**20

    if not file_upload_id:
        upload_multipart_object(upload_urls, app_archive, chunk_size)
        complete_response = finalize_vendor_application(vendor_application_id)
    else:
        parts = upload_multipart_object(upload_urls, app_archive, chunk_size)
        complete_response = finalize_vendor_application(vendor_application_id, parts)

    if complete_response.status_code != 200:
        click.echo(f"Failed with status code: {complete_response.status_code}")
        if complete_response.text:
            click.echo(f"Response: {complete_response.text}")

    update_response = update_vendor_application(
        vendor_application_id,
        app_name,
        executable,
        key_mapping_selection,
        machine_type_id,
    )
    if update_response.status_code != 200:
        click.echo(f"Failed with status code: {update_response.status_code}")
        if update_response.text:
            click.echo(f"Response: {update_response.text}")

    click.echo("Application created successfully.")


def create_vendor_application(file_name, file_size, executable):
    path = "/app-stream-management/cli/applications"
    data = {
        "file_name": file_name,
        "file_size": file_size,
        "executable_list": [executable],
    }

    response = api_generator("POST", path, data)

    return response


def finalize_vendor_application(vendor_application_id, parts=[]):
    path = f"/app-stream-management/cli/applications/{vendor_application_id}/complete"

    data = {"parts": parts}

    response = api_generator("POST", path, data)

    return response


def update_vendor_application(
    vendor_application_id,
    application_name,
    exec,
    key_mapping_selection,
    machine_type_id,
):
    path = f"/app-stream-management/cli/applications/{vendor_application_id}"

    cursor_to_key_mapping = {
        "mouse": "click",
        "360": "game_mode",
    }

    data = {
        "executable_name": exec,
        "application_name": application_name,
        "key_mapping_selection": cursor_to_key_mapping[key_mapping_selection],
        "machine_type_id": machine_type_id,
    }

    response = api_generator("PUT", path, data)

    return response
