$(document).ready(function(){
    /**
     * Add / remove products to wishlist AJAX handler.
     * Concept of AJAX handling is learned from
     * 
     */
    $('.add-to-wishlist').click(function(e){
        e.preventDefault();
        $(this).text(function(i, text){
            text = text.trim();
            return text == 'Add to wishlist' ? 'Remove from wishlist' : 'Add to wishlist';
        });
        let productId = $(this).attr("value");
        let token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            method: "POST",
            url:'/add-to-wishlist/',
            data:{     
                productId: productId,
                csrfmiddlewaretoken: token
            },
            success: function (response){
            }
        });
    });


    /**
     * Add / remove products to cart AJAX handler.
     */
    $('.add-to-cart').click(function(e){
        e.preventDefault();
        $(this).text(function(i, text){
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
            url:'/add-to-cart/',
            data:{
                productId: productId,
                csrfmiddlewaretoken: token,
                productQuantity: productQuantity,
                price:price,
                discount:discount,
            },
            success: function (response){
            }
        });
    });


    /**
     * Product removal handler from with in cart.
     */
    $('.product-remove').click(function(e){
        e.preventDefault();
        let productId = $(this).attr("value");
        $(`.${productId}`).remove();
        $('#continue-btn').css('display', 'none');
        let token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            method: "POST",
            url:'/cart/',
            data:{
                productId: productId,
                csrfmiddlewaretoken: token,
            },
            success: function (response){
                window.location.reload();
            }
        });
    });


    /**
     * This ready to use animation code is taken from ''
     * The effect can be seen above footer on home page.
     */
    $(document).on("scroll", function() {
        let pageTop = $(document).scrollTop();
        let pageBottom = pageTop + $(window).height();
        let tags = $(".tag"); 
        tags.each(function() {
            let tag = $(this);
            if (tag.position().top < pageBottom) {
                tag.addClass("visible");
            } else {
                tag.removeClass("visible");
            }
        });
    });


    /**
     * This event removes warnings once user click on
     * quantity input field on product details page.
     */
    $('#form-quntity').click(function(e) {
        e.preventDefault();
        $(".form-errors").hide();
    });


    /**
     * Below code till very end handles the quantity on products detail page.
     * This code is required as this input was not part of form
     * and input was handled by session later. So input handling
     * was required. This ready to use code is taken from :
     * depricated code was fixed and remaining code was updated
     * as needed.
     */
    $('.btn-number').click(function(e){
        e.preventDefault();
        
        let fieldName = $(this).attr('data-field');
        let type = $(this).attr('data-type');
        var input = $("input[name='"+fieldName+"']");
        var currentVal = parseInt(input.val());
        if (!isNaN(currentVal)) {
            if(type == 'minus') {
                
                if(currentVal > input.attr('min')) {
                    input.val(currentVal - 1).change();
                } 
                if(parseInt(input.val()) == input.attr('min')) {
                    $(this).attr('disabled', true);
                }
            } else if(type == 'plus') {
    
                if(currentVal < input.attr('max')) {
                    input.val(currentVal + 1).change();
                }
                if(parseInt(input.val()) == input.attr('max')) {
                    $(this).attr('disabled', true);
                }
            }
        } else {
            input.val(0);
        }
    });

    $('.input-number').focusin(function(){
       $(this).data('oldValue', $(this).val());
    });

    $('.input-number').change(function() {    
        let minValue =  parseInt($(this).attr('min'));
        let maxValue =  parseInt($(this).attr('max'));
        let valueCurrent = parseInt($(this).val());
        let name = $(this).attr('name');


        if(valueCurrent >= minValue) {
            $(".btn-number[data-type='minus'][data-field='"+name+"']").removeAttr('disabled');
        } else {
            $(".form-errors").text('Sorry, kindly enter between 1 - 10').show();
            $(this).val($(this).data('oldValue'));
        }
        if(valueCurrent <= maxValue) {
            $(".btn-number[data-type='plus'][data-field='"+name+"']").removeAttr('disabled');
        } else {
            $(".form-errors").text('Sorry,  kindly enter between 1 - 10').show();
            $(this).val($(this).data('oldValue'));
        }
    });
});