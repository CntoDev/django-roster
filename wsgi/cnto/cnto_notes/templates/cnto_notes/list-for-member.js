$('.activate-note').on('click', function (e) {
    e.preventDefault();

    var activateInput = $(this);
    var initialChecked = !activateInput.prop('checked');
    var oppositeChecked = !initialChecked;

    if (initialChecked) {
        return;
    }

    $('.activate-note').prop('checked', false);

    var acknowledgeUrl = "{% url 'activate-note' 1 %}".replace(1, CNTOUtils.getPKFromElement(activateInput).toString());
    $('#activating-note-modal').modal('show');
    $.get(acknowledgeUrl, function (data) {
        if (data["success"]) {
            activateInput.prop('checked', oppositeChecked);
        } else {
            activateInput.prop('checked', initialChecked);
        }

        $('#activating-note-modal').modal('hide');
    });
});

$('.delete-note').on('click', function (e) {
    e.preventDefault();
    var element = $(this);
    bootbox.confirm("Are you sure you wish to delete this note?", function (result) {
        if (result) {
            var deleteUrl = "{% url 'delete-note' 1 %}".replace(1, CNTOUtils.getPKFromElement(element).toString());
            $('#deleting-note-modal').modal('show');
            $.get(deleteUrl, function (data) {
                window.location.reload();
            });
        }
    });
});
