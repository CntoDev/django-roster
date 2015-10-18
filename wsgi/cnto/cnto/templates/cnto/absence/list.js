$('.delete-absence').on('click', function (e) {
    e.preventDefault();
    var element = $(this);
    bootbox.confirm("Are you sure you wish to delete this absence?", function (result) {
        if (result) {
            var deleteUrl = "{% url 'delete-absence' 1 %}".replace(1, CNTOUtils.getPKFromElement(element).toString());
            $('#deleting-group-modal').modal('show');
            $.get(deleteUrl, function (data) {
                window.location.reload();
            });
        }
    });
});
