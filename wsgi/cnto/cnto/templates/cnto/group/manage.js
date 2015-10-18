$('.delete-group').on('click', function () {
        var groupElement = $(this);
        bootbox.confirm("Are you sure you wish to delete this group?", function (result) {
            if (result) {
                var deleteUrl = "/delete-group/" + getPKFromElement(groupElement).toString();
                $('#delete-modal').modal('show');
                $.get(deleteUrl, function (data) {
                    window.location.reload();
                });
            }
        });
    });

    $('.edit-group').on('click', function (e) {
        e.preventDefault();
        var groupElement = $(this);
        window.location = "/edit-group/" + getPKFromElement(groupElement).toString();
    });

    $('#create-group').on('click', function () {
        window.location = "/{{ 'create-group' }}";
    });