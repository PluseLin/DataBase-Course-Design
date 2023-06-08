var script=document.createElement("script");  
script.type="text/javascript";  
script.src="jquery.js";  

$(document).ready(function(){
    $(".btn").click(function(){
        var button_id=$(this).attr("id");
        var data={
            "action":button_id,
        };
        $.ajax({
            type:"POST",
            cache:false,
            data:JSON.stringify(data),
            contentType:'application/json;charset=UTF-8',
            dataType:'json',
            async:true,
            success:function(ret){
                window.alert(ret.message);
            },
            error:function(xhr,type){

            }
        })
    })
});