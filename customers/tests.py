from django.test import TestCase
from django.urls import reverse
from customers.models import Customer


class CustomerModelTests(TestCase):
    def test_customer_creation_and_str(self):
        customer = Customer.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
            address="123 Main St",
        )
        self.assertEqual(str(customer), "John Doe")
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(customer.email, "john@example.com")
        self.assertEqual(customer.phone, "1234567890")
        self.assertEqual(customer.address, "123 Main St")
        self.assertIsNotNone(customer.created_at)


class CustomerViewsTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Alice Smith",
            email="alice@example.com",
            phone="5551234567",
            address="456 Elm St",
        )

    def test_customer_list_view(self):
        response = self.client.get(reverse('customer-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/customer_list.html')
        self.assertContains(response, "Alice Smith")
        self.assertContains(response, "alice@example.com")

    def test_customer_detail_view(self):
        response = self.client.get(reverse('customer-detail', kwargs={'pk': self.customer.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/customer_detail.html')
        self.assertContains(response, "Alice Smith")
        self.assertContains(response, "5551234567")
        self.assertContains(response, "456 Elm St")

    def test_customer_create_view_get(self):
        response = self.client.get(reverse('customer-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/customer_form.html')
        self.assertContains(response, "Add New Customer")

    def test_customer_create_view_post(self):
        data = {
            'name': 'Bob Jones',
            'email': 'bob@example.com',
            'phone': '9876543210',
            'address': '789 Oak Ave',
        }
        response = self.client.post(reverse('customer-create'), data)
        self.assertRedirects(response, reverse('customer-list'))
        self.assertTrue(Customer.objects.filter(email='bob@example.com').exists())

    def test_customer_update_view_get(self):
        response = self.client.get(reverse('customer-update', kwargs={'pk': self.customer.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/customer_form.html')
        self.assertContains(response, "Edit Customer")

    def test_customer_update_view_post(self):
        data = {
            'name': 'Alice Updated',
            'email': 'alice_new@example.com',
            'phone': '1112223333',
            'address': 'New Address',
        }
        response = self.client.post(reverse('customer-update', kwargs={'pk': self.customer.pk}), data)
        self.assertRedirects(response, reverse('customer-list'))
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, "Alice Updated")
        self.assertEqual(self.customer.email, "alice_new@example.com")

    def test_customer_delete_view_get(self):
        response = self.client.get(reverse('customer-delete', kwargs={'pk': self.customer.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/customer_confirm_delete.html')
        self.assertContains(response, "Are you sure you want to delete")
        self.assertContains(response, self.customer.name)

    def test_customer_delete_view_post(self):
        response = self.client.post(reverse('customer-delete', kwargs={'pk': self.customer.pk}))
        self.assertRedirects(response, reverse('customer-list'))
        self.assertFalse(Customer.objects.filter(pk=self.customer.pk).exists())
