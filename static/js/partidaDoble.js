function partidaDoble() {
    var debe = document.getElementsByClassName("debe form-control");
    var haber = document.getElementsByClassName("haber form-control");
    var acumdeb = 0;
    var acumhab = 0;

    for (i = 0; i < debe.length; i++) {
        acumdeb = acumdeb + parseFloat(debe[i].value);
        
    }
    for (j = 0; j < haber.length; j++) {
        
        acumhab = acumhab + parseFloat(haber[j].value);
        
    }
    console.log(acumdeb);
    document.getElementById("resultadodeb").innerHTML = acumdeb;
    document.getElementById("resultadohab").innerHTML = acumhab;
}