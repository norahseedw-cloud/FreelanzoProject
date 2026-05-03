from django.contrib import admin

# Register your models here.
from .models import PortfolioProject, PortfolioProjectImage

class PortfolioProjectImageInline(admin.TabularInline):
    model = PortfolioProjectImage
    extra = 4

class PortfolioProjectAdmin(admin.ModelAdmin):
    inlines = [PortfolioProjectImageInline]

admin.site.register(PortfolioProject, PortfolioProjectAdmin)