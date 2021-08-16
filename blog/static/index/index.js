function switchform(tofrm=1){
    var loginform = document.getElementsByName("loginForm")[0];
    var signupform = document.getElementsByName("reg_form")[0];
    if (tofrm == 2){
        loginform.style.display = "none";
        signupform.style.removeProperty("display");
    }else {
        signupform.style.display = "none";
        loginform.style.removeProperty("display");
    }
}
function validate_pw(){
    var signupform = document.getElementsByName("reg_form")[0];
    if (signupform.password.value === signupform.vf_password.value){
        signupform.vf_password.setCustomValidity("")
    }else{
        signupform.vf_password.setCustomValidity("password do not match")
    }
}
validate_pw();