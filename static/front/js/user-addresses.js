$(document).ready(function () {


    $('.add-new-address').click(function () {
        $(this).closest('form').find('.location-box').fadeIn();
        $(this).hide();
    });

    $('#submit_btn').click(function(){
        $.post('/users/addresses-validation/', $('#address-form').serialize(), function(data){
            var obj = JSON.parse(data);
            if(obj.message !== 'success') {
                alertify.error(obj.message);
            }
            else {
                $('#address-form').submit();
            }
        });
    });



});

