$(document).ready(function () {
    var option_type_selected = "";
    var values_selected=[];
    var concatenateTemp="";
    $.ajax({
        url: "/process",
        type: 'GET',
        success: function (response) {
            var counter = 1;
            for (i in response.option_type) {
                $('#option_type').append(`<option id_option_selected="${counter}"> 
                    ${response.option_type[i]} </option>`);
                counter += 1;
            }
            console.log(response);
        }
    });
/* revisar debido a que no esta seleccionando los multiples datos en el formulario*/ 
// first initialize the Chosen select
        $( 'select#option_type').on( 'change', function() {
            var concatenate_no_log=[];
            $.each($("option:selected",this), function(){            
                concatenate_no_log.push($(this).attr('id_option_selected'));
            });
            //console.log();
            values_selected=$(this).val();
            option_type_selected=concatenate_no_log.join(",");
            console.log(option_type_selected);
            console.log(values_selected);
        } );
        
     $('#reset_form').click(function(event){
         location.reload();
     });
    $('#make_calulation').click( function (event) {
        if ($('#option_node_calc').val() !== "" && option_type_selected!="") {
            var SendInfo = [option_type_selected, $('#option_spot').val(), 
            $('#option_strike').val(),
             $('#option_rate').val(), 
             $('#option_sd_risk').val(), 
             $('#option_time_years').val(), 
             360, 
             $('#option_node_calc').val()];
            console.log(SendInfo);
            $.ajax({
                url: '/option_calculation',
                type: "POST",
                data: JSON.stringify(SendInfo),
                processData: false,
                contentType: "application/json; charset=UTF-8",
                success: function (data_reponse) { 
                    var dataCumm=[]
                    for ( i in data_reponse.finalValue){
                        dataCumm.push(data_reponse.finalValue[i]);
                    }
                    $('#option_value_result').attr("style","visibility: visible;");
                    counter=0;
                    console.log(data_reponse);
                    ctx=$("#myChart");
                    var myChart=new Chart(ctx,{
                        type:"bar",
                        data:{
                            labels:values_selected,
                            datasets:[{label:'Precios Opciones',
                                data:dataCumm}] 
                        },
                        options:{
                            scales:{
                                yAxes:[{
                                        ticks:{
                                            beginAtZero:true
                                        }
                                }]
                            }
                        }
                    });
                    for ( i in data_reponse.finalValue){
                        console.log(i);
                        console.log(values_selected[counter]);
                            $('#results_adding').append(`<tr><td>${values_selected[counter]}
                            </td><td> ${data_reponse.finalValue[i]}</td> </tr>`);
                            counter += 1;

                    }
                    
                     },
                failure: function (errMsg) {
                    alert(errMsg);
                }
            });
        } else {
            alert("Hola Haga algo y ponga los valores");
            
        }
        event.preventDefault();
    });


});
