from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import RegexValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

class Users(AbstractUser):
    first_name = None
    last_name = None
    name = models.CharField(max_length=50, blank=False,null=False)
    email = models.EmailField(unique=True,null=False,blank=False)
    mobile = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex='[6-9]{1}[0-9]{9}',
                message="enter a valid 10 digit mobile number",
            ),
        ]
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','mobile']
    friend_list = models.ManyToManyField("blog.Users",related_name='friends')
    friend_request_list = models.ManyToManyField("blog.Users",related_name='friend_requests')
    saved_blogs = models.ManyToManyField('blog.Blog',related_name="savedblogs")

    def __str__(self):
        return self.email
    def get_friend_idlist(self):
        lst = [x.id for x in self.friend_list.all()]
        lst.append(self.id)
        return lst
    def user_isfriend(self,userId):
        return True if self.friend_list.filter(id=userId).exists() else False
    def send_friend_rq(self,user_id):
        usr = Users.objects.get(id=user_id)
        if not self.user_isfriend(user_id):
            usr.friend_request_list.add(self)
    def cancel_friend_rq(self,user_id):
        usr = Users.objects.get(id=user_id)

        usr.friend_request_list.remove(self)
    def reject_friend_rq(self,userId):
        usr = Users.objects.get(id=userId)
        self.friend_request_list.remove(usr)
    def accept_friend_rq(self,userId):
        usr = Users.objects.get(id=userId)
        if self.friend_request_list.filter(id=userId):
            self.friend_request_list.remove(usr)
            self.friend_list.add(usr)
            usr.friend_list.add(self)
    def remove_friend(self,usrId):
        usr = Users.objects.get(id=usrId)
        if self.friend_list.filter(id=usrId).exists():
            self.friend_list.remove(usr)
            usr.friend_list.remove(self)
    @property
    def get_friend_list(self):
        return [{"id":x.id,"name":x.name} for x in self.friend_list.all()]
    @property
    def get_friend_requests(self):
        return {
            "sent":[{"id":x.id,"name":x.name} for x in self.friend_requests.all()],
            "received":[{"id":x.id,"name":x.name} for x in self.friend_request_list.all()],
        }
    def find_friends(self):
        u = Users.objects.filter().exclude(id__in=[x.id for x in self.friend_list.all()]).exclude(id__in=[x.id for x in self.friend_request_list.all()]).exclude(id__in=[x.id for x in self.friend_requests.all().exclude(id=self.id)])
        return [{"id": x.id, "name": x.name} for x in u]


        

class Blog(models.Model):
    user = models.ForeignKey("blog.Users", on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='blog/')
    text = models.TextField()
    like = models.ManyToManyField("blog.Users",related_name="bloglike")
    love = models.ManyToManyField("blog.Users",related_name="bloglove")
    dislike = models.ManyToManyField("blog.Users",related_name="blogdislike")
    # reactions = GenericRelation('blog.Reactions')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_datadict(self,user):
        blogdata = {}
        blogdata["id"] = self.id
        blogdata["user_id"] = self.user.id
        blogdata["user_name"] = self.user.name
        blogdata["auth"] = True if self.user == user else False
        # print(self.picture.url)
        blogdata["picture"] = self.picture.url if self.picture else None
        blogdata["text"]=self.text
        blogdata["created_at"] = self.created_at.__str__()[0:19]
        blogdata["is_saved"] = user.saved_blogs.filter(id=self.id).exists()
        blogdata["is_liked"] = user.bloglike.filter(id=self.id).exists()
        blogdata["is_disliked"] = user.blogdislike.filter(id=self.id).exists()
        blogdata["is_loved"] = user.bloglove.filter(id=self.id).exists()
        blogdata["likes"] = self.like.count()
        blogdata["loves"] = self.love.count()
        blogdata["dislikes"] = self.dislike.count()
        blogdata["saves"] = self.savedblogs.count()
        comments = []
        for c in self.comments_set.all():
            comment = {}
            comment["id"] = c.id
            comment["user_id"] = c.user.id
            comment["user_name"] = c.user.name
            comment["comment"] = c.comment
            comment["auth"] = True if blogdata["auth"] == True else (True if c.user == user else False)
            comment["created_at"] = c.created_at.__str__()[0:19]
            comment["is_liked"] = user.commentlike.filter(id=self.id).exists()
            comment["is_disliked"] = user.commentdislike.filter(id=self.id).exists()
            comment["is_loved"] = user.commentlove.filter(id=self.id).exists()
            comment["likes"] = c.like.count()
            comment["loves"] = c.love.count()
            comment["dislikes"] = c.dislike.count()
            replies = []
            for r in c.reply_set.all():
                reply = {}
                reply["id"] = r.id
                reply["user_id"] = r.user.id
                reply["user_name"] = r.user.name
                reply["replytext"] = r.text
                reply["auth"] = True if comment["auth"] == True else (True if r.user == user else False)
                reply["created_at"] = r.created_at.__str__()[0:19]
                reply["is_liked"] = user.replylike.filter(id=self.id).exists()
                reply["is_disliked"] = user.replydislike.filter(id=self.id).exists()
                reply["is_loved"] = user.replylove.filter(id=self.id).exists()
                reply["likes"] = r.like.count()
                reply["loves"] = r.love.count()
                reply["dislikes"] = r.dislike.count()
                replies.append(reply)
                del reply
            comments.append(comment)
            del comments
        blogdata["comments"] = comments
        return blogdata


    

class Comments(models.Model):
    user = models.OneToOneField("blog.Users", on_delete=models.CASCADE)
    blog = models.ForeignKey("blog.Blog", on_delete=models.CASCADE)
    comment = models.TextField(blank=False,null=False)
    # reactions = GenericRelation('blog.Reactions')
    like = models.ManyToManyField("blog.Users",related_name="commentlike")
    love = models.ManyToManyField("blog.Users",related_name="commentlove")
    dislike = models.ManyToManyField(r"blog.Users",related_name="commentdislike")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Reply(models.Model):
    user = models.OneToOneField("blog.Users", on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments,on_delete=models.CASCADE)
    text = models.TextField(blank=False,null=False)
    like = models.ManyToManyField("blog.Users",related_name="replylike")
    love = models.ManyToManyField("blog.Users",related_name="replylove")
    dislike = models.ManyToManyField("blog.Users",related_name="replydislike")
    # reactions = GenericRelation('blog.Reactions')

    created_at = models.DateTimeField(auto_now_add=True)


#
# class Reactions(models.Model):
#     reaction_choices = [
#         ("like","like"),
#         ("unlike","unlike"),
#         ("love","love"),
#     ]
#     reaction = models.CharField(max_length=10,blank=False,null=False)
#     user = models.ForeignKey("blog.Users",on_delete=models.CASCADE)
#
#     content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,blank=True,null=True)
#     object_id = models.PositiveIntegerField(blank=True,null=True)
#     # content_object = GenericForeignKey('content_type','object_id')
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)