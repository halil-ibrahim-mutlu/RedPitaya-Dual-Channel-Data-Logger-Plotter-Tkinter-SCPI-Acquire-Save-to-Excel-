import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import socket       # as s    # redpipta olmadan aryüz açmak için s olarak tanımladım  

import time
#import openpyxl
import os


#  ayrılabilir 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('169.254.160.106', 5000))  # kendi IP ve portunu kullan  #use your ip an port number 


desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")



#/ SCROOL BAR İÇİN   to open new 
root = tk.Tk()


main_canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollable_frame = tk.Frame(main_canvas)


scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )
)

main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
main_canvas.configure(yscrollcommand=scrollbar.set)

main_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

#////////////////////////////////


frame = tk.Frame(scrollable_frame)
frame.pack(pady=10)



# ustteki girdi yazılan yer /////////////////


EntryA = tk.Entry(frame, width=20,bg="#ADD8E6")
EntryA.pack(side=tk.LEFT)




#/////////////////////////////////// frame adları
canvasA = None
canvasB = None
canvasFark = None

grafik_frame1 = tk.Frame(scrollable_frame)
grafik_frame1.pack(pady=10, fill=tk.BOTH, expand=True)

grafik_frame2 = tk.Frame(scrollable_frame)
grafik_frame2.pack(pady=10, fill=tk.BOTH, expand=True)

grafik_frame_fark = tk.Frame(scrollable_frame)
grafik_frame_fark.pack(pady=10, fill=tk.BOTH, expand=True)
#////////////////////////////////////////////////////////////////

global_data = None
global_data_iki= None


filename = ""
filename2 = ""


def veri_kaydet1():
   
    global global_data, filename
    s.sendall(b'ACQ:START\r\n')   # here is special for your cards 

    #//////////////////////////////////////////////////////////
    komut = 'ACQ:SOUR1:DATA?\r\n'   # here is so special for your card read from card documents 

    s.sendall(komut.encode('utf-8'))
    response = s.recv(524288)
   
    time.sleep(0.2)  # 200ms bekle

   
    komut = 'ACQ:SOUR1:DATA?\r\n'
    s.sendall(komut.encode('utf-8'))
    response = s.recv(524288)
    #///////////////////////////////////////////////////////
   
    data = response.decode('utf-8')
    global_data = list(data[1:-3].split(','))
   
    #masaütünekaydet
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop") #  1.masausut yolu


    filename = EntryA.get() + ".xlsx"
   
   
    filepath = os.path.join(desktop_path, filename) #   2.   masasustu yolu degişken degişti
   


    df = pd.DataFrame(global_data, columns=['Veri'])
   
#  //////       sayı olmayanları boş yapar

    df['Veri'] = pd.to_numeric(df['Veri'], errors='coerce')
    df = df.dropna()

   
    df.to_excel(filepath, header=False, index=False)   # filepath ı filenmae yaprsan eski yerien kaydeder filepath
                                                        #yaparsan eski yerine kaydeder
   
    print(f"{filename} dosyasına kaydedildi.")
    print(f"{filepath} dosyasına kaydedildi.")

   
   

def grafik_ciz1():
    global canvasA

   

    df = pd.DataFrame(global_data, columns=['Veri'])
    df['Veri'] = pd.to_numeric(df['Veri'], errors='coerce')
    df = df.dropna()
   
   
    ortalama = df['Veri'].mean()

   
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df.index, df['Veri'], label="Kanal 1 Verisi")

    ax.axhline(y=ortalama, color='red', linestyle='--', label=f'Ortalama: {ortalama:.6f}')

   
   
   
#grafik resim olarak kaydet
    #plt.savefig(f"{filename}.jpg")
    # filename = EntryA.get() + ".xlsx"   böyle neden olmadı

   


   
   
   
    ax.legend()

    if canvasA:
        canvasA.get_tk_widget().destroy()

    canvasA = FigureCanvasTkAgg(fig, master=grafik_frame1)
    canvasA.draw()
    canvasA.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    s.sendall(b'ACQ:STOP\r\n')

