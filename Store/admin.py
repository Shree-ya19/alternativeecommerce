from django.contrib import admin
from .models import *
from django.db.models import Sum
import datetime

class MonthlySalesAdmin(admin.ModelAdmin):
    change_list_template = 'admin/monthly_sales.html'  # Custom template for monthly sales report

    # Add filter options for 'date_ordered' and 'customer'
    list_filter = ('date_ordered', 'customer')

    # Add search fields for searching by customer name or email
    search_fields = ['customer__username', 'customer__email']

    # List display for Order model in the admin panel
    list_display = ('id', 'customer', 'get_total_amount', 'date_ordered')  # Use get_total_amount method here

    # Custom method to calculate the total amount for each order
    def get_total_amount(self, obj):
        total_amount = 0
        for item in obj.orderitem_set.all():
            total_amount += item.quantity * item.product.price
        return total_amount

    get_total_amount.short_description = 'Total Amount'  # Display name in the admin panel

    def changelist_view(self, request, extra_context=None):
        current_month = datetime.date.today().month
        current_year = datetime.date.today().year

        month_name = datetime.date(current_year, current_month, 1).strftime('%B')

        monthly_sales = Order.objects.filter(date_ordered__month=current_month, date_ordered__year=current_year)

        total_sales = 0
        orders_with_totals = []
        for order in monthly_sales:
            order_total = 0
            for item in order.orderitem_set.all():
                order_total += item.quantity * item.product.price
                total_sales += item.quantity * item.product.price

            if order_total > 0:
                orders_with_totals.append({
                    'order': order,
                    'total_amount': order_total
                })

        total_transactions = len(orders_with_totals)

        extra_context = {
            'monthly_sales': orders_with_totals,
            'total_sales': total_sales,
            'total_transactions': total_transactions,
            'current_month': month_name,
            'current_year': current_year,
        }

        return super().changelist_view(request, extra_context=extra_context)

    actions = ['delete_orders']

    def delete_orders(self, request, queryset):
        deleted_count, _ = queryset.delete()
        self.message_user(request, f"{deleted_count} orders were successfully deleted.")
    delete_orders.short_description = "Delete selected orders"

# Register models with custom MonthlySalesAdmin
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order, MonthlySalesAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Category)
