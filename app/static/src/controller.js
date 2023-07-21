$(document).ready(function () {
    $("#submit").click(function () {
        $.ajax({
            type: "POST",
            url: "{{url_for('control')}}",
            contentType: "application/json;charset=UTF-8",
            data: {'data':$("#controlInput").val()},
        });
    });
});