#//////////////////////////////////////////////////////////////
#                 ikinci

def resim1_save():
    plt.savefig(f"{filename}.jpg")






def veri_kaydet_2():
   
    global global_data_iki, filename2
   
   
    s.sendall(b'ACQ:START\r\n')
   
    """
   
   
    komut = 'ACQ:SOUR2:DATA?\r\n'
    s.sendall(komut.encode('utf-8'))
    responseB = s.recv(524288)
   
    """
   
    komut = 'ACQ:SOUR2:DATA?\r\n'
    s.sendall(komut.encode('utf-8'))
    responseB = s.recv(524288)
   
    data = responseB.decode('utf-8')
   
     # Veriyi ayır ve sadece 1'den küçük olanları filtrele
       
    filtered_data = []
    for halil_ibrahim in data[2:-3].split(','):
        try:
            value = float(halil_ibrahim)
            if value < 1:
                filtered_data.append(value)
        except ValueError:
            continue

           
           

    global_data_iki = filtered_data
   
    filename2 = EntryA.get()+"a2.xlsx"  #excel ismi
   

    df = pd.DataFrame(global_data_iki, columns=['Veri'])
   
#  /       sayı olmayanları boş yapar
    df['Veri'] = pd.to_numeric(df['Veri'], errors='coerce')
    df = df.dropna()

    df.to_excel(filename2, header=False, index=False)
    print(f"{filename2} dosyasına kaydedildi.")

   
   
def grafik_ciz_2():
    global canvasB

    df = pd.DataFrame(global_data_iki, columns=['Veri'])
    df['Veri'] = pd.to_numeric(df['Veri'], errors='coerce')
    #burda verierl df['Veri'] ye aldık
    df = df.dropna()
   
    ortalama = df['Veri'].mean()

   
#/////////////////  isim   //////////////////////////////////////////

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df.index, df['Veri'], label="  input 2 ")  # <-- Label eklendi
   
    ax.axhline(y=ortalama, color='red', linestyle='--', label=f'Ortalama: {ortalama:.6f}')

    #resim kaydetme
   # plt.savefig(f"{filename2}.jpg")

   
   
    ax.legend()  # <-- Legend gösterildi
#///////////////////////////////////////////////

    if canvasB:
        canvasB.get_tk_widget().destroy()

    canvasB = FigureCanvasTkAgg(fig, master=grafik_frame2)
    canvasB.draw()
    canvasB.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    s.sendall(b'ACQ:STOP\r\n')

   
def resim1_save_2():
     plt.savefig(f"{filename2}.jpg")

   

   

   

canvasFark = None  # global olarak en başa ekle

def fark():
    global canvasFark

    df1 = pd.read_excel(filename, header=None)
    df2 = pd.read_excel(filename2, header=None)

    df1 = df1.dropna()
    df2 = df2.dropna()

    min_length = min(len(df1), len(df2))
    df1 = df1.iloc[:min_length]
    df2 = df2.iloc[:min_length]

    fark_df = df1[0] - df2[0]
   
    ortalama_fark = fark_df.mean()

   

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(fark_df.index, fark_df, label="Fark")
   
    ax.axhline(y=ortalama_fark, color='red', linestyle='--', label=f'Ortalama_fark: {ortalama_fark:.6f}')

    #resim kaydetme
   
    plt.savefig(f"{filename}resim.jpg")
   
    ax.legend()

    if canvasFark:
        canvasFark.get_tk_widget().destroy()

    canvasFark = FigureCanvasTkAgg(fig, master=grafik_frame_fark)
    canvasFark.draw()
    canvasFark.get_tk_widget().pack(fill=tk.BOTH, expand=True)
   
   
   
   
