var script=document.createElement("script");  
script.type="text/javascript";  
script.src="jquery.js";  

$(document).ready(function(){
    $(".btn").click(function(){
        var button_id=$(this).attr("id");
        var data={
            "cid":""
        };
        data.cid=button_id.substr("untagging_".length)
        $.ajax({
            type:"POST",
            cache:false,
            data:JSON.stringify(data),
            contentType:'application/json;charset=UTF-8',
            dataType:'json',
            async:true,
            success:function(ret){
                window.alert(ret.message);
                location.reload();
            },
            error:function(xhr,type){

            }
        })
    })
});