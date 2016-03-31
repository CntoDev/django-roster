$('.delete-contribution').on('click', function (e) {
    e.preventDefault();
    var groupElement = $(this);
    bootbox.confirm("Are you sure you wish to delete this contribution?", function (result) {
        if (result) {
            var deleteUrl = "{% url 'delete-contribution' 1 %}".replace(1, CNTOUtils.getPKFromElement(groupElement).toString());
            $('#deleting-contribution-modal').modal('show');
            $.get(deleteUrl, function (data) {
                window.location.reload();
            });
        }
    });
});
