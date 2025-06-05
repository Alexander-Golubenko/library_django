from django.contrib.auth import aget_user
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    profile = models.URLField(null=True, blank=True, verbose_name="Profile URL")
    is_deleted = models.BooleanField(default=False, verbose_name="Is Deleted",
                                     help_text="When the author is deleted is set False")
    rating = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        null=True,
        blank=True,
        verbose_name="Rating in AWS", )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

genre_choice=[
        ('Fiction', 'Fiction'),
 ('Non-Fiction', 'Non-Fiction'),
 ('Science Fiction', 'Science Fiction'),
 ('Fantasy', 'Fantasy'),
 ('Mystery', 'Mystery'),
 ('Biography', 'Biography'),
]


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name="Book Title", blank=False)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, verbose_name="Author", null=True)
    publication_date = models.DateField(null=True, blank=False, verbose_name="Publication Date")
    description = models.TextField(null=True, blank=True, verbose_name="Summary")
    Genre = models.CharField(max_length=100, null=True, blank=True, verbose_name="Genre", choices=genre_choice)
    amount_pages = models.PositiveIntegerField(null=True, blank=True, verbose_name="Amount of Pages",
                                               validators=[MaxValueValidator(10000)])
    publisher = models.ForeignKey("Member", on_delete=models.SET_NULL, verbose_name="Publisher", null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, verbose_name="Category", null=True, related_name='books')
    libraries = models.ManyToManyField("Library", related_name='books', verbose_name="Library")

    @property
    def rating(self):
        if self.reviews.all().count() == 0:
            return 0

        return round(self.reviews.all().aggregate(models.Avg('rating'))['rating__avg'], 2)

    def __str__(self):
        return f'{self.title}'


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Category Title", unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = "Categories"


class Library(models.Model):
    title = models.CharField(max_length=100, verbose_name="Library Title", blank=False)
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name="Location")
    website = models.URLField(null=True, blank=True, verbose_name="Website")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = "Libraries"

gender_choices = [
    ('M', 'Male'),
    ('F', 'Female'), ]

role_choices = [
    ('A', 'Administrator'),
    ('R', 'Reader'),
    ('E', 'Employee'),
]

class Member(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    email = models.EmailField(null=False, blank=False, verbose_name="Email", unique=True)
    gender = models.CharField(max_length=20, verbose_name="Gender", choices=gender_choices)
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    age = models.PositiveIntegerField(verbose_name="Age", editable=False)
    role = models.CharField(max_length=30, verbose_name="Role", choices=role_choices)
    active = models.BooleanField(default=True, verbose_name="Is_active")
    libraries = models.ManyToManyField("Library", related_name='members', verbose_name="Library")

    def save(self, *args, **kwargs):
        ages = timezone.now().year - self.date_of_birth.year
        if 6 <= ages < 120:
            self.age = ages
            super().save(*args, **kwargs)
        else:
            raise ValidationError("Age must be between 6 and 120")

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="Post Title", unique_for_date='date_of_created')
    text = models.TextField(verbose_name="Post Text")
    author = models.ForeignKey(Member, on_delete=models.DO_NOTHING, verbose_name="Author")
    is_moderated = models.BooleanField(default=False, verbose_name="Is Moderated")
    library = models.ForeignKey(Library, on_delete=models.CASCADE, verbose_name="Library", null=True)
    date_of_created = models.DateField(verbose_name="Date of Created")
    date_of_updated = models.DateField(verbose_name="Date of Updated", auto_now=True)

    def __str__(self):
        return f'{self.title}'


class Borrow(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="Member", related_name='borrows')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Book", related_name='borrows')
    library = models.ForeignKey(Library, on_delete=models.CASCADE, verbose_name="Library", related_name='borrows')
    borrow_date = models.DateField(verbose_name="Borrow Date", auto_now=True)
    return_date = models.DateField(verbose_name="Return Date")
    is_returned = models.BooleanField(default=False, verbose_name="Is Returned")

    def __str__(self):
        return f'{self.member.first_name} {self.member.last_name}: {self.book}'

    def check_return(self):
        if self.return_date < timezone.now().date() and not self.is_returned:
            return True
        else:
            return False


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Book", related_name='reviews')
    reviewer = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="Reviewer", related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Review Rating")
    review_text = models.TextField(verbose_name="Review Text")

    def __str__(self):
        return f'{self.book.title}'


class AuthorDetail(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE, verbose_name="Author", related_name='authors')
    biography = models.TextField(verbose_name="Biography")
    date_of_birth = models.DateField(verbose_name="Date of Birth", null=True)
    gender = models.CharField(max_length=20, verbose_name="Gender", choices=gender_choices)

    def __str__(self):
        return f'{self.author.first_name} {self.author.last_name}'


class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name="Event Title")
    description = models.TextField(verbose_name="Event Description")
    timestamp = models.DateField(verbose_name="Event Date")
    library = models.ForeignKey(Library, on_delete=models.CASCADE, verbose_name="Library", related_name='events')
    books = models.ManyToManyField(Book, verbose_name="Books", related_name='events')

    def __str__(self):
        return f'{self.title} - {self.description}'


class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Event", related_name='participants')
    member = models.ManyToManyField(Member, verbose_name="Member", related_name='participants')
    registration_date = models.DateField(verbose_name="Registration Date", default=timezone.now)

    def __str__(self):
        return f'{self.event.title}'