// $document.ready(function(){
$('.add-to-wishlist').click(function(e){
    e.preventDefault();
    let productId = $(this).attr("value");
    console.log('hey')
    let token = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        method: "POST",
        url:'/add-to-wishlist/',
        data:{     
            productId: productId,
            csrfmiddlewaretoken: token
        },
        // success: function(json){},
        // error: function(xhr, errmsg, err){}
        success: function (response){
            console.log(response.status)
        }
    });
});
// });