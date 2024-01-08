from django.db import models
from accounts.models import User
import uuid
# Create your models here.



class BaseModel(models.Model):
    uid=models.UUIDField(primary_key=True,default=uuid.uuid4)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    class Meta:
        abstract=True


class Blog(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog')
    title=models.CharField(max_length=500)
    blog_text=models.TextField()
    image=models.ImageField(upload_to='blog_image')
    class Meta:
        ordering=['updated_at']


    def __str__(self):
        return self.title