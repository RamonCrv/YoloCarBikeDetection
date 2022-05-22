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

        $.blockUI({ message: "<h1>Analyzing...<br/>don't reload a page</h1>"});

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
                    video_source.type = 'video/avi';
                    video_source.src = response.url_video;
                    //video_source.src = "blob:/Users/victoreduardo/projects/victor/hera/inputs/videos/video_violence_woman.avi";
                    $('#video_player')[0].load();
                
                    $('.analyze').slideUp(1000);
                    $('.result').slideDown(1000);
                    $('.duration').append('Video Duration: '+response.duration);

                    if (type_det !== 'gender') {
                        if(response.has_violence){
                            $('.has_violence').append("Violence was detected!");
                        } else{
                            $('.has_violence').append("Violence was not detected!");
                        }
                    }
                    
                    if (type_det !== 'violence') {
                        if(response.has_woman){
                            $('.has_woman').append("Women were detected!");
                        }else {
                            $('.has_woman').append("Women were not detected!");                  
                        }
                    }

                    $.each(response.url_frames, function(index, item) {
                        $("#timeline_scene").append("<div class='col-lg-3 text-center'><img src='"+item+"' />"+response.violence_seconds[index]+"s</div>");
                    });
                    
                }
                
            },
            processData: false,
            cache: false,
            contentType: false
          });
    });    
});
    
