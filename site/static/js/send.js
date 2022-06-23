$(document).ready(function(){    

    $('form#analyze').submit(function(e){
        e.preventDefault();

        var formData = new FormData();
        var video = $('#video').prop('files')[0];
        var video_source = $('#video_player').find('source')[0];
        var src_video = URL.createObjectURL(video);
        var type_det = $("input[name='type_detection']:checked").val();
        
        
        formData.append('type_detection', type_det);
        formData.append('video', video);


        $.blockUI({ message: "<h3 style='padding:4px 1px'>Analisando...<br/>Não recarregue a página.</h3>"});

          $.ajax({
            url: 'http://127.0.0.1:8000/analyze/',
            data: formData,
            type: 'post',
            headers: {
                'Access-Control-Allow-Origin': '*',
                //'Access-Control-Allow-Headers': "Origin, X-Requested-With, Content-Type, Accept",
                
                'Accept': 'application/json',
                'Access-Control-Allow-Methods': 'POST'
            },
            success: function(response) {              

                $.unblockUI(); //Desbloquear UI            
                
                if(response.duration == undefined){
                    alert('the video does not have the minimum requirements for analysis');
                }else{
                    video_source.type = 'video/webm';
                    video_source.src = response.url_video;
                    //video_source.src = "blob:/Users/victoreduardo/projects/victor/hera/inputs/videos/video_violence_woman.avi";
                    $('#video_player')[0].load();
                
                    $('.analyze').slideUp(1000);
                    $('.result').slideDown(1000);
                    $('.duration').append('Duração do video : '+response.duration+'s');

                    if (type_det == 'belt') {
                        if(response.driver_detected){
                            if(response.unbelted_driver){
                                $('.unbelted_driver').append("Motorista <span style='color:red; font-weight:bold'>Sem Cinto</span> foi detectado no video!"); 
                            }else{                                
                                
                                $('.unbelted_driver').append("Nenhum Motorista <span style='color:red; font-weight:bold'>Sem Cinto</span> foi detectado no vídeo!");
                            }
                        } else{
                            $('.unbelted_driver').append("Nenhum Motorista foi detectado no Video!");
                        }

                        if(response.passenger_detected){
                            if(response.unbelted_passenger){                                                             
                                $('.unbelted_passenger').append("Passageiro <span style='color:red; font-weight:bold'>Sem Cinto</span> foi detectado no video!");
                            }else{ 
                                $('.unbelted_passenger').append("Nenhum Passageiro <span style='color:red; font-weight:bold'>Sem Cinto</span> foi detectado no video!");  
                            }
                        } else{
                            $('.unbelted_passenger').append("Nenhum Passageiro foi detectado no Video!");
                        }

                    }
                    
                    $.each(response.unbelted_seconds, function(index, item) {

                        if(response.unbelted_name[index] === 'driver'){
                            var type = "Motorista";
                        }else{
                            var type = "Passageiro";
                        }

                        // $("#timeline_scene").append("<div class='col-lg-12'><img src='"+response.url_frames[index]+"' /> Tempo: "+response.unbelted_seconds[index]+"s [ "+type+" ] Sem Cinto</div>");
                   
                        $("#timeline_scene").append("<div style='border:1px solid #ddd; border-radius:5px; padding:5px; margin-bottom:2px;' class='col-lg-12'><img width='50px' height='50px' src='"+response.url_frames[index]+"'> Tempo: "+response.unbelted_seconds[index]+"s [ "+type+" ] Sem Cinto</div>");
                    });
                    
                }
                
            },
            processData: false,
            cache: false,
            contentType: false
          });
    });    
});
    
