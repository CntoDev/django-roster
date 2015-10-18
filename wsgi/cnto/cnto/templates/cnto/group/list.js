$('.delete-group').on('click', function (e) {
    e.preventDefault();
    var groupElement = $(this);
    bootbox.confirm("Are you sure you wish to delete this group?", function (result) {
        if (result) {
            var deleteUrl = "/delete-group/" + CNTOUtils.getPKFromElement(groupElement).toString();
            $('#deleting-group-modal').modal('show');
            $.get(deleteUrl, function (data) {
                window.location.reload();
            });
        }
    });
});