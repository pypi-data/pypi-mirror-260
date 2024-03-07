#
# PlasmaPlatformClient
# Copyright (c) 2024 10xDevelopment LLC
#

from .FHIRClient import FHIRClient

class PlasmaPlatformClient(FHIRClient):

    def __init__(self, base_url, state, code, project_id, environment_id):
        self.plasma_base_url = base_url

        default_headers = {}
        if state:
            default_headers["x-plasma-state"] = state
        if code:
            default_headers["x-plasma-code"] = code
        if project_id:
            default_headers["x-plasma-project-id"] = project_id
        if environment_id:
            default_headers["x-plasma-environment-id"] = environment_id

        fhir_base_url = base_url + '/api/plasma/fhir'
        super().__init__(fhir_base_url, None, default_headers)

    @staticmethod
    def initialize(base_url, state, code, project_id, environment_id):
        return PlasmaPlatformClient(base_url, state, code, project_id, environment_id)

    @staticmethod
    def from_state(base_url, state):
        return PlasmaPlatformClient(base_url, state, None, None, None)

    @staticmethod
    def from_code(base_url, state, code):
        return PlasmaPlatformClient(base_url, state,code, None, None)

    @staticmethod
    def for_backend(base_url, project_id, environment_id, project_secret):
        client = PlasmaPlatformClient(base_url, None, None, None, None)
        client.backend_connect(project_id, environment_id, project_secret)
        return client

    # Connect to Plasma via backend workflow...
    def backend_connect(self, project_id, environment_id, project_secret):
        # Save project/environment IDs. They will be added as headers to all requests...
        if project_id:
            self.default_headers["x-plasma-project-id"] = project_id
        if environment_id:
            self.default_headers["x-plasma-environment-id"] = environment_id

        # Send request...
        headers = { "x-plasma-project-secret": project_secret }
        url = self.plasma_base_url + '/api/plasma/sof/backend-connect'
        data = self.get_json(url, "", headers)

        # Set state and code headers...
        if data["state"]:
            self.default_headers["x-plasma-state"] = data["state"]
        if data["code"]:
            self.default_headers["x-plasma-code"] = data["code"]

        # Return result...
        return data

    # Get the current user...
    def whoami(self, read_fhir_user):
        url = self.plasma_base_url + '/api/plasma/sof/whoami'
        if read_fhir_user:
            url += '?readFhirUser=1'
        return self.get_json(url)