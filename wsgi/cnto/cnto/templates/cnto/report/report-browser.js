$(document).ready(function() {
    var reportUrl = "/get-report-body";
    $.get(reportUrl, function (data) {
        var tpl = _.template($("#report-body-template").html());
        $("#report-container").html(tpl(data));
    });
});
