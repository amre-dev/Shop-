from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Order, OrderItem
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.urls import reverse
import urllib.parse
import random

def home(request):
    categories = Category.objects.all().order_by('position','name')
    return render(request, 'home.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(is_visible=True)
    return render(request, 'category.html', {'category': category, 'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product.html', {'product': product})

# Simple session-based cart
def _get_cart(request):
    return request.session.setdefault('cart', {})

def cart_detail(request):
    cart = _get_cart(request)
    products = []
    total = 0
    for pid, qty in cart.items():
        try:
            p = Product.objects.get(id=pid)
            subtotal = p.price * qty
            products.append({'product': p, 'quantity': qty, 'subtotal': subtotal})
            total += subtotal
        except Product.DoesNotExist:
            continue
    return render(request, 'cart.html', {'items': products, 'total': total})

def cart_add(request):
    if request.method == 'POST':
        pid = request.POST.get('product_id')
        qty = int(request.POST.get('quantity', '1'))
        cart = _get_cart(request)
        cart[pid] = cart.get(pid, 0) + qty
        request.session['cart'] = cart
    return redirect('cart_detail')

@transaction.atomic
def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        note = request.POST.get('note', '').strip()
        cart = _get_cart(request)
        if not cart:
            return redirect('cart_detail')
        total = 0
        items = []
        for pid, qty in cart.items():
            p = Product.objects.get(id=pid)
            subtotal = p.price * qty
            total += subtotal
            items.append((p, qty, subtotal))
        # create order
        order_number = f"ORD-{timezone.now().strftime('%Y%m%d')}-{random.randint(1000,9999)}"
        order = Order.objects.create(order_number=order_number, customer_name=name or 'غير معروف', customer_phone=phone or '', customer_address=address, total_amount=total, via='whatsapp', note=note)
        for p, qty, subtotal in items:
            OrderItem.objects.create(order=order, product=p, product_name=p.name, quantity=qty, unit_price=p.price, subtotal=subtotal)
        # build whatsapp message
        lines = [f"طلب جديد: {order.order_number}", f"الاسم: {order.customer_name}", f"الهاتف: {order.customer_phone}", f"العنوان: {order.customer_address}", "المنتجات:"]
        for idx, (p, qty, subtotal) in enumerate(items, start=1):
            lines.append(f"{idx}) {p.name} - الكمية: {qty} - السعر للوحدة: {p.price} - المجموع: {subtotal}")
        lines.append(f"الإجمالي: {total}")
        if note:
            lines.append(f"ملاحظة: {note}")
        lines.append(f"رقم الطلب داخلي: {order.order_number}")
        msg = '\n'.join(lines)
        wa_number = settings.WHATSAPP_NUMBER
        wa_text = urllib.parse.quote(msg)
        # keep order in DB (done) and clear cart
        request.session['cart'] = {}
        # create wa.me link and redirect
        wa_link = f"https://wa.me/{wa_number.replace('+','')}?text={wa_text}"
        return redirect(wa_link)
    else:
        return render(request, 'checkout.html')
