from octoprint.plugin import OctoPrintPlugin

class SMBPlugin(OctoPrintPlugin):
    def initialize(self):
        self._logger.info("SMB Plugin initialized")
