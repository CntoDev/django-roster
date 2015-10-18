$('.delete-member').on('click', function (e) {
    e.preventDefault();
    var memberElement = $(this);
    bootbox.confirm("Are you sure you wish to delete this member?", function (result) {
        if (result) {
            var deleteUrl = "{% url 'delete-member' 1 %}".replace(1, CNTOUtils.getPKFromElement(memberElement).toString());
            $('#deleting-member-modal').modal('show');
            $.get(deleteUrl, function (data) {
                window.location.reload();
            });
        }
    });
});