from django.contrib import messages
from django.db.models.functions import datetime
from django.shortcuts import render, redirect

from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from subcategory.models import SubCategory
from category.models import Category


# Create your views here.
def news_detail(request, pk):
    site = Main.objects.get(pk=3)
    news = News.objects.filter(pk=pk)
    category = Category.objects.all()

    context = {
        'news': news,
        'site': site,
        'category': category
    }

    return render(request, 'front/news_detail.html', context)


def news_list(request):
    news = News.objects.all()

    return render(request, 'back/news_list.html', {'news': news})


def news_add(request):
    now = datetime.datetime.now()

    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

    if len(str(month)) == 1:
        month = '0' + str(month)
    if len(str(day)) == 1:
        day = '0' + str(day)
    if len(str(hour)) == 1:
        hour = '0' + str(hour)
    if len(str(minute)) == 1:
        minute = '0' + str(minute)

    today = str(day) + '/' + str(month) + '/' + str(year)
    time = str(hour) + '/' + str(minute)

    cat = SubCategory.objects.all()

    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newscategory = request.POST.get('newscategory')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscategory')

        if newstitle == "" or newstxt == "" \
                or newstxtshort == "" \
                or newscategory == "" \
                or newstitle == "":
            messages.warning(request, "Tous les champs sont requis")
            return redirect('news_add')

        try:

            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):

                if myfile.size < 5000000:

                    newsname = SubCategory.objects.get(pk=newsid).name
                    ocategory_id = SubCategory.objects.get(pk=newsid).category_id

                    add = News(name=newstitle,
                               short_txt=newstxtshort,
                               body_txt=newstxt,
                               date=today,
                               pic_name=filename,
                               pic_url=url,
                               writer="-",
                               category_name=newsname,
                               category_id=newsid,
                               show=0,
                               time=time,
                               ocategory_id=ocategory_id)
                    add.save()

                    count = len(News.objects.filter(ocategory_id=ocategory_id))
                    b = Category.objects.get(pk=ocategory_id)
                    b.count = count
                    b.save()

                    messages.success(request, "Votre article a été ajouté avec succé")
                    return redirect('news_list')

                else:

                    fs = FileSystemStorage()
                    fs.delete(filename)

                    messages.warning(request, "L'image ne doit pas dépasser 5 MB")
                    return redirect('news_add')

            else:

                fs = FileSystemStorage()
                fs.delete(filename)

                messages.warning(request, "Le format de votre fichier n'est pas supporté")
                return redirect('news_add')

        except:

            messages.warning(request, "Vous devez téléverser une image")
            return redirect('news_add')

    return render(request, 'back/news_add.html', {'category': cat})


def news_delete(request, pk):
    try:

        b = News.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(b.pic_name)
        ocategory_id = News.objects.get(pk=pk).ocategory_id

        b.delete()

        count = len(News.objects.filter(ocategory_id=ocategory_id))
        m = Category.objects.get(pk=ocategory_id)
        m.count = count
        m.save()
        messages.success(request, "L'articles  a bien été supprimé")
        return redirect('news_list')
    except:

        messages.warning(request, "Quelque chose c'est mal passée")
        return redirect('news_list')


def news_edit(request, pk):
    if len(News.objects.filter(pk=pk)) == 0:
        messages.warning(request, "News non trouvée")
        return redirect('news_list')

    news = News.objects.get(pk=pk)
    cat = SubCategory.objects.all()

    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newscategory = request.POST.get('newscategory')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscategory')

        if newstitle == "" or newstxt == "" \
                or newstxtshort == "" \
                or newscategory == "" \
                or newstitle == "":
            messages.warning(request, "Tous les champs sont requis")
            return redirect('news_edit', pk=pk)

        try:

            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):

                if myfile.size < 5000000:

                    newsname = SubCategory.objects.get(pk=newsid).name

                    b = News.objects.get(pk=pk)

                    fss = FileSystemStorage()
                    fss.delete(b.pic_name)

                    b.name = newstitle
                    b.short_txt = newstxtshort
                    b.body_txt = newstxt
                    b.pic_name = filename
                    b.pic_url = url
                    b.category_name = newsname
                    b.category_id = newsid
                    b.save()
                    # messages.success(request, "Bravo, votre articles à bien été modifié")
                    # return redirect('news_list')
                else:
                    fs = FileSystemStorage()
                    fs.delete(filename)

                    messages.warning(request, "L'image ne doit pas dépasser 5 MB")
                    return redirect('news_edit', pk=pk)
            else:
                fs = FileSystemStorage()
                fs.delete(filename)

                messages.warning(request, "Le format de votre fichier n'est pas supporté")
                return redirect('news_edit', pk=pk)

        except:
            newsname = SubCategory.objects.get(pk=newsid).name

            add = News.objects.get(pk=pk)

            add.name = newstitle
            add.short_txt = newstxtshort
            add.body_txt = newstxt
            add.category_name = newsname
            add.category_id = newsid
            add.save()
            messages.success(request, "Votre article à bien été modifié")
            return redirect('news_list')

    context = {
        'pk': pk,
        'news': news,
        'category': cat
    }
    return render(request, 'back/news_edit.html', context)
