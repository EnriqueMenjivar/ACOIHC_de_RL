function validar() {
    acumdeb = parseFloat(document.getElementById("resultadodeb").innerHTML);
    acumhab = parseFloat(document.getElementById("resultadohab").innerHTML);
    if (acumdeb != acumhab || acumhab == 0 || acumdeb == 0) {
        document.getElementById("error").classList.remove("hidden");
        $('body, html').animate({
            scrollTop: '0px'
        }, 300);
    }else{
         $("#save").click();
    }
}