import sys
import inspect
import re
import os.path
from django.core.management.base import AppCommand, CommandError
from django.conf import settings
#import ast

class Command(AppCommand):
    args = '<app>'
    help = 'creates boilerplate django files if missing from a give app.'
    tab = "    "

    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError('Need to pass App names')

        app_name = args[0]
        root_path = settings.PROJECT_PATH
        app_path = os.path.join(root_path, app_name)
        self.add_url(app_name, app_path)
        self.add_admin(app_name, app_path)
        self.add_forms(app_name, app_path)

    def add_url(self, app_name, app_path):
        file_name = 'urls.py'
        comment = "#"
        lines = []

        # SHOULD LOOK AT CLASS BASED VIEWS IN views.py FOR URL GENERATION

        lines.append("from django.conf.urls.defaults import patterns, url, include")
        lines.append("from %s import views\n" % app_name)
        lines.append("urlpatterns = patterns(\"\",")
        lines.append("%s%surl(regex=r'^$', view=views.SomeView.as_view(), name='%s_view'),\n)" % (comment, self.tab, app_name) )
        lines.append("\n\n")

        if self.add_file(app_name, app_path, file_name, '\n'.join(lines)):
            print "Added URLs: %s" % app_name

    def add_admin(self, app_name, app_path):

        file_name = 'admin.py'

        lines = []
        comment, models = self.get_models(app_name, app_path)

        lines.append("from django.contrib import admin")
        lines.append("%sfrom %s.models import %s\n" % (comment, app_name, ", ".join(models)))

        for model in models:
            lines.append("%sadmin.site.register(%s)\n" % (comment, model))
        
        lines.append("\n\n")

        if self.add_file(app_name, app_path, file_name, '\n'.join(lines)):
            print "Added admin.py: %s" % app_name

    def add_forms(self, app_name, app_path):

        file_name = 'forms.py'

        #comment = ""
        lines = []
        comment, models = self.get_models(app_name, app_path)

        if models[0] == "ExampleModel":
            comment = "#"

        lines.append("from django import forms")
        lines.append("%sfrom %s.models import %s\n" % (comment, app_name, ", ".join(models)))

        for model in models:
            lines.append("%sclass %sForm(forms.ModelForm):" % (comment, model))
            lines.append(comment)
            lines.append(comment + self.tab + "class Meta:")
            lines.append(comment + (2 * self.tab) + "model = %s\n\n" % (model))
        
        lines.append("\n\n")

        if self.add_file(app_name, app_path, file_name, '\n'.join(lines)):
            print "Added forms.py: %s" % app_name

    def add_file(self, app_name, app_path, file_name, lines):
        file_path = os.path.join(app_path, file_name)

        if os.path.isfile(file_path):
            print "Path exists, skipping: %s" % file_path
            return False

        try:
            FILE = open(file_path, "w")
            FILE.write( lines )
            FILE.close()
        except IOError as e:
            print( "IO Error reading %s\n\t%s" % (file_path, e) )
            return

        return True

    def get_models(self, app_name, app_path):

        classes = inspect.getmembers(sys.modules["%s.models" % app_name], inspect.isclass)  # COULD ALSO ADD CHECK TO SEE IF IT IS A DJANO MODEL CLASS
        models = []
        comment = ""

        for cl in classes:
            if cl[1].__module__ == "%s.models" % app_name:
                models.append(cl[0])

        if not models:
            models = ['ExampleModel']
            comment = "#"

        return comment, models


