function select2_search($el, term) {
    $el.select2('open');

    // Get the search box within the dropdown or the selection
    // Dropdown = single, Selection = multiple
    let $search = $el.data('select2').dropdown.$search || $el.data('select2').selection.$search;
    // This is undocumented and may change in the future

    $search.val(term);
    $search.trigger('input');
    let counter = 0;
    let looper = setInterval(function () {
        $('.select2-results__option').trigger("mouseup");
        counter++;
        console.log($('.select2-results__option').length >= 1, counter);
        if (counter > 5) {
            clearInterval(looper);
        }

    }, 40);
}

$(document).ready(function () {

    $("#search-nav input").on("keyup", function () {
        let value = $(this).val().toLowerCase();
        $("#side-menu").find("span").filter(function () {
            if (!($(this).parents().hasClass('nav-header') || $(this).parents().hasClass('input-search'))) {
                $(this).parent().toggle($(this).text().toLowerCase().indexOf(value) > -1)
            }
        });
    }).focus();

    if ($("[data-barcode=select2]").length) {
        $(document).codeScanner({
            minEntryChars: 5,
            disableEnterKey: true,
            onScan: function ($element, barcode) {
                select2_search($("[data-barcode=select2]"), barcode);
            }
        });
    }
    if ($("[data-barcode=simple]").length) {
        $(document).codeScanner({
            minEntryChars: 5,
            onScan: function ($element, barcode) {
                $("[data-barcode=simple]").val(String(barcode).toEnglishDigits());
                // if ($("[data-barcode=simple]").closest('form').length > 0 && $("[data-barcode=simple]").is("[data-submit-on-enter]")) {
                //     $("[data-barcode=simple]").closest('form').submit();
                // }
            }
        });
        setTimeout(function () {
            $("[data-barcode=simple]").get(0).focus();
        }, 1000);
    }

    if ($("[data-barcode=factory]").length) {
        $(document).codeScanner({
            minEntryChars: 5,
            disableEnterKey: true,
            onScan: function ($element, barcode) {
                $("[data-barcode=factory]").val(String(barcode).toEnglishDigits());
            }
        });
    }

    if ($("[data-barcode=ajax]").length) {
        $(document).codeScanner({
            minEntryChars: 5,
            disableEnterKey: true,
            onScan: function ($element, barcode) {
                $("[data-barcode=ajax]").val(barcode);
                $("[data-barcode=ajax]").closest('form').submit();
            }
        });
        setTimeout(function () {
            $("[data-barcode=ajax]").get(0).focus();
        }, 1000);
    }

    if ($("[data-focus]").length)
        setTimeout(function () {
            $("[data-focus]").get(0).focus();
        }, 1000);

    toastr.options = {
        "closeButton": true,
        "debug": false,
        "progressBar": false,
        "positionClass": "toast-bottom-left",
        "onclick": null,
        "showDuration": "400",
        "hideDuration": "5000",
        "timeOut": "10000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };


    $('input[type="checkbox"]').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
    });


    $(document).off("click.fb-start", "[data-trigger]");


    $(document).on('change', '.form-control-file input[type=file]', function () {
        var filename = $(this).val().replace(/^.*[\\\/]/, '');
        $(this).closest('.form-control-file').find('.file-name').html(filename);
    });


    $('input[type=number]').on('wheel', function (e) {
        return false;
    });

});


function notify(tag, message, title) {
    if (tag == 'success') {
        toastr.success(title || "", message, {timeOut: 4000});
    } else {
        toastr.error(title || "", message, {timeOut: 4000});
    }
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }

    }
});


