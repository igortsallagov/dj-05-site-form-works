from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from .models import Product, Review
from .forms import ReviewForm


class ProductsList(ListView):
    model = Product
    context_object_name = 'product_list'


class ProductView(DetailView):
    model = Review

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs['pk'])
        reviews = Review.objects.filter(product=product)
        context = dict()
        context['product'] = product
        if reviews:
            context['reviews'] = reviews
        if not request.session['reviewed_products']:
            request.session['reviewed_products'] = list()
        if product.id not in request.session['reviewed_products']:
            context['form'] = ReviewForm()
        else:
            context['review_exists'] = True
        return render(request, 'app/product_detail.html', context)

    def post(self, request, **kwargs):
        product = kwargs['pk']
        request.session.modified = True
        request.session['reviewed_products'].append(product)
        form = ReviewForm(
            {'text': request.POST['text']}
        )
        if form.is_valid():
            filled_form = form.save(commit=False)
            filled_form.product_id = product
            form.save()
            return redirect('product_detail', pk=product)
