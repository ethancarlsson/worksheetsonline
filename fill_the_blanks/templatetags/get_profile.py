from django import template
from fill_the_blanks.models import Profile

register = template.Library()

@register.simple_tag
def profile_url(user):
    '''
    gets the URL for the profile page of a user.
    '''
    user_profile = Profile.objects.get(user=user)
    url = f'{user_profile.pk}/{user_profile.slug}/profile/'
    return url