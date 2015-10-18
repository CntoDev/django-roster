    $('.delete-member').on('click', function () {
        var memberElement = $(this);
        bootbox.confirm("Are you sure you wish to delete this member?", function (result) {
            if (result) {
                var deleteUrl = "/delete-member/" + getPKFromElement(memberElement).toString();
                $('#delete-modal').modal('show');
                $.get(deleteUrl, function (data) {
                    window.location.reload();
                });
            }
        });
    });

    $('.edit-member').on('click', function (e) {
        e.preventDefault();
        var memberElement = $(this);
        var editUrl = "/edit-member/" + getPKFromElement(memberElement).toString();
        $.get(editUrl, function (data) {
            window.location = editUrl;
        });
    });

    $('#create-member').on('click', function () {
        window.location = "/{{ 'create-member' }}";
    });