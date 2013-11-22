function parseCurrency(integer) {
    return integer.toFixed(2);
}

function set_value() {
    switch ($('#paytype').val()) {
        case "A":
            $('#price').html(parseCurrency(price * 12));
            break;
        case "T":
            $('#price').html(parseCurrency(price * 3));
            break;
        case "M":
            $('#price').html(parseCurrency(price));
            break;
    }
};

var price;
$(document).ready(function() {
    price = parseFloat($('#price').html().replace(",", "."));
});
