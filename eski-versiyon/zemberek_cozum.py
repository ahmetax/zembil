# -*- coding: utf-8 -*-
# zemberek_cozum.py
"""
Kod   : Ahmet Aksoy
Sistem: Ubuntu 16.04 LTS
Python: Python 3.6.3
Modül : JPype1-py3 0.5.5.2
Java  : zemberek-tum-2.0.jar
"""
import jpype
def zemberek_baslat():
    global zemberek, Zemberek
    # JVM başlat
    # Aşağıdaki adresleri java sürümünüze ve jar dosyasının bulunduğu klasöre göre değiştirin
    jpype.startJVM("/usr/lib/jvm/java-8-oracle/jre/lib/amd64/server/libjvm.so",
             "-Djava.class.path=zemberek-tum-2.0.jar", "-ea")
    # Türkiye Türkçesine göre çözümlemek için gerekli sınıfı hazırla
    Tr = jpype.JClass("net.zemberek.tr.yapi.TurkiyeTurkcesi")
    # tr nesnesini oluştur
    tr = Tr()
    # Zemberek sınıfını yükle
    Zemberek = jpype.JClass("net.zemberek.erisim.Zemberek")
    # zemberek nesnesini oluştur
    zemberek = Zemberek(tr)

def zemberek_coz(kelime):
    if isinstance(zemberek, Zemberek)==False:
        zemberek_baslat()
    if kelime.strip()>'':
        return zemberek.kelimeCozumle(kelime)

def ana():
    zemberek_baslat()
    #Çözümlenecek örnek kelimeleri belirle
    kelimeler = ["iştahlı","iştahsız","süreğen","sergüzeşt"]
    print(type(zemberek))
    for kelime in kelimeler:
        if kelime.strip()>'':
            #yanit = zemberek.kelimeCozumle(kelime)
            yanit = zemberek_coz(kelime)
            if yanit:
                print("{}".format(yanit[0]))
            else:
                print("{} ÇÖZÜMLENEMEDİ".format(kelime))

    zemberek_kapat()

def zemberek_kapat():
    #JVM kapat
    jpype.shutdownJVM()

if __name__ == "__main__":
    ana()
