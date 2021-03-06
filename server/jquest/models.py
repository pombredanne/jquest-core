from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField
    
class Instance(models.Model):
    name = models.CharField(max_length=135, help_text='Name of the Instance. Ex: "Syrian Quest"')
    host = models.CharField(max_length=135, help_text='Domain where the instance is accessible. Ex: "syrianquest.com"')
    slug = models.CharField(max_length=135, blank=True, help_text='Simplified version of the name. Ex: "syrianquest"')
    
    def __unicode__(self):
        return self.name

class Mission(models.Model):
    instance = models.ForeignKey(Instance, null=True, db_column='instance', blank=True)
    name = models.CharField(max_length=135, blank=True)  
    description = models.TextField(blank=True)
    image = models.ImageField('Image', upload_to='images/', blank=True)  
    package = models.CharField(max_length=35, blank=True, help_text='Name of the jquest-mission package to load for this mission.')  

    def __unicode__(self):
        return str(self.instance) + ": " + self.name

class MissionRelationship(models.Model):
    mission = models.ForeignKey(Mission, null=True, db_column='mission', blank=True, related_name='+')
    parent = models.ForeignKey(Mission, null=True, db_column='parent', blank=True, related_name='+')


class Post(models.Model):
    title      = models.CharField(max_length=255, blank=True)
    excerpt    = models.CharField(max_length=1536, blank=True)
    content    = models.TextField(blank=True)  
    slug       = models.SlugField(max_length=100)
    created_at = models.DateTimeField(null=True, auto_now_add=True, db_column='created_at', blank=True)
    upadted_at = models.DateTimeField(null=True, auto_now=True, db_column='updated_at', blank=True)

    def __unicode__(self):
        return self.title
  
class UserOauth(models.Model):
    consumer = models.CharField(max_length=165, blank=True)
    consumer_user_id = models.CharField(max_length=165, blank=True)
    oauth_access_token = models.CharField(max_length=765, db_column='oauth_access_token', blank=True)
    oauth_access_token_secret = models.CharField(max_length=765, db_column='oauth_access_token_secret', blank=True)
    user = models.ForeignKey(User, null=True, db_column='user', blank=True)

    def __unicode__(self):
        return str(self.user) + " using " + self.consumer

class UserToken(models.Model):
    user = models.ForeignKey(User, null=True, db_column='user', blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True, db_column='created_at', blank=True) 
    token = models.CharField(max_length=128, blank=True)

    def __unicode__(self):
        return str(self.user)    

class UserProgression(models.Model):
    PROGRESSION_STATES = (
        (u'g', u"game"),
        (u'f', u"failed"),
        (u's', u"succeed")
    )
    mission = models.ForeignKey(Mission, null=True, db_column='mission', blank=True)
    user = models.ForeignKey(User, null=True, db_column='user', blank=True)
    points = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=2, blank=True, choices=PROGRESSION_STATES)   

    def __unicode__(self):
        return str(self.user) + " on " + str(self.mission)


class EntityFamily(models.Model):
    name = models.CharField(max_length=128, blank=True, help_text='Name of the family type and its provider')
    schema_url = models.CharField(max_length=512, blank=True, help_text='URL that describes the schema of the entity')

    class Meta:
        verbose_name_plural = "Entity families"

    def __unicode__(self):
        return str(self.name)

class Entity(models.Model):
    body = JSONField()
    solution = models.CharField(max_length=50, help_text="Optional solution for trusted sources", null=True, blank=True)
    family =  models.ForeignKey(EntityFamily, null=False)    
    fid = models.CharField(max_length=50, help_text="Unique ID of the field in its family")
    created_at = models.DateTimeField(null=True, auto_now_add=True, db_column='created_at', blank=True)
    upadted_at = models.DateTimeField(null=True, auto_now=True, db_column='updated_at', blank=True)
    
    class Meta:
        verbose_name_plural = "entities"   
        unique_together = ('family', 'fid') 

    def __unicode__(self):
        if not self.solution:
            return str(self.id) + "  (" + str(self.family) + ')'
        else:
            return str(self.id) + "  (" + str(self.family) + '): ' + self.solution

class EntityEval(models.Model):
    entity =  models.ForeignKey(Entity, null=False)
    user =  models.ForeignKey(User, null=False)
    value = models.CharField(max_length=512, blank=True)    
    created_at = models.DateTimeField(null=True, auto_now_add=True, db_column='created_at', blank=True)
    upadted_at = models.DateTimeField(null=True, auto_now=True, db_column='updated_at', blank=True)
        
    class Meta:
        unique_together = ('entity', 'user')

    def __unicode__(self):
        return str(self.user) + " evaluted entity " + str(self.entity)
