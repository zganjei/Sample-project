$(document).ready(function () {

    const $complementPage = $('#complement-page');

    $complementPage.find('.add-child').click(function () {

        let childName = $complementPage.find('.child-name-main').val().trim();
        if (!childName) {
            alertify.dismissAll();
            alertify.error('لطفا نام فرزندتان را وارد نمایید');
            return;
        }
        $complementPage.find('.child-name-main').val('');

        let $childBox = $('#temp-child-box').clone().removeAttr('id').removeAttr('hidden');
        $childBox.find('div.child-name').html(childName);
        $childBox.find('input.child-name').val(childName);

        $complementPage.find('.child-container').append($childBox);


        checkChildrenInputs();

    });

    $(document).on('click', '.child-box .remove', function () {
        $(this).closest('.child-box').remove();
        checkChildrenInputs();
    });


    $complementPage.find('.submit-form').click(function () {
        let password = $('[name=password]').val();
        let repassword = $('[name=repassword]').val();
        let first_name = $('[name=first_name]').val();
        let last_name = $('[name=last_name]').val();

        if (!password) {
            alertify.dismissAll();
            alertify.error('لطفا رمز عبور را وارد نمایید');
            return;
        }
        if (password.length < 6) {
            alertify.dismissAll();
            alertify.error('رمز عبور باید حداقل 6 کاراکتر باشد');
            return;
        }
        if (password !== repassword) {
            alertify.dismissAll();
            alertify.error('رمز عبور با تکرار آن مطابقت ندارد');
            return;
        }
        if (!last_name) {
            alertify.dismissAll();
            alertify.error('لطفا نام خانوادگی خود را وارد نمایید');
            return;
        }

        $complementPage.find('.child-box').each(function () {
            $(this).find('.birth-date-input').val($(this).find('.birth-date').html().trim() || '');
        });

        $complementPage.submit();
    });


});


function checkChildrenInputs() {
    let i = 1;
    $('#complement-page').find('.child-box').each(function () {
        $(this).find('input, .birth-date').each(function () {
            let inputName = $(this).attr('name');
            if (inputName.indexOf('-') > -1) {
                inputName = inputName.substring(0, inputName.indexOf('-'))
            }
            $(this).attr('name', inputName + '-' + i);
        });

        $(this).find('.birth-date, .calendar-img, .birth-date-label').MdPersianDateTimePicker({
            Placement: 'bottom',
            Trigger: 'click',
            TargetSelector: '[name=birth-' + i + ']',
            EnableTimePicker: false,
            Disabled: false,
            Format: 'yyyy/MM/dd',
            ToDate: false,
            FromDate: false,
            IsGregorian: false,
            EnglishNumber: false,
        });

        i += 1;

    });
}