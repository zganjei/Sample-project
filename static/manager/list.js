$(document).ready(function () {

    $('.filter-form select, .action-form select:not(.noselect2)').each(function () {
        if ($(this).parents('.formset_fieldset').length === 0)
            $(this).select2({
                minimumResultsForSearch: 99,
                width: '100%',
                dir: 'rtl'
            });
    });

    $('.filter-form input[type=text]').addClass('form-control');

    $('.filter-form .filter-reset').click(function () {
        $('.filter-form input[type="checkbox"]').iCheck('uncheck');
        $('.filter-form select').val('').trigger('change');
        $('.filter-form select.django-select2 option').remove();
    });


    $('.form-control .checkbox').each(function () {
        $(this).parent().removeClass('form-control');
    });

    $('form').find('[data-form-control="time"]').each(function () {
        var input = $(this);
        input.datetimepicker({
            format: input.data('date-format'),
            datepicker: false,
            timepicker: true,
            mask: false,
            scrollInput: false,
            step: 30,
            lang: input.data('lang')
        });
    });


});