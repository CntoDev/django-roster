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
