let window_focus;

$(window).focus(function () {
    window_focus = true;
}).blur(function () {
    window_focus = false;
});


function getUrlParameter(sParam) {
    let sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
}

String.prototype.replaceAll = function (search, replacement) {
    let target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

function isImageURL(url) {
    return (url.toLowerCase().match(/\.(jpeg|jpg|gif|png)$/) != null);
}

function max_str(value, size) {
    if (value.length > size) {
        return value.substring(0, size - 1) + '...';
    }
    return value;
}

function strip_tags(str) {
    str = str.toString();
    return str.replace(/<\/?[^>]+>/gi, ' ');
}

String.prototype.format = function () {
    let args = arguments;
    return this.replace(/{(\d+)}/g, function (match, number) {
        return typeof args[number] != 'undefined'
            ? args[number]
            : match
            ;
    });
};

String.prototype.toEnglishDigits = function () {
    let charCodeZero = '۰'.charCodeAt(0);
    return this.replace(/[۰-۹]/g, function (w) {
        return w.charCodeAt(0) - charCodeZero;
    });
};

function isValid(str) {
    return !/[~`!#$%\^&\/|:*?؟"><]/g.test(str);
}


function select2ChangeItems(elem_id, data) {
    let oldVal = $('#' + elem_id).val();

    $('#' + elem_id).empty();
    $('#' + elem_id).append('<option value>---------</option>');

    let hasVal = false;

    data.forEach(function (item) {
        if (item.id == oldVal)
            hasVal = true;
        $('#' + elem_id).append('<option value="{0}">{1}</option>'.format(item.id, item.name));
    });

    if (!hasVal)
        $('#' + elem_id).val('').trigger('change');
    else
        $('#' + elem_id).val(oldVal).trigger('change');
}

function updateFancybox() {
    if (window.parent.$.fancybox.getInstance().update != undefined) {
        let oldScrollTop = window.parent.$('.fancybox-slide').scrollTop();
        window.parent.$.fancybox.getInstance().update();
        window.parent.$('.fancybox-slide').scrollTop(oldScrollTop);
    }
}


const convertToPrice = (x) => {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "،");
};