def fark_yeni():
    global canvasFark

    # Öncelikle global_data ve global_data_iki'den veri alalım
    if global_data is not None and global_data_iki is not None:
        # global_data ve global_data_iki listeler, DataFrame yapalım
        df1 = pd.DataFrame(global_data)
        df2 = pd.DataFrame(global_data_iki)

        # Sayısal veriye çevir
        df1[0] = pd.to_numeric(df1[0], errors='coerce')
        df2[0] = pd.to_numeric(df2[0], errors='coerce')

        # NaN olanları çıkar
        df1 = df1.dropna()
        df2 = df2.dropna()
    else:
        # Eğer global_data yoksa, dosyalardan oku (varsa)
        try:
            df1 = pd.read_excel(filename, header=None).dropna()
            df2 = pd.read_excel(filename2, header=None).dropna()
        except Exception as e:
            print("Veri yok ya da dosyalar okunamadı:", e)
            return

    # Veri uzunluklarını eşitle
    min_length = min(len(df1), len(df2))
    df1 = df1.iloc[:min_length]
    df2 = df2.iloc[:min_length]

    fark_df = df1[0] - df2[0]

    ortalama_fark = fark_df.mean()

   
   
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(fark_df.index, fark_df, label="Fark_yeni_güncel")
   
    ax.axhline(y=ortalama_fark, color='red', linestyle='--', label=f'Ortalama_fark: {ortalama_fark:.6f}')
#resim kaydet
   # plt.savefig(f"{filename} resimyeni .jpg")

    ax.legend()

    if canvasFark:
        canvasFark.get_tk_widget().destroy()

    canvasFark = FigureCanvasTkAgg(fig, master=grafik_frame_fark)
    canvasFark.draw()
    canvasFark.get_tk_widget().pack(fill=tk.BOTH, expand=True)
   
def resim_fark():
    plt.savefig(f"{filename} resimyeni .jpg")

   
   

def kapa():
    s.close()


#buton çerçeve
buttons_frame = tk.Frame(scrollable_frame)
buttons_frame.pack(pady=10)
   
   
   
# Butonlar

# 1.
button_kaydet1 = tk.Button(buttons_frame, text="Veri Kaydet 1", command=veri_kaydet1, width=15, height=2)
button_kaydet1.grid(row=0, column=0, pady=5)

button_grafik1 = tk.Button(buttons_frame, text="Grafik Göster 1", command=grafik_ciz1, width=15, height=2)
button_grafik1.grid(row=1, column=0, pady=5)

button_resim1_save = tk.Button(buttons_frame, text="resim1_save1", command=resim1_save, width=15, height=2)
button_resim1_save.grid(row=2, column=0, pady=5)



#2.
button_kaydet2 = tk.Button(buttons_frame, text="Veri Kaydet 2", command=veri_kaydet_2, width=15, height=2)
button_kaydet2.grid(row=0, column=1, padx=10, pady=5)

button_grafik2 = tk.Button(buttons_frame, text="Grafik Göster 2", command=grafik_ciz_2, width=15, height=2)
button_grafik2.grid(row=1, column=1, padx=10, pady=5)

button_resim2_save = tk.Button(buttons_frame, text="resim2_save2", command=resim1_save_2, width=15, height=2)
button_resim2_save.grid(row=2, column=1, padx=10, pady=5)


#button_fark = tk.Button(scrollable_frame, text="Fark Grafiği", command=fark, width=15, height=2)
#button_fark.pack(pady=5)

# fark_yeni
button_fark_yeni = tk.Button(buttons_frame, text="Grafiği yeni", command=fark_yeni, width=15, height=2)
button_fark_yeni.grid(row=0, column=2, padx=10, pady=5)

button_resim_fark = tk.Button(buttons_frame, text="kaydet fark", command=resim_fark, width=15, height=2)
button_resim_fark.grid(row=1, column=2, padx=10, pady=5)


# pady padx  sag sol boşul yeri

button_kapa = tk.Button(buttons_frame, text="close", command=kapa, width=15, height=2)
button_kapa.grid(row=2, column=2, padx=10, pady=5)


scrollable_frame.mainloop()
