function validar() {
    acumdeb = parseFloat(document.getElementById("resultadodeb").innerHTML);
    acumhab = parseFloat(document.getElementById("resultadohab").innerHTML);
    if (acumdeb != acumhab || acumhab == 0 || acumdeb == 0) {
        document.getElementById("error").classList.remove("hidden");
        $("#error").html("<strong>Advertencia!</strong> No se cumple partida doble. Revisar datos de transaccion.");
        $('body, html').animate({
            scrollTop: '0px'
        }, 300);
    }else{
        if( !$('#cj').is(':checked') && !$('#cp').is(':checked')){
            document.getElementById("error").classList.remove("hidden");
            $("#error").html("Necesita seleccionar Caja General, Cuentas por Pagar o ambas.");
            $('body, html').animate({
                scrollTop: '0px'
            }, 300);
        }else{
            if( $('#cj').is(':checked') && $('#cjin').val()!=0){
                $("#save").click();
            }else{
                document.getElementById("error").classList.remove("hidden");
               $("#error").html("Selecciono una cuenta y su saldo esta en cero");
               $('body, html').animate({
                    scrollTop: '0px'
                }, 300);
            }

            if( $('#cp').is(':checked') && $('#cpin').val()!=0){
                $("#save").click();
            }else{
                document.getElementById("error").classList.remove("hidden");
                $("#error").html("Selecciono una cuenta y su saldo esta en cero");
                $('body, html').animate({
                    scrollTop: '0px'
                }, 300);
            }
        }
        
    }
}