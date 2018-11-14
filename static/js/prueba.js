$(document).ready(function(){
var $myForm = $('.formulario');
$myForm.submit(function (event) {
    event.preventDefault();
    var $formData = $myForm.serialize();
    var $thisURL = $myForm.attr('data-url') || window.location.href;

    $.ajax({
        type: "POST",
        url: $thisURL,
        data: $formData,
        success: handleSuccess,
        error: handleError,
    });
    function handleSuccess(data) {
        alert("Transaccion iniciada con exito. Agregue Cuentas a la transaccion");
        $("#2").attr("readonly", true);
        $("#3").attr("readonly", true);
        $("#1").attr("disabled", true);
        $("#recibedeb").attr("value", data.message);
        $("#recibehab").attr("value", data.message);
        /*$("#ad").seteAttribute('disabled',false);
        $("#ah").removeAttribute('disabled',false);*/


    }
    function handleError(data) {
        console.log(data);
    }

});

});