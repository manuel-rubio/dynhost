function set_redirect_user() {
    value = document.getElementById('id_type').checked;
    username_field = document.getElementById('id_username');
    if (value) {
        username_field.disabled = true;
        username_field.value = '';
    } else {
        username_field.disabled = false;
    }
}

function set_redirect_user_onload() {
    check = document.getElementById('id_type');
    value = document.getElementById('id_username');
    if (value.value == '') {
        check.checked = true;
        value.disabled = true;
    }
}

if (window.addEventListener) { // W3C standard
  window.addEventListener('load', set_redirect_user_onload, false); // NB **not** 'onload'
} else if (window.attachEvent) { // Microsoft
  window.attachEvent('onload', set_redirect_user_onload);
}
