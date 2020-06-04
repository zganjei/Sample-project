$(document).ready(function () {

    const $complementPage = $('#cart-detail-page');


    $complementPage.find('.add-new-address').click(function () {
        $complementPage.find('.location-box').fadeIn();
        $(this).hide();

        $complementPage.find('.check-box').find('input[type=radio]').attr("checked", false);
        $complementPage.find('.check-box').find('input[type=radio]').prop("checked", false);
    });

    $('#submit_btn').click(function(){
        $.post('/users/addresses-validation/', $('#cart-detail-page').serialize(), function(data){
            var obj = JSON.parse(data);
            if(obj.message !== 'success') {
                alertify.error(obj.message);
            }
            else {
                $('#cart-detail-page').submit();
            }
        });
    });
});

