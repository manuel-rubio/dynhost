function setEmailHelp(type) {
    switch (type) {
        case "":
            $('#help-mailboxes').hide();
            $('#help-redirects').hide();
            $('#help-manual').show();
            break;
        case "V":
            $('#help-mailboxes').hide();
            $('#help-redirects').show();
            $('#help-manual').hide();
            break;
        case "R":
            $('#help-mailboxes').show();
            $('#help-redirects').hide();
            $('#help-manual').hide();
            break;
    }
}

function checkDelete(id, domain, button, url) {
    if ($("#" + id).val() == domain) {
        $("#" + button).removeClass('disabled');
        $("#" + button).attr("href", url);
    }
}

$(document).ready(function() {
    setEmailHelp($('#email_type').val());
    $('#email_type').change(function() {
        setEmailHelp($('#email_type').val());
    });
});
