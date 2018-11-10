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
        success:handleSuccess,
        error: handleError,
    });
    function handleSuccess(data){
        alert("todo vergon");
    }
    function handleError(data){
        console.log(data.message);
    }

});

});