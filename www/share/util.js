window.onload = function() {
    tests = [ /^\/mit\/[^\/]+/, /^\/afs\/[^\/]+/, /^~[^\/]+/ ];
    for (var i = 0; i < tests.length; i++) {
        if (tests[i].test(URI)) {
            $('permissions_menu').show();
            break;
        }
    }
}

var index_errors = [];

function index_error(str) {
    index_errors = index_errors.concat([str]);
    $('index-error').innerHTML = '<ul><li>' + index_errors.join('</li><li>') + '</li></ul>';
}

function ui_open(elt) {
    $('p_1').innerHTML = 'Loading...';
    url = null;
    if (elt == 'permissions') {
        url = '/fs_la?path=' + encodeURIComponent(URI);
    } else if (elt == 'tokens') {
        url = '/tokens';
    }
    if (url != null) {
        $('index').addClassName('greyout');
        new Ajax.Request(url, {
            method: 'get',
            onSuccess: function(transport) {
                $('p_1').update('<br /><pre>' + transport.responseText + '</pre>');
            }
        });
        $('p_0').show();
    }
}

function ui_close(elt) {
    $(elt+'_0').hide();
    $('index').removeClassName('greyout');
}
