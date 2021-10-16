function react(fetched_id){
    $.ajax({
        method: "POST",
        url: "/react",
        data: { 
          pid:fetched_id,
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        }
        })
        .done(function( msg ) {
            console.log(msg.likecount);
           
            document.getElementById('1'+fetched_id).innerHTML=msg.likecount;
            if(msg.lk == 1)
            {
                let imgid=7+fetched_id;
                document.getElementById(imgid).style.color="red";
            }
            else{
                let imgid=7+fetched_id;
                document.getElementById(imgid).style.color="black";
            }
            
            console.log(1+fetched_id)
            
        });
}


function commentreact(fetched_id){
    $.ajax({
        method: "POST",
        url: "/commentreact",
        data: { 
          pid:fetched_id,
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        }
        })
        .done(function( msg ) {
            console.log(msg.likecount);
           
            document.getElementById('1'+fetched_id).innerHTML=msg.likecount;
            if(msg.lk == 1)
            {
                let imgid=7+fetched_id;
                document.getElementById(imgid).style.color="red";
            }
            else{
                let imgid=7+fetched_id;
                document.getElementById(imgid).style.color="black";
            }
            
            console.log(1+fetched_id)
            
        });
}


function postcomment(){
    $.ajax({
        method: "POST",
        url: "/mycomment",
        data: { 
            myid:$('input[name=cmtpstid]').val(),
            comment:$('input[name=mycmt]').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        }
        })
        .done(function( msg ) {
            console.log("hello");
        });
}

function srch(){
    let term=document.getElementById('search').value;
    window.location = '/search/' +term;
}