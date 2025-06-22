from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # for clean URLs like /projects/my-first-app/
    description = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True) # Added this line
    created_at = models.DateTimeField(auto_now_add=True)
    is_premium = models.BooleanField(default=False)

    def teaser(self):
        return self.content[:200] + "..." 

    def __str__(self):
        return self.title

