from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag


# Create your views here.
# Show posts list
def post_list(request, tag_slug=None):
    object_list = Post.published.all()

    # Tags
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    # Pagination
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        'blog/post/list.html',
        {
            'page': page,
            'posts': posts,
            'tag': tag,
        }
    )


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# Show post detail
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    # List active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # User sent comment
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment without saving in BD
            new_comment = comment_form.save(commit=False)
            # Link a comment to the current article
            new_comment.post = post
            # Save comment to BD
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
        }
    )


# Share form
def post_share(request, post_id):
    # Get post on id
    post = get_object_or_404(
        Post,
        id=post_id,
        status='published',
    )
    sent = False
    if request.method == 'POST':
        # form arrived to save
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # validation is True
            cd = form.cleaned_data
            # sending
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin0@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )
