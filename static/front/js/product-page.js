$(document).ready(function () {
    $('.product-rate-select').barrating({
        theme: 'fontawesome-stars-o',
        emptyValue: '',
        initialRating: $('.product-rate-select').attr('data-value'),
        readonly: true
    });
    $('.review-rate-show').barrating({
        theme: 'fontawesome-stars-o',
        emptyValue: '',
        readonly: true
    });
    $('.send-review-rate').barrating({
        theme: 'fontawesome-stars-o',
        emptyValue: '',
    });


    $('.open-review').click(function () {
        $(this).fadeOut(300, function () {
            $('.send-review-box').fadeIn();
        });
    });


    $('.review-likes .positive, .review-likes .negetive').click(function () {
        var $reviewBox = $(this).closest('.review-box');
        var reviewId = $reviewBox.attr('data-id');
        var positive = $(this).hasClass('positive');
        $.ajax({
            url: sendReviewLike,
            data: {'review_id': reviewId, 'positive': positive},
            method: 'POST',
            success: function (res) {
                if (res.success) {
                    $reviewBox.find('.review-likes .positive').html(res.positive_text);
                    $reviewBox.find('.review-likes .negetive').html(res.negative_text);
                }
                // toastr.clear();
                // toastr.success('آیتم به سبد خرید اضافه شد');
            }
        });
    });


    $('.gallery-images').slick({
        infinite: false,
        slidesToShow: 5,
        slidesToScroll: 5,
        rtl: true,
        prevArrow: '<div class="right-arrow"></div>',
        nextArrow: '<div class="left-arrow"></div>',
        adaptiveHeight: true,
        responsive: [
            {
                breakpoint: 900,
                settings: {
                    slidesToShow: 5.5,
                    slidesToScroll: 5
                }
            }
        ]
    });

    $('.add-reminder-btn').click(function () {
        $.ajax({
            url: productReminderUrl,
            data: {'product-code': $(this).attr('product-code')},
            method: 'GET',
            success: function (res) {
                alertify.dismissAll();
                if (res.success) {
                    alertify.success(res.message);
                } else {
                    alertify.error(res.message);
                }
            }
        });
    });

});