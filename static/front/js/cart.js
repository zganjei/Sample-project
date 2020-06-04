$(document).ready(function () {

    $('.order-item .plus, .order-item .minus').click(function () {
        var $orderItem = $(this).closest('.order-item');
        $.ajax({
            url: $(this).attr('data-href'),
            data: {},
            method: 'POST',
            success: function (res) {
                if (res.success) {
                    if (res.count == 0) {
                        $orderItem.remove();
                    } else {
                        $orderItem.find('.count-text').html(res.count);
                        $orderItem.find('.price').html(res.price);
                    }
                    $('#cart-page').find('.total-price span').html(res.total_price);
                    $('.cart-total-count').html(res.total_count);
                    if ($('.order-item').length === 0)
                        location.reload();
                } else if (res.count) {
                    $orderItem.find('.count-text').html(res.count);
                    $orderItem.find('.price').html(res.price);
                    $('#cart-page').find('.total-price span').html(res.total_price);
                    $('.cart-total-count').html(res.total_count);
                    alertify.dismissAll();
                    alertify.error(res.message);
                }
            }
        });
    });

});