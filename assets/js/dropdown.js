
  function deletepost(pst_id){
    var answer = window.confirm("Are you Sure want to Delete this Post?");
    var id=parseInt(pst_id)
    if(answer)
    {
      console.log(id);
      window.location = '/deletepost/' +id;
    }
    else{
      console.log("No");
    }
  }