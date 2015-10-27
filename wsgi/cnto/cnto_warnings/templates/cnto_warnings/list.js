$('.toggle-acknowledge-warning').on('click', function (e) {
    e.preventDefault();
    console.log("WARNING");

    var warningInput = $(this);
    var initialChecked = !warningInput.prop('checked');
    var oppositeChecked = !initialChecked;

    var acknowledgeUrl = "{% url 'toggle-warning-acknowledge' 1 %}".replace(1, CNTOUtils.getPKFromElement(warningInput).toString());
    $('#acknowledging-warning-modal').modal('show');
    $.get(acknowledgeUrl, function (data) {
        if (data["success"]) {
            warningInput.prop('checked', oppositeChecked);
        } else {
            warningInput.prop('checked', initialChecked);
        }

        $('#acknowledging-warning-modal').modal('hide');
    });
});
