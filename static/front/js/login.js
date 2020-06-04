$(document).ready(function () {

    if ($('.countdown-clock').length > 0) {
        const clock = $('.countdown-clock').FlipClock({
            clockFace: 'MinuteCounter',
            autoStart: false,
            countdown: true,
            lang: true,
            language: 'fa',
            callbacks: {
                stop: function () {
                    $('#login-page').addClass('stopped-clock')
                }
            }
        });

        clock.setTime(59);
        clock.start();
    }


    $('#login-page .confirm-submit').click(function (e) {
        let code = $('#login-page [name=code]').val();
        $.ajax({
            url: confirmAjaxUrl,
            data: {'code': code},
            method: 'POST',
            success: function (res) {
                if (res.success) {
                    $('#login-page').submit();
                } else {
                    alertify.dismissAll();
                    alertify.error(res.message);
                }
            }
        });
        e.preventDefault();
        e.stopPropagation();
    });

});