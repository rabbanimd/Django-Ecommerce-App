from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
# from .models import items
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.http import HttpResponseRedirect
from .models import items, OrderItem, Order, address, payment, Category
from django.db.models import Q
from itertools import chain
import stripe
from django.contrib import messages
from .forms import checkout_form,SearchForm
from .filters import FilterPro

# stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'
class HomeView(ListView):
    context_object_name = 'name'
    template_name = 'index.html'
    queryset = items.objects.all()
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['product'] = self.queryset
        return context

class ItemDetailView(DetailView):
    model = items
    template_name = "cart.html"

def categories(request, category_slug=None):
    category=None
    categories = Category.objects.all()
    product = items.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        product = items.objects.filter(category=category)
    context = {'category': category,
               'categories':categories,
               'product': product
               }
    return render(request,"index.html",context)
def product(request,slug,id):
    products = get_object_or_404(items,id=id,slug=slug,available=True)
    context = {
        'products': products,
    }
    return render(request, 'cart.html', context)


@login_required
def add_item(request, slug):
    item = get_object_or_404(items, slug=slug)
    order_item, create = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    details = Order.objects.filter(user=request.user, ordered=False)
    if details.exists():
        order = details[0]
        if order.product.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "item is updated to cart")
            return redirect("cart:product", slug=slug)

        else:
            messages.info(request, "item is added to cart")
            order.product.add(order_item)
            return redirect("/", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.product.add(order_item)
        messages.info(request, "item is updated to cart")
    return redirect("cart:product", slug=slug)


@login_required()
def delete_item(request, slug):
    item = get_object_or_404(items, slug=slug)
    details = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if details.exists():
        order = details[0]
        # check if the order item is in the order
        if order.product.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.product.remove(order_item)
            order_item.delete()
            messages.info(request, "This item is removed from your cart.")
            return redirect("cart:order_details")
        else:
            messages.info(request, "This item is not in your cart")
            return redirect("cart:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart:product", slug=slug)


class order_details(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "order_details.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "cart is Empty")
            return redirect("cart:order_details")


@login_required()
def remove_qty(request, slug):
    item = get_object_or_404(items, slug=slug)
    details = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if details.exists():
        order = details[0]
        # check if the order item is in the order
        if order.product.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.product.remove(order_item)
            return redirect("cart:order_details")


class checkout(View):

    def get(self, *args, **kwargs):
        form = checkout_form()
        context = {
            'form': form
           }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        # if self.request . method== 'POST' :
        form = checkout_form(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                st_address = form.cleaned_data.get('st_address')
                home_address = form.cleaned_data.get('home_address2')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # same_billing_add = form.cleaned_data.get('same_billing_add')
                # save_info = form.cleaned_data.get('save_info')
                payment_op = form.cleaned_data.get('payment_op')
                billing_address = address(
                    user=self.request.user,
                    st_address=st_address,
                    home_address=home_address,
                    country=country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('cart:checkout')
            messages.warning(self.request, "failed to checkout")
            return redirect("cart:checkout")
            return render(self.request, "order_details.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "cart is Empty")
            return redirect("cart:order_details")


class payment(View):
    def get(self, *rgs, **kwargs):
        return render(self.request, "payment.html")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = order.get_total() * 100
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
            )
            # Use Stripe's library to make requests...
            pass
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught

            print('Status is: %s' % e.http_status)
            print('Type is: %s' % e.error.type)
            print('Code is: %s' % e.error.code)
            # param is '' in this case
            print('Param is: %s' % e.error.param)
            print('Message is: %s' % e.error.message)
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            pass
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            pass
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            pass
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            pass
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            pass
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            pass

        # craete the payment
        payment = payment()
        payment.str_chrg_id = charge[id]
        payment.user = self.request.user
        payment.amount = amount
        payment.save()
        # assign the payment to the  return render(request,) order
        order.ordered = True
        order.payment = payment
        order.save()


@login_required
def wish_list(request):
    return render(request, "wishlist.html")


def search(request):
    if request.method== 'POST':
        query = request.POST['query']
        result=items.objects.all()
        if query:
            if len(query)>78:
                result=items.objects.none()
            else:
                result=items.objects.filter(title__icontains=query)
                # result2=items.objects.filter(title__icontains=query)
                # # result2=items.objects.filter(title__icontains=query)
                # result=list(result1)+list(result2)
            if result.count() == 0:
                messages.warning(request,"no search result found. Please refine your query")

            context = {'result': result, 'query': query}
            return render(request,'search.html',context)

    #
