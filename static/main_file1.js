$(document).ready(function(){
        $.ajax({
            url:"/process",
            type:'GET',
            success: function(response){
                var counter=1;
                for( i in response.option_type){
                    $('#option_type').append(`<option id_option_selected="${counter}"> 
                    ${response.option_type[i]} </option>`);
                    counter+=1;
                }
                    console.log(response);
            }
        });
        $('form').on('submit',function(event){
            var SendInfo ={} ;
            $.ajax({
                url: '/process',
                type: "POST",
                data: JSON.stringify(data),
                processData: false,
                contentType: "application/json; charset=UTF-8",
                complete: callback
            });
        });
        event.preventDefault();

});
