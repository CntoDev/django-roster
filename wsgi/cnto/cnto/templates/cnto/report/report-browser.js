$(document).ready(function() {
    var reportUrl = "/get-report-body";
    $.get(reportUrl, function (data) {
        $("#report-container").html(data);
    });
});
