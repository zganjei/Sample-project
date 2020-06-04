$(document).ready(function () {


    $('#top-slider').slick({
        infinite: false,
        slidesToShow: 2.5,
        slidesToScroll: 2,
        rtl: true,
        prevArrow: '<div class="right-arrow"></div>',
        nextArrow: '<div class="left-arrow"></div>',
        adaptiveHeight: true,
        responsive: [
            {
                breakpoint: 900,
                settings: {
                    slidesToShow: 1.1,
                    slidesToScroll: 1
                }
            }
        ]
    });


    $('.brands-container').slick({
        infinite: false,
        slidesToShow: 5.5,
        slidesToScroll: 5,
        rtl: true,
        prevArrow: '<div class="right-arrow"></div>',
        nextArrow: '<div class="left-arrow"></div>',
        adaptiveHeight: true,
        responsive: [
            {
                breakpoint: 900,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    variableWidth: true
                }
            }
        ]
    });


    $('#top-slider .main-field').click(function () {
        $(this).toggleClass('active');
        let $check = $(this).find('[type=checkbox]');
        $check.prop("checked", !$check.prop("checked"));
    });


});