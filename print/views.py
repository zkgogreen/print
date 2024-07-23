from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import win32print
import win32api
import os
from datetime import datetime
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from main.models import Main

def generate_and_print_pdf(request):

    data = Main.objects.all().first()
    # Get parameters from the request
    number = request.GET.get('number', '0001')
    datetime_str = request.GET.get('datetime', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    date_to_print = request.GET.get('datekasir', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    toko = request.GET.get('toko', data.toko)
    kasir = request.GET.get('kasir', 'Default Cashier')
    pembayaran = request.GET.get('pembayaran', '0.00')
    total = request.GET.get('total', '0.00')
    metode_bayar = request.GET.get('metode_bayar', 'Cash')
    kembalian = request.GET.get('kembalian', '0.00')

    # Define the file path
    pdfmetrics.registerFont(TTFont('PuffFont', data.font))
    pdf_path = 'receipt.pdf'
    y = data.page_higth
    # Create a PDF file
    c = canvas.Canvas(pdf_path, pagesize=(data.page_width, y))  # 227 points = 80mm width
    c.setFont("PuffFont", data.font_size)
    
    # Function to draw justified text
    def draw_justified_text(c, text_left, text_right, y):
        c.drawString(data.padding, y, text_left)
        text_width = c.stringWidth(text_right, "PuffFont", data.font_size)
        c.drawString(data.page_width - data.padding - text_width, y, text_right)
    
    
    y -= 40
    
    c.drawString(data.padding, y, toko)
    y -= 20
    c.drawString(data.padding, y, "Mitra")
    y -= 17
    c.drawString(data.padding, y, "-"*60)
    y -= 17
    c.drawString(data.padding, y, datetime_str)
    y -= 20
    c.drawString(data.padding, y, number)
    y -= 17
    c.drawString(data.padding, y, "-"*60)
    y -= 17
    draw_justified_text(c, "1x Puff", f"Rp.{pembayaran}", y)
    y -= 17
    c.drawString(data.padding, y, "-"*60)
    y -= 17
    draw_justified_text(c, "Total", f"Rp.{total}", y)
    y -= 17
    c.drawString(data.padding, y, "-"*60)
    y -= 17
    draw_justified_text(c, f"{metode_bayar}:", f"Rp.{total}", y)
    y -= 20
    draw_justified_text(c, "Change", f"Rp.{kembalian}", y)
    
    # Finish up and save the PDF
    c.showPage()
    c.save()
    
    # Print the PDF file
    try:
        printer_name = win32print.GetDefaultPrinter()
        win32api.ShellExecute(
            0,
            "print",
            pdf_path,
            f'/d:"{printer_name}"',
            ".",
            0
        )
        print("Print job sent successfully. "+str(data.font))
    except Exception as e:
        return HttpResponse(f"<center><h1>Gagal print dokumen : {str(e)} </h1></center>")
    
    # Return a response
    return HttpResponse("<script>window.close();</script>")
