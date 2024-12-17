$(document).ready(function() {
    $('#uploadForm').on('submit', function(event) {
        event.preventDefault();
        
        let formData = new FormData();
        formData.append('image', $('#imageInput')[0].files[0]);

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                $('#outputPopup').text(JSON.stringify(response, null, 2)).show();
            },
            error: function(jqXHR) {
                $('#outputPopup').text('Error: ' + jqXHR.responseText).show();
            }
        });
    });
});
