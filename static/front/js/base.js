$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});


$(document).ready(function () {

    $('.related-container').slick({
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
                    slidesToShow: 1.3,
                    slidesToScroll: 1
                }
            }
        ]
    });


    $(document).off("click.fb-start", "[data-trigger]");

    let searchTimeout;
    let $searchResBox = $('.search-res-box');
    let liSelected;
    $(".search-input").keyup(function (e) {
        let listItems = $searchResBox.find(".item-list li");
        let next;
        if (e.which === 40) {
            if (liSelected) {
                liSelected.removeClass('selected');
                next = liSelected.next();
                if (next.length > 0) {
                    liSelected = next.addClass('selected');
                } else {
                    liSelected = listItems.eq(0).addClass('selected');
                }
            } else {
                liSelected = listItems.eq(0).addClass('selected');
            }
        } else if (e.which === 38) {
            if (liSelected) {
                liSelected.removeClass('selected');
                next = liSelected.prev();
                if (next.length > 0) {
                    liSelected = next.addClass('selected');
                } else {
                    liSelected = listItems.last().addClass('selected');
                }
            } else {
                liSelected = listItems.last().addClass('selected');
            }
        } else if (e.which === 13) {
            let selectedItem = $searchResBox.find(".item-list li.selected");
            if (selectedItem.length > 0) {
                selectedItem.find('a').trigger('click');
                e.preventDefault();
                e.stopPropagation();
            } else {
                let searchTerm = $('.search-input').val() || '';
                window.location.href = $('.header-search').attr('data-url') + '?q=' + searchTerm;
            }
        } else {
            let term = $(this).val().trim();

            if (term.length > 2) {

                $searchResBox.find('.message').html('در حال جستجو ...');


                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(function () {
                    $.ajax({
                        type: 'GET',
                        url: autoCompleteUrl,
                        data: {
                            'q': term
                        },
                        success: function (msg) {
                            let res = eval(msg).res;

                            $searchResBox.find(".item-list").empty();

                            if (res) {
                                $searchResBox.find(".item-list").html(res);
                                $searchResBox.find('.message').html('');
                            } else {
                                $searchResBox.find('.message').html('کالای مورد نظر یافت نشد');
                            }

                        }
                    });
                }, 700);

                $('.header-search').addClass('open');
                e.stopPropagation();
            }
        }
    });

    $(document).on('click', '.search-res-box .item-list a', function (e) {

        let productId = $(this).attr('data-id');
        let productPageUrl = $(this).attr('href');

        $.ajax({
            type: 'GET',
            url: autoCompleteLogUrl,
            data: {
                'q': $(".search-input").val().trim(),
                'product': productId
            },
            success: function (msg) {
                let res = eval(msg);
                if (res.success) {
                    window.location.href = productPageUrl;
                }
            }
        });

        e.stopPropagation();
        e.preventDefault();
    });


    $('.search-btn').click(function () {
        let searchTerm = $('.search-input').val() || '';
        window.location.href = $('.header-search').attr('data-url') + '?q=' + searchTerm;
    });


    $(document).click(function (e) {
        let target = e.target;
        if (!$(target).is('.header-search') && !$(target).parents().is('.header-search')) {
            $('.header-search').removeClass('open');
        }
    });


    $('.check-box').click(function () {
        if ($(this).find('input[type=radio]').is(":checked")) {
            $(this).find('input[type=radio]').attr("checked", false);
            $(this).find('input[type=radio]').prop("checked", false);
        } else {
            $(this).find('input[type=radio]').attr("checked", true);
            $(this).find('input[type=radio]').prop("checked", true);
        }
    });

    $('.check-box').find('input[type=radio]').click(function (e) {
        e.stopPropagation();
    });


    // HAS LOADING BOX
    let $loadMoreBox = $('.load-more-box');
    if ($loadMoreBox.length > 0) {
        let onLoading = false;
        $(document).on('scroll', function () {

            let $loading = $('.load-more-box + .loading-box');

            let pageTop = $(window).scrollTop();
            let pageBottom = pageTop + $(window).height();
            let elementTop = $loadMoreBox.offset().top;
            let elementBottom = elementTop + $loadMoreBox.height();

            if (pageBottom >= elementBottom && !onLoading && $loadMoreBox.attr('data-has-next') === 'true') {
                onLoading = true;
                $loading.addClass('show');
                let url = $loadMoreBox.attr('data-url');
                let searchFormParams = $('#filter-box').find('form').serialize();
                if (searchFormParams)
                    url += '?' + searchFormParams;
                else {
                    let searchTerm = $('.product-search').val() || $('.search-input').val() || '';
                    url += '?q=' + searchTerm;
                }
                $.ajax({
                    url: url,
                    data: {'page': $loadMoreBox.attr('data-page')},
                    method: 'GET',
                }).done(function (res) {
                    $loadMoreBox.append(res.res);
                    $loadMoreBox.attr('data-has-next', res.has_next);
                    $loadMoreBox.attr('data-page', res.page_number);
                }).fail(function () {
                }).always(function () {
                    onLoading = false;
                    $loading.removeClass('show');
                });
            }

        });
    }


    // MOBILE VIEW
    $('#header').find('.header-menu').click(function () {
        $('body').addClass('mobile-menu-open');
    });

    $('#gray-overlay').click(function () {
        $('body').removeClass('mobile-menu-open');
    });

    $('#mobile-menu').find('.close').click(function () {
        $('body').removeClass('mobile-menu-open');
    });
});

function addToCartBtn(url) {
    $.ajax({
        url: url,
        data: {},
        method: 'GET',
        success: function (res) {
            alertify.dismissAll();
            if (res.success) {
                $('.cart-total-count').html(res.total_count);
                alertify.success(res.message);
            } else {
                alertify.error(res.message);
            }
        }
    });
};