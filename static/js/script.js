$(document).ready(function(){

    // remove messages in 3 seconds
    // setTimeout(function(){
    //     let messages = document.getElementById("msg");

    //     if (messages) {
    //         let alert = new bootstrap.Alert(messages);
    //         alert.close();
    //     }
    // },3000);

    // Add/remove from wishlist
    $('.add-to-wishlist').click(function(e){
        e.preventDefault();

        $(this).text(function(i, text){
            text = text.trim()
            return text == 'Add to wishlist' ? 'Remove from wishlist' : 'Add to wishlist'
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
            // // success: function(json){},
            // // error: function(xhr, errmsg, err){}
            success: function (response){
                // console.log(response)
                // console.log(response.status)
            }
        });
    });

    // Add/remove from cart
    $('.add-to-cart').click(function(e){
        e.preventDefault();
        $(this).text(function(i, text){
            text = text.trim()
            return text == 'Add to cart' ? 'Remove from cart' : 'Add to cart'
        });
        let productId = $(this).attr("value");
        let token = $('input[name=csrfmiddlewaretoken]').val();
        let productQuantity = parseInt($('.input-number').val());
        console.log(productQuantity)
        let price = $('.product-price').html();
        console.log(price)
        let discount = $('.product-discount').html();
        console.log(discount)
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
            // // success: function(json){},
            // // error: function(xhr, errmsg, err){}
            success: function (response){
                // console.log(response)
                // console.log(response.status)
            }
        });
    });

    $('.product-remove').click(function(e){    
        e.preventDefault();
        console.log(12232)
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
            // // success: function(json){},
            // // error: function(xhr, errmsg, err){}
            success: function (response){
                // $('#continue-btn').prop('disabled', false);
                
                window.location.reload()
                // console.log(response)
                // console.log(response.status)
            }
        });
    });

    $('#form-quntity').click(function(e) {
        e.preventDefault();
        $(".form-errors").hide();
    });

    $('.btn-number').click(function(e){
        e.preventDefault();
        
        fieldName = $(this).attr('data-field');
        type      = $(this).attr('data-type');
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
        
        minValue =  parseInt($(this).attr('min'));
        maxValue =  parseInt($(this).attr('max'));
        valueCurrent = parseInt($(this).val());
        console.log(valueCurrent + 'asdasd')
        let name = $(this).attr('name');

        if(valueCurrent >= minValue) {
            $(".btn-number[data-type='minus'][data-field='"+name+"']").removeAttr('disabled')
        } else {
            // console.log(1)
            // alert('Sorry, the minimum value was reached');
            $(".form-errors").text('Sorry, the minimum value was reached').show();
            $(this).val($(this).data('oldValue'));
        }
        if(valueCurrent <= maxValue) {
            $(".btn-number[data-type='plus'][data-field='"+name+"']").removeAttr('disabled')
        } else {
            // alert('Sorry, the maximum value was reached');
            $(".form-errors").text('Sorry, the maximum value was reached').show();
            $(this).val($(this).data('oldValue'));
        }
        
    });
    // $(".input-number").keydown(function (e) {
    //         // Allow: backspace, delete, tab, escape, enter and .
    //         if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
    //              // Allow: Ctrl+A
    //             (e.keyCode == 65 && e.ctrlKey === true) || 
    //              // Allow: home, end, left, right
    //             (e.keyCode >= 35 && e.keyCode <= 39)) {
    //                  // let it happen, don't do anything
    //                  return;
    //         }
    //         // Ensure that it is a number and stop the keypress
    //         if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
    //             e.preventDefault();
    //         }
    //     });

});