import json

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from news.models import sync_from_content


class Command(BaseCommand):
    """
    Sync from the manager.
    """

    def add_arguments(self, parser):
        parser.add_argument("--host", type=str, help="The host to sync from.")
        parser.add_argument("--port", type=int, help="The port to sync from.")

    def handle(self, *args, **options):
        if not options["host"]:
            raise ValueError("Missing required argument: --host")
        if not options["port"]:
            raise ValueError("Missing required argument: --port")
        
        host = options["host"]
        port = options["port"]

        # Get the data from the manager.
        key = settings.SYNC_KEY
        response = requests.get(f"http://{host}:{port}/sync/sync?key={key}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
            raise Exception(f"Failed to sync with manager: status {response.status_code}")
        
        data = json.loads(response.text)
        sync_from_content(data)
        