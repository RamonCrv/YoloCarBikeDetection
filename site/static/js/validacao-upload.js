
    $(document).ready(function(){
        $("#video").change(function () {
            var ext = this.value.match(/\.(.+)$/)[1];
            var size =  Math.round(parseInt(this.files[0].size)/1024);

            if(ext !== 'avi' && ext !== 'mp4' && ext !== 'MOV'){
                alert("This is not an allowed file type. Use '.avi' or '.mp4' or '.MOV'  video extension");
                this.value = '';
            }else{
                if(size > 102400){
                    alert('This video reached the maximum size. 100MB maximum size');
                    this.value = '';
                }
            }                  
        });    
    });
