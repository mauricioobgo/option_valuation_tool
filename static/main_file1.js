$(document).ready(function(){
    $.ajax({
        url:"/process",
        type:'GET',
        success: function(response){
                console.log(response);
        }
    });

 /*   $('form').on('submit',function(event){
        var SendInfo ={} ;
        $.ajax({
            url: '/process',
            type: "POST",
            data: JSON.stringify(data),
            processData: false,
            contentType: "application/json; charset=UTF-8",
            complete: callback
        });

        event.preventDefault();

*/

    });
