from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import win32print
import win32api
import os
from datetime import datetime
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from main.models import Main, FieldMenu

def splitItem(item : str):
    return item.replace(' ','').replace("'",'').split(',')

def split_array_into_chunks(array):
    results = [array[i:i + 18] for i in range(0, len(array), 18)]
    return results

def generate_and_print_pdf(request):
    # Ambil data master
    data = Main.objects.filter(utama=True)

    # Jika tidak ada data yang ditandai sebagai 'utama', set salah satu sebagai 'utama'
    if not data.exists():
        print("not data.exists()")
        data = Main.objects.all().first()
        data.utama = True
        data.save()
    # Jika ada lebih dari satu data yang 'utama', set satu sebagai 'utama' dan yang lainnya sebagai 'tidak utama'
    elif data.count() > 1:
        print(" data.count() > 1")
        data.update(utama=False)
        data = data.first()
        data.utama = True
        data.save()
    else:
        # Ambil main pertama yang sudah utama
        print("else")
        data = data.first()

    # Tentukan urutan default untuk field 'jumlah', 'rasa', 'varian', dan 'harga'
    urutan_fields = {
        'jumlah': 14,
        'rasa': 6,
        'varian': 5,
        'harga': 15
    }

    # Loop melalui FieldMenu untuk memperbarui urutan berdasarkan nama field
    for item in FieldMenu.objects.filter(main=data):
        if item.nama in urutan_fields:
            urutan_fields[item.nama] = item.urutan

    # Ambil parameter dari request dengan nilai default
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

    # Di sini tambahkan logika untuk mengenerate PDF dengan parameter di atas

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
    if data.alamat:
        c.drawString(data.padding, y, data.alamat)
        y -= 17
    if data.telp:
        c.drawString(data.padding, y, data.telp)
        y -= 17
    c.drawString(data.padding, y, "-"*60)
    y -= 17
    c.drawString(data.padding, y, datetime_str)
    y -= 20
    c.drawString(data.padding, y, number)   
    y -= 20
    c.drawString(data.padding, y, "-"*60)
    y -= 17
    for arr in arraylist:
        draw_justified_text(c, f"{arr[urutan_fields['jumlah']-1]}x {arr[urutan_fields['rasa']-1]} {arr[urutan_fields['varian']-1]}", f"Rp.{arr[urutan_fields['harga']-1]}", y)
        y -= 15
        for item in [col for i, col in enumerate(arr) if i not in [urutan_fields['jumlah'], urutan_fields['rasa'], urutan_fields['varian'], urutan_fields['harga']]]:
            if item == '':
                continue
            c.drawString(data.padding, y, f"  {item}")
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
    y -= 20
    if data.wifi:
        c.drawString(data.padding, y, "-"*60)
        y -= 20
        c.drawString(data.padding, y, "WIFI")
        y -= 20
        c.drawString(data.padding, y, "SSID : "+str(data.wifi))
        y -= 17
        c.drawString(data.padding, y, "PASSWORD : "+str(data.password_wifi))
        y -= 17
    if data.ucapan:
        ucapan = data.ucapan.splitlines()
        c.drawString(data.padding, y, "-"*60)
        y -= 20
        for ucap in ucapan:
            c.drawString(data.padding, y, str(ucap))
            y -= 17

    
    # Finish up and save the PDF
    c.showPage()
    c.save()
    
    # Print the PDF file
    try:
        # printer_name = win32print.GetDefaultPrinter()
        # win32api.ShellExecute(
        #     0,
        #     "print",
        #     pdf_path,
        #     f'/d:"{printer_name}"',
        #     ".",
        #     0
        # )
        print("Print job sent successfully. "+str(data.font))
    except Exception as e:
        return HttpResponse(f"<center><h1>Gagal print dokumen : {str(e)} </h1></center>")
    
    # Return a response
    return HttpResponse("<script>window.close();</script>")
