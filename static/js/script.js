$(document).ready(function () {

    /**
     * The product details page is being reloaded if user presses
     * back from cart. This is beacuse sometimes. Buttons are not
     * maintaing the states so requires a reload. Better solution
     * is to handle with AJAX. I'll do it in future releases.
     * https://stackoverflow.com/questions/43043113/how-to-force-reloading-a-page-when-using-browser-back-button
     */
    window.addEventListener("pageshow", function (event) {
        let isDetailsPage = window.location.pathname.includes('/details');
        let isCart = window.location.pathname.includes('/cart');
        let navigationEntries = performance.getEntriesByType('navigation');
        if ((isDetailsPage || isCart) && navigationEntries.length > 0 && navigationEntries[0].type === 'back_forward') {
            window.location.reload();
        }
    });

    /**
     * This Bootstarp 5 code handles the toast appears on webpage.
     * https://getbootstrap.com/docs/5.3/components/toasts/
     */
    let toasts = document.querySelectorAll('.toast');
    if (toasts.length > 0) {
        let toastContainer = new bootstrap.Toast(toasts[0], {
            autohide: false
        });
        toasts.forEach(function (toast) {
            toastContainer.show(toast);
            setTimeout(function () {
                toastContainer.hide();
            }, 3000);
        });
    }

    /**
     * Add / remove products to wishlist using AJAX.
     * Concept of AJAX handling is learned from
     * 1. https://docs.djangoproject.com/en/3.2/ref/csrf/#ajax
     * 2. https://www.youtube.com/watch?v=kD2vWOZFFcw
     */
    $('.add-to-wishlist').click(function (e) {
        e.preventDefault();
        $(this).text(function (i, text) {
            text = text.trim();
            return text == 'Add to wishlist' ? 'Remove from wishlist' : 'Add to wishlist';
        });
        let productId = $(this).attr("value");
        let token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            method: "POST",
            url: '/add-to-wishlist/',
            data: {
                productId: productId,
                csrfmiddlewaretoken: token
            },
            success: function (response) {}
        });
    });

    /**
     * Add / remove products to cart using AJAX.
     */
    $('.add-to-cart').click(function (e) {
        e.preventDefault();
        $(this).text(function (i, text) {
            text = text.trim();
            return text == 'Add to cart' ? 'Remove from cart' : 'Add to cart';
        });
        let productId = $(this).attr("value");
        let token = $('input[name=csrfmiddlewaretoken]').val();
        let productQuantity = parseInt($('.input-number').val());
        let price = $('.product-price').html();
        let discount = $('.product-discount').html();
        $.ajax({
            method: "POST",
            url: '/add-to-cart/',
            data: {
                productId: productId,
                csrfmiddlewaretoken: token,
                productQuantity: productQuantity,
                price: price,
                discount: discount,
            },
            success: function (response) {
                if (response.success) {
                }
            }
        });
    });


    /**
     * Product removal handler from with in cart.
     */
    $('.product-remove').click(function (e) {
        e.preventDefault();
        let productId = $(this).attr("value");
        $(`.${productId}`).remove();
        $('#continue-btn').css('display', 'none');
        let token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            method: "POST",
            url: '/cart/',
            data: {
                productId: productId,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {
                window.location.reload();
            }
        });
    });


    /**
     * This event removes warnings once user click on
     * quantity input field on product details page.
     */
    $('#form-quntity').click(function (e) {
        e.preventDefault();
        $(".form-errors").hide();
    });


    /**
     * Below code till very end handles the quantity on products detail page.
     * This code is required as this input was not part of form
     * and input was handled by session later. So input handling
     * was required. This ready to use code is taken from : 
     * https://www.codeply.com/go/2VmBU7TanF/bootstrap-plus-minus-counter-input
     * Altough input field is handled in below code but I still disabled it on
     * html side to be on safe side. User can use + and - to increase and decrease quantity.
     */
    $('.btn-number').click(function (e) {
        e.preventDefault();
        let fieldName = $(this).attr('data-field');
        let type = $(this).attr('data-type');
        let input = $("input[name='" + fieldName + "']");
        let currentVal = parseInt(input.val());
        if (!isNaN(currentVal)) {
            if (type == 'minus') {

                if (currentVal > input.attr('min')) {
                    input.val(currentVal - 1).change();
                }
                if (parseInt(input.val()) == input.attr('min')) {
                    $(this).attr('disabled', true);
                }
            } else if (type == 'plus') {

                if (currentVal < input.attr('max')) {
                    input.val(currentVal + 1).change();
                }
                if (parseInt(input.val()) == input.attr('max')) {
                    $(this).attr('disabled', true);
                }
            }
        } else {
            input.val(0);
        }
    });

    $('.input-number').focusin(function () {
        $(this).data('oldValue', $(this).val());
    });

    $('.input-number').change(function () {
        let minValue = parseInt($(this).attr('min'));
        let maxValue = parseInt($(this).attr('max'));
        let valueCurrent = parseInt($(this).val());
        let name = $(this).attr('name');


        if (valueCurrent >= minValue) {
            $(".btn-number[data-type='minus'][data-field='" + name + "']").removeAttr('disabled');
        } else {
            $(".form-errors").text('Kindly enter between 1 - 10').show();
            $(this).val($(this).data('oldValue'));
        }
        if (valueCurrent <= maxValue) {
            $(".btn-number[data-type='plus'][data-field='" + name + "']").removeAttr('disabled');
        } else {
            $(".form-errors").text('Kindly enter between 1 - 10').show();
            $(this).val($(this).data('oldValue'));
        }
    });
});