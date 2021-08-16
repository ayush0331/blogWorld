function processingAnim(action = "push"||"pop", targetId = ""){
    var target = document.getElementById(targetId);
    if (action == "push"){
        target.innerHTML = "<div class=\"lds-ellipsis-parent\"><div class=\"lds-ellipsis\"><div></div><div></div><div></div><div></div></div></div>";
    }else {
        target.innerHTML = "";
    }
}
function reactOnPost(el,postId,objectId,objectType,reaction){

}
function toggleSave(PostId){

}
function deletePost(postId){

}
function deleteComment(){

}
function deleteReply(){

}
