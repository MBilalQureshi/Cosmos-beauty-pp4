// function loadDomContent() {
//     x = document.getElementsByClassName("add-to-wishlist")[0];
//     x.addEventListener("click", checkUserName);
//     function checkUserName(){
//     if (this.innerHTML === "Add to wishlist") {
//         this.innerHTML = "Remove from wishlist";
//     } else {
//         this.innerHTML = "Add to wishlist";
//     }
//     }
// }
$(document).ready(function(){
    // $('.add-to-wishlist').click(function(){
    //     $(this).text($(this).text() == 'Add to wishlist' ? 'Remove from wishlist' : 'Add to wishlist');
    // });
    // $(".add-to-wishlist").click(function () {
    //     $(this).text(function(i, v){
    //        return v === 'PUSH ME' ? 'DON"T PUSH ME' : 'PUSH ME'
    //     })
    // });
    $('.add-to-wishlist').click(function(e){
        e.preventDefault();
        // $(this).text($(this).text() == 'Add to wishlist' ? 'Remove from wishlist' : 'Add to wishlist');
        // var z = document.getElementById(profileid);
        // if (z.value == "Add to wishlist") x.value = "Invite";
        $(this).text(function(i, v){
            return v == 'Add to wishlist' ? 'Remove from wishlist' : 'Add to wishlist'
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
            // success: function(json){},
            // error: function(xhr, errmsg, err){}
            success: function (response){
                console.log(response.status)
            }
        });
    });
});