function printValues(values_list) {

    var addRow = function (d, tag) {
        var str = '<tr>';

        for (var i = 0, ien = d.length; i < ien; i++) {
            // null and undefined aren't useful in the print output
            var dataOut = d[i] === null || d[i] === undefined ?
                '' :
                d[i];

            dataOut = String(dataOut).trim();

            str += '<' + tag + ' ' + '>' + dataOut + '</' + tag + '>';
        }

        return str + '</tr>';
    };

    // Construct a table for printing
    var html = '<table class="">';


    html += '<tbody>';

    for (var i = 0, ien = values_list.length; i < ien; i++) {
        html += addRow(values_list[i], 'td');
    }
    html += '</tbody>';

    html += '</table>';

    // Open a new window for the printable table
    var win = window.open('', '');
    win.document.close();

    // Inject the title and also a copy of the style and link tags from this
    // document so the table can retain its base styling. Note that we have
    // to use string manipulation as IE won't allow elements to be created
    // in the host document and then appended to the new window.
    var head = '<title>پرینت بارکدها</title>';
    $('style, link').each(function () {
        head += _styleToAbs(this);
    });

    try {
        win.document.head.innerHTML = head; // Work around for Edge
    }
    catch (e) {
        $(win.document.head).html(head); // Old IE
    }

    // Inject the table and other surrounding information
    win.document.body.innerHTML =
        '<h1>پرینت بارکدها</h1>' +
        html;

    $(win.document.body).addClass('dt-print-view white-bg');

    $('img', win.document.body).each(function (i, img) {
        img.setAttribute('src', _relToAbs(img.getAttribute('src')));
    });

    // Allow stylesheets time to load
    win.setTimeout(function () {
        win.print(); // blocking - so close will not
        // win.close();
    }, 1000);
}


function printTable(title, table) {

    // Construct a table for printing
    var html = table;

    // Open a new window for the printable table
    var win = window.open('', '');
    win.document.close();

    // Inject the title and also a copy of the style and link tags from this
    // document so the table can retain its base styling. Note that we have
    // to use string manipulation as IE won't allow elements to be created
    // in the host document and then appended to the new window.
    var head = '<title>' + title + '</title>';
    $('style, link').each(function () {
        head += _styleToAbs(this);
    });

    try {
        win.document.head.innerHTML = head; // Work around for Edge
    } catch (e) {
        $(win.document.head).html(head); // Old IE
    }

    // Inject the table and other surrounding information
    win.document.body.innerHTML =
        '<h1>' + title + '</h1>' +
        html;

    $(win.document.body).addClass('dt-print-view white-bg padded-window');

    $('img', win.document.body).each(function (i, img) {
        img.setAttribute('src', _relToAbs(img.getAttribute('src')));
    });

    $('.no-print', win.document.body).remove();

    // Allow stylesheets time to load
    win.setTimeout(function () {
        win.print(); // blocking - so close will not
        // win.close();
    }, 1000);
}

var _styleToAbs = function (el) {
    var url;
    var clone = $(el).clone()[0];
    var linkHost;

    if (clone.nodeName.toLowerCase() === 'link') {
        clone.href = _relToAbs(clone.href);
    }

    return clone.outerHTML;
};
var _link = document.createElement('a');
var _relToAbs = function (href) {
    // Assign to a link on the original page so the browser will do all the
    // hard work of figuring out where the file actually is
    _link.href = href;
    var linkHost = _link.host;

    // IE doesn't have a trailing slash on the host
    // Chrome has it on the pathname
    if (linkHost.indexOf('/') === -1 && _link.pathname.indexOf('/') !== 0) {
        linkHost += '/';
    }

    return _link.protocol + "//" + linkHost + _link.pathname + _link.search;
};


function printHtml(content) {

    // Construct a table for printing
    let html = content;

    // Open a new window for the printable table
    let win = window.open('', '');
    win.document.close();

    let head = '';
    $('style, link').each(function () {
        head += _styleToAbs(this);
    });

    try {
        win.document.head.innerHTML = head; // Work around for Edge
    } catch (e) {
        $(win.document.head).html(head); // Old IE
    }


    win.document.body.innerHTML = html;

    $(win.document.body).addClass('dt-print-view white-bg');

    win.setTimeout(function () {
        win.print(); // blocking - so close will not
        // win.close();
    }, 1000);
}
