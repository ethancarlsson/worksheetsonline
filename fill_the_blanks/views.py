'''
All views that are essential for core functionality of the app.
'''
from django.shortcuts import redirect

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.utils.html import strip_tags


from .models import OriginalWorksheet, Profile, StudentWorksheet
from .add_input_tags import transform_to_answers
from .decorators import allowed_users


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_users(False), name='dispatch')
class ProfileView(DetailView):
    model = Profile
    template_name = 'fill_the_blanks/profile_detail.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        worksheets = OriginalWorksheet.objects.filter(worksheet_owner=self.request.user)
        context.update({'worksheets':worksheets})
        return context

    def post(self, request, *args, **kwargs):
        request_post = request.POST
        if 'delete' in request_post:
            OriginalWorksheet.objects.get(pk=request_post['delete']).delete()
        return redirect(f'https://worksheetsonline.herokuapp.com/{kwargs["pk"]}/{kwargs["slug"]}/profile')

class WriteWorksheet(CreateView):
    model = OriginalWorksheet
    fields = ['name', 'original_text']

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.worksheet_owner = self.request.user
            
        return super().form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_users(True), name='dispatch')
class ReadWorksheet(DetailView):
    '''
    Where the teacher can read a new worksheet after creating it.
    '''
    model = OriginalWorksheet
    template_name = 'fill_the_blanks/originalworksheet_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        worksheet = context.get('originalworksheet')
        student_sheets = StudentWorksheet.objects.filter(worksheet=worksheet)
        teacher_answers = []
        if worksheet.answers:
            teacher_answers = zip(worksheet.answers, worksheet.correct, worksheet.incorrect)

        context.update({'teacher_answers': teacher_answers, 'student_sheets': student_sheets})
        return context


    def post(self, request, *args, **kwargs):
        worksheet = OriginalWorksheet.objects.get(pk=kwargs['pk'])

        # the list comprehension below is the ugliest thing in the world and needs to be refactored at some point
        # it strips tags, and normalises the answers, then puts them in a list.
        # handles both the original answer and the updates
        # should be transformed into a dictionary and saved as an Hstore field later on
        answers = [strip_tags(request.POST[f'{answ}']).strip().lower() for answ in range(1, len(request.POST))]

        worksheet.answers = answers

        worksheet.save()

        return redirect(worksheet.get_absolute_url())

class EditWorksheet(UpdateView):
    template_name_suffix = '_edit'
    model = OriginalWorksheet
    fields = ['name', 'original_text']

    def post(self, request, *args, **kwargs):
        the_pk = kwargs.get('pk')
        worksheet = OriginalWorksheet.objects.get(pk=the_pk)
        worksheet.answers = None
        worksheet.correct = None
        worksheet.save()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)



class StudentWorksheetView(DetailView):
    '''
    Where students can answer .
    '''
    template_name_suffix = '_student'
    model = OriginalWorksheet

    def post(self, request, *args, **kwargs):
        '''
        Creates a new object for the worksheet and each answer on the worksheet.
        '''
        worksheet = OriginalWorksheet.objects.get(pk=kwargs['pk'])
        # the list comprehension below is the ugliest thing in the world and needs to be refactored at some point
        # it strips tags, and normalises the answers, then puts them in a list.
        answers = [strip_tags(request.POST[f'{answ}']).strip().lower() for answ in range(1, len(request.POST)-1)]

        student_workheet = StudentWorksheet.objects.create(
            worksheet=worksheet, name=strip_tags(request.POST['Student Name']), answers=answers
            )

        return redirect(f'https://worksheetsonline.herokuapp.com/{student_workheet.get_absolute_url()}')


class FinishedWorksheet(DetailView):
    '''
    Where the student can view their finished worksheet.
    '''
    template_name_suffix = '_finished'
    model = StudentWorksheet

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        worksheet = context.get('studentworksheet')

        student_answers = worksheet.answers
        teacher_answers = worksheet.worksheet.answers

        context.update({'teacher_answers': teacher_answers, 'student_answers': student_answers})

        new_worksheet = transform_to_answers(worksheet, student_answers)
        context['studentworksheet'].worksheet.original_text = new_worksheet

        return context
