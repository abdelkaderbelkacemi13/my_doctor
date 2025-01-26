// handling the logout process
document.getElementById("logoutButton").addEventListener("click", logout)
function logout(){
    // check everything please when you test.
    // the endpoint will be updated later to the exact endpoint.
    fetch("/logout",{
        method : 'GET',
        credentials : 'same-origin',
    })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                console.error("Unable to log out");
            }
        })
}
