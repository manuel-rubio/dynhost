function set_fields() {
    value = $('#id_type').val();
    mx_block = $('#mx');
    cname_block = $('#cname');
    mx_field = $('#id_mx_priority');
    cname_field = $('#id_host');
    switch (value) {
        case "A":
        case "CNAME":
            cname_block.removeClass('hidden');
            mx_block.addClass('hidden');
            mx_field.val('');
            break;
        case "MX":
            cname_block.addClass('hidden');
            mx_block.removeClass('hidden');
            mx_field.val('0');
            cname_field.val('@');
            break;
        case "TXT":
            cname_block.addClass('hidden');
            mx_block.addClass('hidden');
            mx_field.val('');
            cname_field.val('@');
            break;
    }
}

$(document).ready(function() {
    set_fields();
});
