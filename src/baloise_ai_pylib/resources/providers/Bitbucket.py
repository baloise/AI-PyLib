from baloise_ai_pylib.resources.providers import ProviderInterface, Resource
from baloise_ai_pylib.console.Spinner import Spinner
import requests
import os
import urllib.parse
from pathlib import Path

class Bitbucket(ProviderInterface):
    def provide(self, resource:Resource):
        resource.local_path = f"resources/{resource.remote_path}/{resource.name}"
        if(os.path.exists(resource.local_path)):
            print(f"{resource.local_path} ✅")
        else: 
            Path(resource.local_path).parent.mkdir(parents=True, exist_ok=True)
            username = os.getenv('BITBUCKET_USER')
            if not username:
                raise KeyError(f"Environment variable 'BITBUCKET_USER' is missing.")
            token = os.getenv('BITBUCKET_TOKEN')
            if not token:
                raise KeyError(f"Environment variable 'BITBUCKET_TOKEN' is missing.")
            at = f"?at={urllib.parse.quote(resource.version)}" if resource.version else ''
            url = f"https://{os.getenv('BITBUCKET_HOST', 'bitbucket')}/rest/api/latest/projects/{resource.org}/repos/data/raw/{resource.remote_path}/{resource.name}{at}"
            spin = Spinner(f"Loading {url}")
            spin.start()
            response = requests.get(url, auth=(username, token))
            if response.status_code == 200:
                with open(resource.local_path, 'wb') as f:
                    f.write(response.content)
                spin.stop()
                print(f"{resource.local_path} ✅")
            else:
                spin.stop()
                raise IOError(f"😞 Status code: {response.status_code}, Error: {response.text}")