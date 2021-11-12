from home.models import Comment

def comment_delete(id):
    #Fetch the post with the given ID

    pst = Comment.objects.get(id=id)
    pst.delete()
    return 