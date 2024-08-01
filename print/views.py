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

def splitItem(item : str):
    return item.replace(' ','').replace("'",'').split(',')

def split_array_into_chunks(array):
    results = [array[i:i + 18] for i in range(0, len(array), 18)]
    return results

def generate_and_print_pdf(request):

    data = Main.objects.all().first()
    # Get parameters from the request
    number = request.GET.get('number', '0001')
    datetime_str = request.GET.get('datetime', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    date_to_print = request.GET.get('datekasir', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    toko = request.GET.get('toko', data.toko)
    brand = request.GET.get('brand', data.brand)
    kasir = request.GET.get('kasir', 'Default Cashier')
    pembayaran = request.GET.get('pembayaran', '0.00')
    total = request.GET.get('total', '0.00')
    metode_bayar = request.GET.get('metode_bayar', 'Cash')
    kembalian = request.GET.get('kembalian', '0.00')

    rasa1 = splitItem(request.GET.get('rasa1')) 

    arraylist = split_array_into_chunks(rasa1)
    pdf_path = 'receipt.pdf'
    y = data.page_higth
    # Create a PDF file
    c = canvas.Canvas(pdf_path, pagesize=(data.page_width, y))  # 227 points = 80mm width
    c.setFont("Helvetica", data.font_size)
    
    # Function to draw justified text
    def draw_justified_text(c, text_left, text_right, y):
        c.drawString(data.padding, y, text_left)
        text_width = c.stringWidth(text_right, "Helvetica", data.font_size)
        c.drawString(data.page_width - data.padding - text_width, y, text_right)
    
    
    y -= 40
    
    c.drawString(data.padding, y, brand)
    y -= 17
    c.drawString(data.padding, y, toko)
    y -= 17
    c.drawString(data.padding, y, "-"*60)
    y -= 17
    c.drawString(data.padding, y, datetime_str)
    y -= 20
    c.drawString(data.padding, y, number)
    y -= 17
    c.drawString(data.padding, y, "-"*60)
    y -= 17
    for arr in arraylist:
        draw_justified_text(c, f"{arr[13]}x {arr[5]} {arr[4]}", f"Rp.{arr[14] or arr[15]}", y)
        y -= 15
        for item in arr[6:12]:
            if item == '':
                continue
            c.drawString(data.padding + 25, y, f"{item}")
            y -= 15
        c.drawString(data.padding + 25, y, f"{arr[17]}")
        y -= 15


    c.drawString(data.padding, y, "-"*60)
    y -= 17
    draw_justified_text(c, "Total", f"Rp.{pembayaran}", y)
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
