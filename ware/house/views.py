from django.shortcuts import get_object_or_404, redirect, render
from home.models import *
from django.utils import timezone
from .models import *
# Create your views here.
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from django.conf import settings
import os
# new




def invoice(request, id):
    customer = Customer.objects.get(id=id)
    timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    invoice_number = f"INV-{customer.id}-{timestamp}"
    customer.invoice_number = invoice_number
    customer.save()
    
    if request.method == 'POST':
        lr_number = request.POST.get('lr_number')
        subtotal = float(request.POST.get('subtotal', 0))
        cgst = float(request.POST.get('cgst', 0))
        sgst = float(request.POST.get('sgst', 0))
        total = float(request.POST.get('total', 0))

        invoice = Invoice.objects.create(
            customer=customer,
            invoice_number=invoice_number,
            lr_number=lr_number,
            subtotal=subtotal,
            cgst=cgst,
            sgst=sgst,
            total=total
        )

        descriptions = request.POST.getlist('description[]')
        quantities = request.POST.getlist('quantity[]')
        prices = request.POST.getlist('price[]')

        for desc, qty, price in zip(descriptions, quantities, prices):
            quantity = int(qty)
            unit_price = float(price)
            amount = quantity * unit_price

            InvoiceItem.objects.create(
                invoice=invoice,
                description=desc,
                quantity=quantity,
                price=unit_price,
                amount=amount
            )

        return redirect('invoice_detail', invoice_id=invoice.id)

    return render(request, 'house/invoice.html', {
        'customer': customer,
        'timestamp': timestamp
    })



def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    items = InvoiceItem.objects.filter(invoice=invoice)
    
    return render(request, 'house/template.html', {
        'invoice': invoice,
        'items': items,
        'for_pdf': False
    })
    
    
    
    
    
    
    



# from django.http import HttpResponse
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import mm
# from reportlab.pdfgen import canvas

# def invoice_pdf(request, invoice_id):
#     # Fetch your invoice and items from DB (pseudo-code)
#     invoice = Invoice.objects.get(id=invoice_id)
#     items = invoice.items.all()  # assuming related name is items

#     # Create HTTP response with PDF content type
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'

#     # Create a canvas to draw on
#     c = canvas.Canvas(response, pagesize=A4)
#     width, height = A4

#     # Draw title
#     c.setFont("Helvetica-Bold", 16)
#     c.drawString(30 * mm, height - 30 * mm, "Invoice")

#     # Draw invoice details
#     c.setFont("Helvetica", 12)
#     c.drawString(30 * mm, height - 40 * mm, f"Invoice Number: {invoice.invoice_number}")
#     c.drawString(30 * mm, height - 50 * mm, f"Date: {invoice.date_created.strftime('%d-%m-%Y')}")
#     c.drawString(30 * mm, height - 60 * mm, f"Customer: {invoice.customer.name}")

#     # Draw table header
#     c.drawString(30 * mm, height - 80 * mm, "Sr No.")
#     c.drawString(50 * mm, height - 80 * mm, "Description")
#     c.drawString(120 * mm, height - 80 * mm, "Quantity")
#     c.drawString(150 * mm, height - 80 * mm, "Amount (INR)")

#     y = height - 90 * mm
#     for i, item in enumerate(items, start=1):
#         c.drawString(30 * mm, y, str(i))
#         c.drawString(50 * mm, y, item.description)
#         c.drawString(120 * mm, y, str(item.quantity))
#         c.drawString(150 * mm, y, f"{item.price:.2f}")
#         y -= 10 * mm
#         if y < 30 * mm:  # Add page break if needed
#             c.showPage()
#             y = height - 30 * mm

#     # Draw totals
#     c.drawString(120 * mm, y - 10 * mm, "Subtotal:")
#     c.drawString(150 * mm, y - 10 * mm, f"{invoice.subtotal:.2f}")

#     c.drawString(120 * mm, y - 20 * mm, "CGST 6%:")
#     c.drawString(150 * mm, y - 20 * mm, f"{invoice.cgst:.2f}")

#     c.drawString(120 * mm, y - 30 * mm, "SGST 6%:")
#     c.drawString(150 * mm, y - 30 * mm, f"{invoice.sgst:.2f}")

#     c.setFont("Helvetica-Bold", 12)
#     c.drawString(120 * mm, y - 45 * mm, "Total:")
#     c.drawString(150 * mm, y - 45 * mm, f"{invoice.total:.2f}")

#     c.showPage()
#     c.save()

#     return response


def invoice_pdf(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    items = invoice.items.all()

    html_string = render_to_string('house/template.html', {
        'invoice': invoice,
        'items': items,
        'for_pdf': True
    })

    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="invoice_{invoice.invoice_number}.pdf"'
    return response

