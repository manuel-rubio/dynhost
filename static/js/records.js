function set_fields() {
    value = document.getElementById('id_type').value;
    mx_block = document.getElementById('mx').style;
    cname_block = document.getElementById('cname').style;
    mx_field = document.getElementById('id_mx_priority');
    cname_field = document.getElementById('id_host');
    switch (value) {
        case "A":
        case "CNAME":
            cname_block.visibility = 'visible';
            mx_block.visibility = 'hidden';
            mx_field.value = '';
            break;
        case "MX":
            cname_block.visibility = 'hidden';
            mx_block.visibility = 'visible';
            mx_field.value = '0';
            cname_field.value = '@';
            break;
        case 'TXT':
            cname_block.visibility = 'hidden';
            mx_block.visibility = 'hidden';
            mx_field.value = '';
            cname_field.value = '@';
            break;
    }
}

if (window.addEventListener) { // W3C standard
  window.addEventListener('load', set_fields, false); // NB **not** 'onload'
} else if (window.attachEvent) { // Microsoft
  window.attachEvent('onload', set_fields);
}
