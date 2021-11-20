from django.contrib import admin
from podcasts import models
import reprlib
# Register your models here.

@admin.register(models.Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display =('title', 'podcast_name', 'short_description', 'pub_date')

    #@admin.display(ordering= 'short_description', description= 'Description')
    def short_description(self, obj):
        """Form a short representation of the description"""

        return reprlib.repr(obj.description)[1:-1]

