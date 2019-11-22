function partidaDoble() {
        var debe = document.getElementsByClassName("debe form-control");
        var haber = document.getElementsByClassName("haber form-control");
        var acumdeb = 0;
        var acumhab = 0;
        var val=0;

        for (i = 0; i < debe.length; i++) {
            if(debe[i].value==""){
                val=0;
            }else{
                val=parseFloat(debe[i].value);
            }

            acumdeb = acumdeb + val;
        }

        val=0;
        for (j = 0; j < haber.length; j++) {
            if(haber[j].value==""){
                val=0;
            }else{
                val=parseFloat(haber[j].value);
            }
            acumhab = acumhab + val;  
        }
        
        document.getElementById("resultadodeb").innerHTML = acumdeb.toFixed(2);
        document.getElementById("resultadohab").innerHTML = acumhab.toFixed(2);
    }