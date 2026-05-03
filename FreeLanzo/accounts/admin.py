from django.contrib import admin
from .models import (
    Category,
    Skill,
    PortfolioProject,
    PortfolioProjectImage,
    Project,
)

class PortfolioProjectImageInline(admin.TabularInline):
    model = PortfolioProjectImage
    extra = 4

class PortfolioProjectAdmin(admin.ModelAdmin):
    inlines = [PortfolioProjectImageInline]

admin.site.register(Category)
admin.site.register(Skill)
admin.site.register(PortfolioProject, PortfolioProjectAdmin)
admin.site.register(Project)