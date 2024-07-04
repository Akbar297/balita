from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Article, Category, Contact, Comments, Tag
from .validators import validate_contact_form
import requests

BOT_TOKEN = '6538606606:AAH2YUwidwBTWHweGrdz_3rlBeI99UkTqok'
CHAT_ID = '728795819'


def home_view(request):
    data = request.GET
    page = data.get('page', 1)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    slider_article = Article.objects.all().order_by('-view_count')[:3]
    posts = Article.objects.all().order_by('-view_count')
    pag_obj = Paginator(posts, 4)
    last_post = Article.objects.all().order_by('-created_at')[:3]
    more_blog_post = Article.objects.all().order_by('view_count')[:3]

    d = {
        "home": "active",
        "categories": categories,
        "tags": tags,
        "slider_article": slider_article,
        "posts": pag_obj.get_page(page),
        "last_post": last_post,
        "more_blog_post": more_blog_post
    }
    return render(request, 'index.html', context=d)


def about_view(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()

    d = {
        "about": "active",
        "categories": categories,
        "tags": tags

    }
    return render(request, 'about.html', context=d)


def categories_view(request, pk):
    data = request.GET
    page = data.get('page', 1)
    cat = data.get('cat', None)
    if cat:
        articles = Article.objects.filter(is_published=True, category_id=cat)
        d = {
            'articles': articles,
            'category': 'active'
        }
        return render(request, 'blog.html', context=d)
    articles = Article.objects.filter(category=pk)

    page_obj = Paginator(articles, 2)

    categories = Category.objects.all()

    tags = Tag.objects.all()

    cat_name = categories.filter(id=pk).first().name
    d = {
        'articles': page_obj.get_page(page),
        "category": "active",
        "categories": categories,
        "cat_name": cat_name,
        "tags": tags,
    }
    return render(request, 'category.html', context=d)


def article_info(request, pk):
    if request.method == 'POST':
        data = request.POST
        comment = Comments.objects.create(article_id=pk, name=data['name'], email=data['email'],
                                          message=data['message'])
        comment.save()
        return redirect(f'/category/{pk}/')
    detail = Article.objects.filter(id=pk).first()
    print(detail.tags.all())
    categories = Category.objects.all()
    tags = Tag.objects.all()
    detail.view_count += 1
    detail.save(update_fields=['view_count'])
    comments = Comments.objects.filter(id=pk)
    d = {
        "category": "active",
        'comments': comments,
        "categories": categories,
        "detail": detail,
        "comments_count": len(comments),
        "tags": tags
    }
    return render(request, 'blog-single.html', context=d)


def contact_view(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    d = {
        "contact": "active",
        "categories": categories,
        "tags": tags
    }
    if request.method == 'POST':
        data = request.POST
        validate = validate_contact_form(data)
        if validate['ok'] is True:
            obj = Contact.objects.create(name=data['name'], email=data['email'], message=data['message'],
                                         phone_number=data['phone'])
            obj.save()
            text = f"""
                    project: BALITA \nid: {obj.id} \nname: {obj.name} \ntime_step: {obj.created_at} \nmessage: {obj.message}
                    """

            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=<{text}>'
            response = requests.get(url)
            print(response)
            return redirect('/contact')
        d['error'] = validate['error']
        return render(request, 'contact.html', context=d)

    return render(request, 'contact.html', context=d)


def search_view(request):
    if request.method == 'POST':
        data = request.POST
        query = data['query']
        return redirect(f'/search?q={query}')

    query = request.GET.get('q')
    if query is not None and len(query) >= 1:
        articles = Article.objects.filter(is_published=True, title__icontains=query, description__icontains=query)
    else:
        articles = Article.objects.filter(is_published=True)

    d = {
        'articles': articles,
        'categories': Category.objects.all()
    }
    return render(request, 'category.html', context=d)


def tag_view(request, pk):
    data = request.GET
    page = data.get('page', 1)
    articles = Article.objects.filter(tags__in=[pk])

    page_obj = Paginator(articles, 2)

    categories = Category.objects.all()

    tags = Tag.objects.all()

    d = {
        'articles': page_obj.get_page(page),
        "category": "active",
        "categories": categories,
        "tags": tags,
    }
    return render(request, 'category.html', context=d)
