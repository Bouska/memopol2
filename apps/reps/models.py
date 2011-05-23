from django.db import models

class RepsContainerManager(models.Manager):
    """ Manager for models to which the representative model has a foreign key"""
    def with_counts(self):
        """ Return the models with a count property, with the count of active Reps """
        return self.get_query_set().filter(representative__mep__active=True).annotate(count=models.Count('representative'))

class Party(models.Model):
    name = models.CharField(max_length=255, unique=True)

    objects = RepsContainerManager()

    def __unicode__(self):
        return self.name

    @property
    def meps(self):
        return self.mep_set.filter(active=True)

class Opinion(models.Model):
    title = models.CharField(max_length=1023, unique=True)
    content = models.TextField()
    url = models.URLField()

    def __unicode__(self):
        return self.title

class Representative(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=2, choices=((u'M', u'Male'), (u'F', u'Female')))
    picture = models.CharField(max_length=255, unique=True)
    #picture = models.ImageField(upload_to="")
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=255)
    local_party = models.ManyToManyField(Party, through='PartyRepresentative')
    opinions = models.ManyToManyField(Opinion, through='OpinionREP')

    def __unicode__(self):
        return self.full_name

    class Meta:
        ordering = ['last_name']

class PartyRepresentative(models.Model):
    representative = models.ForeignKey(Representative)
    party = models.ForeignKey(Party)
    role = models.CharField(max_length=255, null=True)
    current = models.BooleanField()
    # well maybe need those one day
    #begin = models.DateField()
    #end = models.DateField()

class Email(models.Model):
    email = models.EmailField()
    representative = models.ForeignKey(Representative)

    def __unicode__(self):
        return self.email

class CV(models.Model):
    title = models.CharField(max_length=1023)
    representative = models.ForeignKey(Representative)

    def __unicode__(self):
        return self.title

class WebSite(models.Model):
    url = models.URLField()
    representative = models.ForeignKey(Representative)

    def __unicode__(self):
        return self.url

class OpinionREP(models.Model):
    representative = models.ForeignKey(Representative)
    opinion = models.ForeignKey(Opinion)
    date = models.DateField()

    def __unicode__(self):
        return u"%s : %s" % (self.opinion, self.mep)
