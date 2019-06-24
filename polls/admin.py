from django.contrib import admin
from .models import Poll, Choices,Vote
# Register your models here.
admin.site.register(Poll) # makes the Classes i add to the models.py and the info i append from Shell
                          # appears on the Admin panel

admin.site.register(Choices)
admin.site.register(Vote)
