from django.shortcuts import *
from .models import *
from django.http import *
from django.template.context import RequestContext
from .forms import *
from dal import autocomplete
from django.views.generic import *


def home(request):
    return render(request, template_name="home.html", context={'user': request.user})


def user_page(request, usafa_id):
    cForm, lForm, bForm = False, False, False
    bioform = bioForm(instance=Account.objects.filter(usafa_id=usafa_id)[0])
    contactform = contactForm(instance=Account.objects.filter(usafa_id=usafa_id)[0])
    locationform = locationForm(instance=Account.objects.filter(usafa_id=usafa_id)[0])
    if request.method=='POST':
        if 'bioForm' in request.POST:
            bioform = bioForm(request.POST, instance=Account.objects.filter(usafa_id=usafa_id)[0])
            if bioform.is_valid():
                bioform.save()
            else:
                bForm=True
        if 'contactForm' in request.POST:
            contactform = contactForm(request.POST, instance=Account.objects.filter(usafa_id=usafa_id)[0])
            if contactform.is_valid():
                contactform.save()
            else:
                cForm=True
        if 'locationForm' in request.POST:
            locationform = locationForm(request.POST, instance=Account.objects.filter(usafa_id=usafa_id)[0])
            if locationform.is_valid():
                locationform.save()
            else:
                lForm=True

    return render(request, template_name='accounts/user_page.html', context={
        'user': Account.objects.filter(usafa_id=usafa_id)[0],
        'bioForm': bioform,
        'contactForm': contactform,
        'locationForm': locationform,
        'cForm': cForm,
        'lForm': lForm,
        'bForm': bForm,

    })


class account_name_autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Account.objects.none()

        qs = Account.objects.all()

        if self.q:
            qs = qs.filter(proper_name__istartswith=self.q)
        return qs
class directory(ListView):
    template_name = 'directory/directory.html'
    model = Account
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = account_search()
        return context

    def get_queryset(self):
        try:
            name = self.kwargs['name']
        except:
            name = ''
        if (name != ''):
            object_list = self.model.objects.filter(full_name__icontains = name)
        else:
            object_list = self.model.objects.all()
        return object_list

def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response

def discus_home(request):
    if 'discusAdmin' in request.user.group_dict:
        boards = Board.objects.all()
    else:
        boards = Board.objects.filter(is_archived=False)
    return render(request, template_name='discus/discus_home.html', context = {'boards': boards})
def board_archive(request, uid):
    if 'discusAdmin' in request.user.group_dict:
        board = get_object_or_404(Board, id=uid)
        board.archive()
        board.save()
    return redirect('discus_home')
def board_unarchive(request, uid):
    if 'discusAdmin' in request.user.group_dict:
        board = get_object_or_404(Board, id=uid)
        board.unarchive()
        board.save()
    return redirect('discus_home')
def discus_board(request, id):
    user = request.user
    board = Board.objects.filter(id=id)[0]
    posts = Post.objects.filter(board=board).filter(is_archived=False)
    return render(request, template_name='discus/discus_board.html', context={'user': user, 'posts': posts,
                                                                                  'board': board})
def discus_post(request, id):
    user = request.user
    post = Post.objects.filter(id=id)[0]
    return render(request, template_name='discus/discus_post.html', context={'user': user, 'post': post,})
def new_board(request):
    if 'discusAdmin' in request.user.group_dict:
        if request.method == 'POST':
            form = create_board(request.POST)
            if form.is_valid():
                board = form.save(commit=False)
                board.creator = request.user
                board.save()
                return redirect('discus_home')
        else:
            form = create_board()
        return render(request, 'discus/create_board.html', {'form': form})
def edit_board(request, bid):
    if 'discusAdmin' in request.user.group_dict:
        if request.method == 'POST':
            form = create_board(request.POST)
            if form.is_valid():
                board = Board.objects.filter(id=bid)[0]
                if board is not None:
                    board.name = form.cleaned_data['name']
                    board.description = form.cleaned_data['description']
                else:
                    board = form.save(commit=False)
                board.creator = request.user
                board.save()
                return redirect('discus_home')
        else:
            board = Board.objects.filter(id=bid)[0]
            if board is not None:
                data = {'name': board.name, 'description': board.description,}
                form = create_board(initial=data)
            else:
                form = create_board()
        return render(request, 'discus/create_board.html', {'form': form})
def new_post(request, bid):
    if request.method == 'POST':
        form = create_post(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.board = Board.objects.filter(pk=bid)[0]
            post.save()
            return redirect('discus_board', id=bid)
    else:
        form = create_post()
    return render(request, 'discus/create_post.html', {'form': form})
def delete_post(request, bid, pid):
    post=get_object_or_404(Post, id=pid)
    if post.creator.usafa_id == request.user.usafa_id:
        post.delete()
    return redirect('discus_board', id=bid)
def new_reply(request, pid):
    if request.method == 'POST':
        form = create_post(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.creator = request.user
            reply.reply_to = Post.objects.filter(pk=pid)[0]
            reply.save()
            return redirect('discus_post', id=pid)
    else:
        form = create_post()
    return render(request, 'discus/create_post.html', {'form': form})
def delete_reply(request, pid1, pid2):
    post=get_object_or_404(Post, id=pid2)
    if post.creator.usafa_id == request.user.usafa_id:
        post.delete()
    return redirect('discus_post', id=pid1)

