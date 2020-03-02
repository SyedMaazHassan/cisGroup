//function showSignUp() {
//    var mylogin = document.getElementById("login")
//    mylogin.style.display = 'none'
//
//    var mysignup = document.getElementById("signup")
//    mysignup.style.display = 'block'
//}
//
//function showLogin() {
//    var mylogin = document.getElementById("login")
//    mylogin.style.display = 'block'
//
//    var mysignup = document.getElementById("signup")
//    mysignup.style.display = 'none'
//}

function showNow() {
    var x =  document.getElementById("skills");

    if (x.style.display == 'block') {
        document.getElementById("skills").style.display = 'none'
    }else{
        document.getElementById("skills").style.display = 'block'
    }

}

function godown(){
    var x = document.getElementById("mycontent");
    x.scrollIntoView(false)
}



godown()
