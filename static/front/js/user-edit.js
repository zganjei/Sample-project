$(document).ready(function () {

    $('[name=birth_date]').MdPersianDateTimePicker({
        Placement: 'bottom',
        Trigger: 'click',
        TargetSelector: '[name=birth_date]',
        EnableTimePicker: false,
        Disabled: false,
        Format: 'yyyy/MM/dd',
        ToDate: false,
        FromDate: false,
        IsGregorian: false,
        EnglishNumber: false,
    });

});