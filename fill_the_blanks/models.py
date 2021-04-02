import uuid

from django.db import models

from django.contrib.postgres.fields import ArrayField

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

from django.template.defaultfilters import slugify
from django.utils.html import strip_tags

from django.utils import timezone

from .add_input_tags import add_leading_spaces, add_input


class CustomUserManager(BaseUserManager):
    '''
    Customer user model which uses email as the unique identifier instead of username.
    '''
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email  = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField()

    def get_absolute_url(self):
        return f'{self.pk}/{self.slug}/profile/'

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.user))
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

class OriginalWorksheet(models.Model):
    '''
    This is the text from the worksheet before text inputs are added.
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField()

    name = models.CharField(verbose_name='Worksheet title', default='Your worksheet', max_length=1000)
    worksheet_text = models.TextField()
    original_text = models.TextField(verbose_name='Paste your worksheet here')
    worksheet_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    answers = ArrayField(models.TextField(null=True), null=True)

    correct = ArrayField(models.IntegerField(null=True), null=True)
    incorrect = ArrayField(models.IntegerField(null=True), null=True)

    def transform_text(self, original_text):
        '''
        This method turns "blanks" into inputs for students to write there answers into.
        '''

        with_leading_space = add_leading_spaces(original_text)

        split_worksheet = with_leading_space.split(' ')
        counter_number = 0

        for word in enumerate(split_worksheet):
            if '……' in word[1]:
                counter_number +=1
                new_letters = add_input(
                    word[1],
                    '…',
                    f'<input type="text" id="{counter_number}" name="{counter_number}">',
                    )
                split_worksheet[word[0]] = ''.join(new_letters).replace('.', '')
            elif '__' in word[1]:
                counter_number +=1
                new_letters = add_input(
                    word[1],
                    '_',
                    f'<input type="text" id="{counter_number}" name="{counter_number}">',
                    )
                split_worksheet[word[0]] = ''.join(new_letters)
            elif '....' in word[1]:
                counter_number +=1
                new_letters = add_input(
                    word[1],
                    '.',
                    f'<input type="text" id="{counter_number}" name="{counter_number}">',
                    )
                split_worksheet[word[0]] = ''.join(new_letters)
            elif '….' in word[1]:
                counter_number +=1
                new_letters = add_input(
                    word[1],
                    '…',
                    f'<input type="text" id="{counter_number}" name="{counter_number}">',
                    )
                split_worksheet[word[0]] = ''.join(new_letters).replace('.', '')
            elif '.…' in word[1]:
                counter_number +=1
                new_letters = add_input(
                    word[1],
                    '…',
                    f'<input type="text" id="{counter_number}" name="{counter_number}">',
                    )
                split_worksheet[word[0]] = ''.join(new_letters).replace('.', '')

        new_worksheet = ' '.join(split_worksheet)
        return new_worksheet


    def save(self, *args, **kwargs):
        '''
        This save method creates a slug strips tags and adds inputs to text in that order.
        '''        
        self.slug = slugify(self.name)
        self.name = strip_tags(self.name)
        self.original_text = strip_tags(self.original_text)
        self.worksheet_text = self.transform_text(self.original_text)

        if self.answers:
            if self.correct == None:
                # this initilises a list of tuples with the answer being [0] and the amount of correct answers being [1]
                self.correct = [0 for i in range(len(self.answers))]
                self.incorrect = [0 for i in range(len(self.answers))]
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return f'/{self.pk}/{self.slug}/'

    def __str__(self):
        return self.name


class StudentWorksheet(models.Model):
    '''
    A place for students to store their answers.
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    worksheet = models.ForeignKey(OriginalWorksheet, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    mark = models.IntegerField(default=0)

    answers = ArrayField(models.TextField(null=True))

    upload_time = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return f'{self.pk}/'
    
    def __str__(self):
        return f'{self.name} {self.upload_time}'

    def save(self, *args, **kwargs):
        og_worksheet = self.worksheet
        teacher_answers = og_worksheet.answers
        if teacher_answers:
            corrections = og_worksheet.correct
            incorrections = og_worksheet.incorrect

            for answer in enumerate(teacher_answers):
                if self.answers[answer[0]] == answer[1]:
                    self.mark += 1
                    self.answers[answer[0]] = f'<span style="font-weight:bold; color:green">{self.answers[answer[0]]}</span>'
                    corrections[answer[0]] +=1

                else:
                    self.answers[answer[0]] = f'<span style="font-weight:bold; color:red">{self.answers[answer[0]]}</span>'
                    incorrections[answer[0]] +=1

        self.worksheet.save()
        
        super().save(*args, **kwargs)
