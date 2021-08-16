function sendFrndUpdtRq(el,action,userId){
    jQuery.ajax({
        url : "/updaterequest",
        method:"get",
        data:{
            action:action,
            userId:userId
        },
        success:function (){
            el.parentElement.remove()
        },
        error:function (){
            window.location.reload();
        }
    })

}
