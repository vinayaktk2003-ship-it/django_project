from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Customer


class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'


class CustomerCreateView(CreateView):
    model = Customer
    fields = ['name', 'email', 'phone', 'address']
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer-list')


class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ['name', 'email', 'phone', 'address']
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer-list')


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customer-list')
