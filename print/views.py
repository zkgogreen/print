from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import win32print
import win32api
import os
from datetime import datetime

def generate_and_print_pdf(request):
    # Get parameters from the request
    number = request.GET.get('number', '0001')
    datetime_str = request.GET.get('datetime', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    date_to_print = request.GET.get('datekasir', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    toko = request.GET.get('toko', 'Default Store')
    kasir = request.GET.get('kasir', 'Default Cashier')
    pembayaran = request.GET.get('pembayaran', '0.00')
    total = request.GET.get('total', '0.00')
    metode_bayar = request.GET.get('metode_bayar', 'Cash')
    kembalian = request.GET.get('kembalian', '0.00')

    # Define the file path
    pdf_path = 'receipt.pdf'
    
    # Create a PDF file
    c = canvas.Canvas(pdf_path, pagesize=(227, 400))  # 227 points = 80mm width
    c.setFont("Helvetica", 12)
    
    # Function to draw justified text
    def draw_justified_text(c, text_left, text_right, y):
        c.drawString(10, y, text_left)
        text_width = c.stringWidth(text_right, "Helvetica", 12)
        c.drawString(227 - 10 - text_width, y, text_right)
    
    # Add content to the PDF
    c.drawString(10, 390, toko)
    draw_justified_text(c, "Receipt No:", number, 370)
    draw_justified_text(c, "waktu:", datetime_str, 350)
    c.drawString(10, 330, "-"*63)
    draw_justified_text(c, "Total Pembayaran:", f"Rp.{pembayaran}", 310)
    draw_justified_text(c, "Total Bayar:", f"Rp.{total}", 290)
    draw_justified_text(c, "Kembalian:", f"Rp.{kembalian}", 270)
    
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
        print("Print job sent successfully.")
    except Exception as e:
        return HttpResponse(f"<center><h1>Gagal print dokumen : {str(e)} </h1></center>")
    
    # Return a response
    return HttpResponse("<script>window.close();</script>")
