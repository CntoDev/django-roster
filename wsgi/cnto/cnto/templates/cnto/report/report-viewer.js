$(document).ready(function () {
    $('#generate-report-throbber').hide();

    $("#month-picker").datetimepicker({
                                          defaultDate: moment().subtract(1, 'months'),
                                          viewMode: 'months',
                                            format: 'YYYY-MM'
                                      }
    );

    $('#generate-report').on('click', function (e) {
        $('#generate-report-throbber').show();
        var dateString = $("#selected-date-text").val();
        var reportUrl = "{% url 'get-report-body-for-month' '1234-56' %}".replace('1234-56', dateString);
        $.get(reportUrl, function (data) {
            $('#generate-report-throbber').hide();
            var tpl = _.template($("#report-body-template").html());
            $("#report-container").html(tpl(data));
        });
    });
});