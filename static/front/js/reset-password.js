$(document).ready(function () {

    const $complementPage = $('#complement-page');

    $complementPage.find('.submit-form').click(function () {
        let password = $('[name=password]').val();
        let repassword = $('[name=repassword]').val();

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

        $complementPage.submit();
    });


});

