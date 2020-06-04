$(document).ready(function () {

    $('.order-box .item-arrow').click(function () {
        $(this).closest('.order-box').toggleClass('open');
    });

});