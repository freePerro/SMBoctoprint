$(function () {
    function SMBViewModel(parameters) {
        var self = this;

        self.loginState = parameters[0];

        self.connectSMB = function () {
            // Get the form data
            var formData = new FormData($("#smb_settings_form")[0]);

            // Send an API request to the plugin
            OctoPrint.postJson("plugin/octoprint_smb/connect", formData)
                .done(function (response) {
                    console.log(response);
                    // Handle the response, e.g., update the file list
                })
                .fail(function () {
                    console.error("Error connecting to SMB share");
                });
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: SMBViewModel,
        dependencies: ["loginStateViewModel"],
        elements: ["#smb_plugin_sidebar"],
    });
});
