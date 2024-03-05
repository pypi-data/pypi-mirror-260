import os
import json
import click

@click.command()
def configure():
    """Configure the Vagon Streams API Key and Secret for the CLI.

    Usage: `vagon-cli configure` and fill in the prompts to save the credentials.

    The credentials are saved at ~/.vagon/credentials."""
    # Define the credentials file path

    credentials_file = os.path.expanduser("~/.vagon/credentials")

    # Check if the credentials file already exists
    if not os.path.exists(credentials_file):
        # Create the directory if it does not exist
        os.makedirs(os.path.dirname(credentials_file), exist_ok=True)

        # Prompt the user for the Vagon Streams API Key and Secret
        api_key = click.prompt("Please enter your Vagon Streams API Key", type=str)
        api_secret = click.prompt(
            "Please enter your Vagon Streams API Secret", type=str
        )

        # Save the credentials in a dictionary
        credentials = {"default": {"api_key": api_key, "api_secret": api_secret}}

        # Write the credentials to the file in JSON format
        with open(credentials_file, "w") as file:
            json.dump(credentials, file, indent=4)

        click.echo("Credentials saved successfully.")
    else:
        click.echo(
            "Credentials file already exists. Please manually update it if necessary."
        )
