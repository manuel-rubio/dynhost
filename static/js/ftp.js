
jQuery(function($) {
    $('#container')
    .jstree({
        "plugins": ["themes","html_data","ui"],
        "core": {
            "url": "/static/",
            "strings": {
                "loading": "Cargando..."
            },
            "select_limit": 1,
            "initially_open": []
        },
        "ui": {
            "initially_select": [$('#id_homedir').val()]
        }
    })
    .bind('select_node.jstree', function(evt, data) {
        var id = data.rslt.obj.attr('id');
        $('#id_homedir').val(id);
    })
    .delegate("a", "click", function(evt, data) { evt.preventDefault(); });
});
