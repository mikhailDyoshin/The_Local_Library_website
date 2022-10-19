from django.contrib import admin
from .models import Genre, Language, Book, BookInstance, Author


admin.site.register(Genre)
admin.site.register(Language)
# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Author)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'date_of_birth',
        'date_of_death',
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'display_genre',
    )


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = (
        'book',
        'status',
        'due_back',
        'imprint',
    )

    list_filter = (
        'status',
        'due_back',
    )