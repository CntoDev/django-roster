$('.delete-event-type').on('click', function (e) {
    e.preventDefault();
    var element = $(this);
    bootbox.confirm("Are you sure you wish to delete this event type?", function (result) {
        if (result) {
            var deleteUrl = "/delete-event-type/" + getPKFromElement(element).toString();
            $('#deleting-event-type-modal').modal('show');
            $.get(deleteUrl, function (data) {
                window.location.reload();
            });
        }
    });
});

$('.edit-event-type').on('click', function (e) {
    e.preventDefault();
    var groupElement = $(this);
    window.location = "/edit-event-type/" + getPKFromElement(groupElement).toString();
});

$('#create-event-type').on('click', function (e) {
    e.preventDefault();
    window.location = "{% url 'create-event-type' %}";
});