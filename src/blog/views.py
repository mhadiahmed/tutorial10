from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib import messages
from django.db.models import Q
from .models import post
from .forms import PostForm

#List View
def post_list(request):
	query = post.objects.all().order_by('-puplish') # select * from post
	q = request.GET.get('q')
	if q:
		query = query.filter(
			Q(title__icontains=q)|
			Q(content__icontains=q)|
			Q(user__username__icontains=q)
			)
	paginator = Paginator(query, 10) # Show 10 posts per page
	page_var = 'page'
	page = request.GET.get(page_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	context = {
	'views_title':'list',
	'query':queryset,
	'page_var':page_var,
	}
	return render(request,"list.html",context)

# Detail View
def post_detail(request,id):
	# instance = post.objects.get(id=13)
	instance = get_object_or_404(post,id=id)
	context = {
	'views_title':'detail',
	'instance':instance
	}
	return render(request,"detail.html",context)

# Create View
def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request,'Successfuly Created')
		return HttpResponseRedirect(instance.get_url())
	context = {
	'views_title':'create',
	'btn':'Create',
	'form':form
	}
	return render(request,"form.html",context)

# Update View
def post_update(request,id):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(post,id=id)
	form = PostForm(request.POST or None,request.FILES or None,instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,'item saved')
		return HttpResponseRedirect(instance.get_url())
	context = {
	'views_title':'update',
	'instance':instance,
	'btn':'Edit',
	'form':form
	}
	return render(request,"form.html",context)

# Delete View
def post_delete(request,id):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(post,id=id)
	instance.delete()
	messages.success(request,'Successfuly deleted')
	return redirect('list')
