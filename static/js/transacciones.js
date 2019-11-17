$(document).ready(function(){
    function validar() {
        acumdeb = parseFloat(document.getElementById("resultadodeb").innerHTML);
        acumhab = parseFloat(document.getElementById("resultadohab").innerHTML);
        if (acumdeb != acumhab || acumhab==0 ||acumdeb==0) {
            document.getElementById("error").classList.remove("hidden");
            $('body, html').animate({
                scrollTop: '0px'
            }, 300);

            $("#regresar").click();
        }else {
            if($("#f").val().length>0&&$("#d").val().length>0){
                $.ajax({
                    url: "/transaccion/",
                    type: "POST",
                    data: $("#transaccionPost").serialize(),
                    dataType: "json"
                }).done(function(data){
                   location.href="/transaccion/";
                })
                .fail(function(xhr, status, e) {
                    console.log(e);
                });
            }else{
                document.getElementById("error").classList.remove("hidden");
                $("#error").html("<strong>Advertencia!</strong> La fecha y la descripcion de la transaccion son requeridos");
                $("#regresar").click();
            }
        }
    }
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

    $(".valores").keyup(function(){
        console.log("ENTRO");
        partidaDoble();
    });

    $("#inicio_transaccion").click(function(){
        validar();
    })
});