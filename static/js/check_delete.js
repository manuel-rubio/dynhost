function checkDelete(id, domain, button, url) {
    if ($("#" + id).val() == domain) {
        $("#" + button).removeClass('disabled');
        $("#" + button).attr("href", url);
    }
}

