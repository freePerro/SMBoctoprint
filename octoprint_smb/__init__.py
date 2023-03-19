from octoprint.plugin import OctoPrintPlugin, TemplatePlugin, SettingsPlugin, AssetPlugin, SimpleApiPlugin
from smbprotocol.connection import Connection
from smbprotocol import smb3
import tempfile
import os

class SMBPlugin(OctoPrintPlugin, TemplatePlugin, SettingsPlugin, AssetPlugin, SimpleApiPlugin):

    def initialize(self):
        self._logger.info("SMB Plugin initialized")

    def get_settings_defaults(self):
        return {
            "smb_host": "",
            "smb_username": "",
            "smb_password": "",
            "smb_share": "",
            "smb_directory": ""
        }

    def smb_connect(self):
        smb_host = self._settings.get(["smb_host"])
        smb_username = self._settings.get(["smb_username"])
        smb_password = self._settings.get(["smb_password"])

        connection = Connection(smb_host, smb_username, smb_password)
        connection.connect()
        return connection

    def smb_disconnect(self, connection):
        connection.disconnect()

    def smb_list_directory(self):
        connection = self.smb_connect()
        smb_share = self._settings.get(["smb_share"])
        smb_directory = self._settings.get(["smb_directory"])

        with smb3.SMB3(connection, smb_share) as smb:
            for entry in smb.list_entries(smb_directory):
                self._logger.info(entry.name)

        self.smb_disconnect(connection)

    def smb_download_file(self, remote_filename, local_filepath):
        connection = self.smb_connect()
        smb_share = self._settings.get(["smb_share"])
        smb_directory = self._settings.get(["smb_directory"])
        remote_file_path = os.path.join(smb_directory, remote_filename)

        with smb3.SMB3(connection, smb_share) as smb:
            with open(local_filepath, "wb") as local_file:
                smb.get(remote_file_path, local_file)

        self.smb_disconnect(connection)

    def smb_upload_file(self, local_filepath, remote_filename):
        connection = self.smb_connect()
        smb_share = self._settings.get(["smb_share"])
        smb_directory = self._settings.get(["smb_directory"])
        remote_file_path = os.path.join(smb_directory, remote_filename)

        with smb3.SMB3(connection, smb_share) as smb:
            with open(local_filepath, "rb") as local_file:
                smb.put(remote_file_path, local_file)

        self.smb_disconnect(connection)

     # TemplatePlugin mixin
    def get_template_configs(self):
        return [
            {
                "type": "sidebar",
                "name": "SMB",
                "custom_bindings": True,
                "data_bind": "visible: loginState.isAdmin",
            }
        ]

        # AssetPlugin mixin
    def get_assets(self):
        return {
            "js": ["js/smb.js"],
            "css": ["css/smb.css"]
        }


    # SimpleApiPlugin mixin
    def get_api_commands(self):
        return {
            "connect": ["smb_host", "smb_username", "smb_password", "smb_share", "smb_directory"]
        }

    def on_api_command(self, command, data):
        if command == "connect":
            smb_host = data["smb_host"]
            smb_username = data["smb_username"]
            smb_password = data["smb_password"]
            smb_share = data["smb_share"]
            smb_directory = data["smb_directory"]

            self._settings.set(["smb_host"], smb_host)
            self._settings.set(["smb_username"], smb_username)
            self._settings.set(["smb_password"], smb_password)
            self._settings.set(["smb_share"], smb_share)
            self._settings.set(["smb_directory"], smb_directory)
            self._settings.save()

            file_list = self.smb_list_directory()

            return flask.jsonify(file_list=file_list)