from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Invoice, InvoiceDetail

@api_view(['GET', 'POST'])
def invoices(request):
    if request.method == 'GET':
        invoices = Invoice.objects.all()
        data = []
        for invoice in invoices:
            invoice_data = {
                'id': invoice.id,
                'date': invoice.date,
                'customer_name': invoice.customer_name,
                'details': [{
                    'description': detail.description,
                    'quantity': detail.quantity,
                    'unit_price': detail.unit_price,
                    'price': detail.price
                } for detail in invoice.details.all()]
            }
            data.append(invoice_data)
        return Response(data)

    elif request.method == 'POST':
        invoice_data = request.data
        invoice_details_data = invoice_data.pop('details', None)
        invoice = Invoice.objects.create(**invoice_data)

        if invoice_details_data:
            for detail_data in invoice_details_data:
                InvoiceDetail.objects.create(invoice=invoice, **detail_data)

        return Response({'message': 'Invoice created successfully'}, status=status.HTTP_201_CREATED)

# Create your views here.
