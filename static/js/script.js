$(document).ready(function(){
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
                console.log(response)
                console.log(response.status)
            }
        });
    });
});