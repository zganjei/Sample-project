$(document).ready(function () {


    $('#filter-btn').click(function () {
        $('#filter-box').fadeToggle();
    });


    let $filterBox = $('#filter-box');

    $filterBox.find('.close').click(function () {
        $('#filter-box').fadeOut();
    });

    $filterBox.find('select[multiple]').select2({
        placeholder: function () {
            return $(this).data('data-placeholder');
        }
    });

    $filterBox.find('.main-field').click(function () {
        $(this).toggleClass('active');
        let $check = $(this).find('[type=checkbox]');
        $check.prop("checked", !$check.prop("checked"));
        $filterBox.find('.submit-filter').trigger('click');
    });

    $filterBox.find('select[multiple], [name=available]').change(function () {
        $filterBox.find('.submit-filter').trigger('click');
    });

    let $productList = $('.product-list-container');

    $filterBox.find('.submit-filter').click(function () {
        $.ajax({
            url: ajaxSearchUrl + '?' + $(this).closest('form').serialize(),
            data: {},
            method: 'GET',
            success: function (res) {
                if (!res.res) {
                    $('#list-message').fadeIn();
                } else {
                    $('#list-message').hide();
                }
                $productList.html(res.res);
                $productList.attr('data-has-next', res.has_next);
                $productList.attr('data-page', res.page_number);

                if (window.matchMedia('(max-width: 800px)').matches) {
                    $('#filter-box').fadeOut();
                }
            }
        });
    });


    $(".product-search").keyup(function (e) {
        if (e.which === 13) {
            let searchTerm = $('.product-search').val() || '';
            window.location.href = $('.header-search').attr('data-url') + '?q=' + searchTerm;
        }
    });


    $('.slide-categories').slick({
        infinite: false,
        slidesToShow: 2.5,
        slidesToScroll: 2,
        rtl: true,
        prevArrow: '<div class="right-arrow"></div>',
        nextArrow: '<div class="left-arrow"></div>',
        adaptiveHeight: true,
    });


    $('#category-filter:not(.slide-categories)').slick({
        infinite: false,
        slidesToShow: 5.5,
        slidesToScroll: 5,
        rtl: true,
        prevArrow: '',
        nextArrow: '',
        adaptiveHeight: true,
    });


});