function set_redirect_user() {
    value = $('#id_type:checked').val();
    username_field = $('#id_username');
    if (value) {
        username_field.prop("disabled", true);
        username_field.val("");
    } else {
        username_field.prop("disabled", false);
    }
}

$(document).ready(function(){
    set_redirect_user();
});
