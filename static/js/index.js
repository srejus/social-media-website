function react(fetched_id){
    console.log('hello');
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

function commentdelete(fetched_id){
    $.ajax({
        method: "POST",
        url: "/commentdelete",
        data: { 
          pid:fetched_id,
         csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        }
        })
        .done(function( msg ) {
            console.log(msg);
            location.reload();
           
            
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
    
    if(term != undefined || term != ""){
        window.location = '/search/' +term;
        
    }
    
    
}

function share(url){
   var curl=window.location.href;
   var domn=location.protocol+'//'+location.host;

    // var s = '/Controller/Action';
    var n = curl.indexOf('?');
    s = curl.substring(0, n != -1 ? n : curl.length);
    document.write(curl);
    var fullurl=domn+url;
      /* Select the text field */
    fullurl;
    // fullurl.setSelectionRange(0, 99999); /* For mobile devices */

    /* Copy the text inside the text field */
    navigator.clipboard.writeText(fullurl);

    /* Alert the copied text */
    alert("Copied to clipboard: " + fullurl);
    location.reload();
}