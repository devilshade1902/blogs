from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Post
from django.contrib.auth.models import User


# Custom filter to show "By Author" and Author objects
class AuthorFilter(admin.SimpleListFilter):
    title = _('Author')  # Title displayed in the filter sidebar
    parameter_name = 'author'  # Query parameter for the filter

    def lookups(self, request, model_admin):
        """Define the filter options."""
        authors = User.objects.all()
        return [(author.id, author.username) for author in authors]

    def queryset(self, request, queryset):
        """Filter the queryset based on the selected option."""
        if self.value():  # If a specific author is selected
            return queryset.filter(author_id=self.value())
        return queryset  # Default to show all posts


# Customize the admin panel for Post
class PostAdmin(admin.ModelAdmin):
    # Specify the fields to display as columns in the table format
    list_display = ('title', 'content', 'author', 'updated_at', 'created_at')

    # Add the custom filter on the right-hand side
    list_filter = (AuthorFilter,)

    # Optionally, display links for a specific field (defaults to the first field in list_display)
    list_display_links = ('title',)


admin.site.register(Post, PostAdmin)

# Customizing the admin site headers
admin.site.site_header = "Blogs Admin Dashboard"
admin.site.site_title = "Blogs Admin Portal"
admin.site.index_title = "Welcome to the Blogs Admin Dashboard"
