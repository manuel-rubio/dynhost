function set_fields() {
    value = $('#id_legalForm').val();
    // association
    org = $('#nic_form_organization');
    // corporation
    legalName = $('#nic_form_legalName');
    legalNumber = $('#nic_form_legalNumber');
    switch (value) {
        case "individual":
            org.addClass('hidden');
            legalName.addClass('hidden');
            legalNumber.addClass('hidden');
            break;
        case "association":
            org.removeClass('hidden');
            legalName.addClass('hidden');
            legalNumber.addClass('hidden');
            break;
        case "corporation":
            org.addClass('hidden');
            legalName.removeClass('hidden');
            legalNumber.removeClass('hidden');
            break;
    }
}

$(document).ready(function() {
    set_fields();
});
