# zembil.py
# Kod   : Ahmet Aksoy
# Sistem: Ubuntu 16.04 LTS
# Python: Python 3.6.3
# Modül : JPype1-py3 0.5.5.2
# Java  : zemberek-tum-2.0.jar
# Tarih : 04.12.2017
# Son   : 26.03.2018
# Sürüm : 0.0.0

from tkinter import *
from tkinter import ttk
from zemberek_cozum import *

"""
Bu projede zemberek jar dosyasını kullanarak sözcük çözümlemeyi
komut modu yerine bir masaüstü uygulaması ile sağlıyoruz.
Görsel arayüz sistemi olarak tkinter kullandım. Bu sistem
ayrıntılı örnekler açısından biraz zayıf görünse de, Python'un
yeni sürümleriyle uyumu önemli bir avantaj sağlıyor.
"""

class Zembil():
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("zembil.py")

        self.anaCerceve = ttk.Frame(self.parent, padding=(3, 3, 12, 12))
        self.anaCerceve.grid(row=0, column=0, sticky=(N,S,E,W))

        self.ebeveyn=self.anaCerceve

        self.cerceve2 = Frame(self.ebeveyn)
        self.cerceve2.pack(side=TOP, fill=X, ipady=2)

        style = ttk.Style()
        style.configure('TButton', borderwidth=1,
                        relief="groove"
                        )
        style.configure('Normal.TButton', foreground="black")
        self.b0 = Button(self.cerceve2, text="Temizle ", command=self.temizle)
        self.b1 = Button(self.cerceve2, text="Zemberek", command=self.zemberek)
        self.b0.pack(side=LEFT)
        self.b1.pack(side=LEFT)

        self.cerceve4 = ttk.Frame(self.ebeveyn)
        self.cerceve4.pack(fill=BOTH, expand=1)

        self.detayKutusu = Text(self.cerceve4, height=60)
        self.detayKutusu.config(wrap=WORD)

        self.vscroll = ttk.Scrollbar(self.detayKutusu, orient=VERTICAL,
                                 command = self.detayKutusu.yview)
        self.detayKutusu['yscroll']=self.vscroll.set
        self.vscroll.pack(side=RIGHT, fill=Y)
        self.detayKutusu.pack(fill=BOTH, expand=1)

        self.detayKutusu.insert(END, "deneme")

        self.yanCerceve = ttk.Frame(self.parent, padding=(3, 3, 12, 12))
        self.yanCerceve.grid(row=1, column=0, sticky=(N,S,E,W))
        # ttk.Label(self.yanCerceve, text=" Rapor Alanı").pack()

        self.raporKutusu = Text(self.yanCerceve, height=60, width=60)
        self.raporKutusu.pack(fill=BOTH, expand=1)
        self.raporKutusu.config(wrap=WORD, width=60)

        self.vscroll2 = ttk.Scrollbar(self.raporKutusu, orient=VERTICAL,
                                 command = self.raporKutusu.yview)
        self.raporKutusu['yscroll']=self.vscroll2.set
        self.vscroll2.pack(side=RIGHT, fill=Y)
        self.raporKutusu.insert(END,"rapor deneme")

        self.parent.grid_columnconfigure(0, minsize =400, weight=1)
        #self.parent.grid_columnconfigure(1, minsize =300, weight=1)
        self.parent.grid_rowconfigure(0, minsize =200, weight=1)
        self.parent.grid_rowconfigure(1, minsize =200, weight=1)

    def zemberek(self):
        # kelimeleri ayır ve çözümle
        metin = self.detayKutusu.get("1.0", END)
        kelimeler = list(set(metin.split()))
        if len(kelimeler)>0:
            for kelime in kelimeler:
                yanit = zemberek_coz(kelime)
                if yanit:
                    s = str(yanit[0])
                    sat = s.strip()
                    icerik = re.findall("({.+})", sat)
                    ekler = sat[len(icerik[0]):]
                    icerik = icerik[0].split(' ')
                    kelime = icerik[1]
                    kok = icerik[3]
                    tip = icerik[4][4:-1]
                    ekler = ekler[8:]
                    s="({} - {} - {}) : {}".format(kelime, kok, tip, ekler)

                    self.raporKutusu.insert("end", s)
                    self.raporKutusu.insert("end", "\n")
                else:
                    pass

    def temizle(self):
        self.detayKutusu.delete("1.0", END)
        self.raporKutusu.delete("1.0", END)

    def aramaSil(self):
        self.aramaVar.set('')
        self.detayKutusu.tag_remove('bulundu', '1.0', END)

    def aramaYap(self, ne=None):
        self.aranacak=self.aramaVar.get()
        self.metin = self.detayKutusu.get("1.0", END)
        self.detayKutusu.tag_remove('bulundu', '1.0', END)

        if self.aranacak:
            endeks = '1.0'
            while 1:
                endeks = self.detayKutusu.search(self.aranacak, endeks, nocase=1, stopindex=END)
                if not endeks: break
                sonendeks = f"{endeks}+{len(self.aranacak)}c"
                print(sonendeks)
                self.detayKutusu.tag_add('bulundu', endeks, sonendeks)
                endeks = sonendeks
            self.detayKutusu.tag_config('bulundu', foreground='red')
        self.arama.focus_set(  )

    def bos(self):
        pass


def main():
    root = Tk()
    zemberek_baslat()
    Zembil(root)
    root.mainloop()
    zemberek_kapat()

if __name__ == "__main__":
    main()
