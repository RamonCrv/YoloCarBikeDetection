
    $(document).ready(function(){
        $("#video").change(function () {
            var ext = this.value.match(/\.(.+)$/)[1];
            var size =  Math.round(parseInt(this.files[0].size)/1024);

            if(ext !== 'avi'){
                alert("This is not an allowed file type. Use '.avi' video extension");
                this.value = '';
            }else{
                if(size > 51200){
                    alert('This video reached the maximum size. 50MB maximum size');
                    this.value = '';
                }
            }                  
        });    
    });
