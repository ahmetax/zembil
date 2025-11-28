# kelime_analiz_interaktif_log.py - Düzeltilmiş Versiyon
#
# Zemberek ile interaktif kelime analizi ve LOG dosyasına kaydetme
# Sonuçlar ekranda gösterilirken aynı zamanda 'zemberek_analiz_log.txt' dosyasına eklenir.
# Gemini - Zemberek ile İnteraktif Kelime Analizi

import signal
import sys
from jpype import startJVM, getDefaultJVMPath, JClass, JString, shutdownJVM
import os
from typing import List, Tuple
from datetime import datetime

# --- Yapılandırma ---
LOG_FILE_NAME = "zemberek_analiz_log.txt"
ZEMBEREK_PATH = os.path.abspath('zemberek-full-0.17.2.jar')
# ---------------------

# Custom Exception for Timeout
class TimeoutException(Exception):
    pass

# Signal Handler function: Zaman aşımı sinyalini yakalar
def signal_handler(signum, frame):
    """Bu fonksiyon, alarm çaldığında (zaman aşımı) çağrılır."""
    raise TimeoutException("Zemberek Analiz Zaman Aşımı (Timeout)")

# Global değişkenler
morphology = None
TurkishMorphology = None

def setup_jvm():
    """JVM'yi başlatır ve Zemberek'i hazırlar."""
    global morphology, TurkishMorphology
    if morphology is None:
        try:
            print("\n⏳ Zemberek JVM başlatılıyor ve morfoloji yükleniyor...")
            startJVM(getDefaultJVMPath(), '-ea', f'-Djava.class.path={ZEMBEREK_PATH}', '-Xmx4g') 
            TurkishMorphology = JClass('zemberek.morphology.TurkishMorphology')
            morphology = TurkishMorphology.createWithDefaults()
            print("✅ Zemberek başarıyla hazırlandı.")
        except Exception as e:
            print(f"\n❌ KRİTİK HATA: Zemberek başlatılamadı. Hata: {e}")
            print("Lütfen 'zemberek-full.jar' dosyasının mevcut olduğundan emin olun.")
            sys.exit(1)


def shutdown_jvm():
    """JVM'yi kapatır."""
    global morphology
    if morphology is not None:
        print("\n👋 Zemberek JVM kapatılıyor...")
        shutdownJVM()
        morphology = None

def format_morphemes(analysis):
    """Ekleri (iyor-um) formatında çıkarır."""
    morpheme_data_list = analysis.getMorphemeDataList()
    if morpheme_data_list.size() <= 1: 
        return ""
    surface_forms = [str(morpheme_data_list.get(i).surface) for i in range(1, morpheme_data_list.size())]
    return f"({'-'.join(surface_forms)})"


def analyze_word_safe(word: str) -> Tuple:
    """Tek bir kelimeyi 5 saniye zaman aşımı ile analiz eder."""
    
    if word.startswith("acıtıyor"):
        return (word, word, "", "", "ATLANDI: acıtıyor kuralı", "atlandı")

    try:
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(5) # 5 saniye zaman aşımı
        
        j_word = JString(word)
        analysis = morphology.analyze(j_word) 
        
        signal.alarm(0) 

        results = analysis.getAnalysisResults()
        
        if results.isEmpty():
            return (word, word, "", "", "Analiz yok", "zemberek")
        
        best_result = results.get(0)
        
        lemma = str(best_result.getLemmas()[0])
        kok = str(best_result.getStems()[0])
        ekler = format_morphemes(best_result)
        analiz_tam = str(best_result.formatLong())
        yontem = "zemberek"
        
        return (word, lemma, kok, ekler, analiz_tam, yontem)

    except TimeoutException:
        print(f"\n⚠️ HATA: '{word}' kelimesi 5 saniyede analiz edilemedi (TIMEOUT).")
        return (word, word, "", "", f"HATA: TIMEOUT (5s)", "zemberek_hata")

    except Exception as e:
        print(f"\n❌ HATA: '{word}' kelimesi analizde çöktü. Hata: {e}")
        return (word, word, "", "", f"HATA: {e}", "zemberek_hata")
    
    finally:
         signal.alarm(0) 


def analyze_batch(words: List[str]) -> List[Tuple]:
    """Kelimelerin listesini alır ve analyze_word_safe fonksiyonunu kullanarak analiz eder."""
    if morphology is None:
        raise Exception("Zemberek morfolojisi başlatılmamış.")
        
    results_list = []
    
    for word in words:
        result = analyze_word_safe(word.strip())
        results_list.append(result)
        
    return results_list


def print_and_log_results(results: List[Tuple], log_file: str):
    """Analiz sonuçlarını ekrana ve belirtilen log dosyasına yazar."""
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ekrana yazma için başlıklar
    screen_output = "\n" + "="*80 + "\n"
    screen_output += f"Kelime Analiz Sonuçları ({current_time})\n"
    screen_output += "-"*80 + "\n"
    screen_output += f"{'Kelime':<18} | {'Kök':<15} | {'Ekler':<15} | {'Lemma':<15} | {'Durum':<10}\n"
    screen_output += "-"*80 + "\n"
    
    # Log dosyasına yazma için başlıklar
    log_output = "\n" + "#"*100 + "\n"
    log_output += f"### ANALİZ BAŞLANGIÇ ZAMANI: {current_time} ###\n"
    log_output += f"{'Kelime':<25} | {'Lemma':<25} | {'Kök':<25} | {'Ekler':<25} | {'Durum':<10} | {'Tam Analiz/Hata Mesajı'}\n"
    log_output += "-"*160 + "\n"
    
    
    # Sonuçları işleme
    for word, lemma, kok, ekler, analiz_tam, yontem in results:
        durum = "OK"
        
        # Analiz tam metnindeki satır sonu karakterlerini (backslash içerir) f-string dışında temizle
        cleaned_analiz_tam = analiz_tam.replace('\n', ' ').strip()
        
        if yontem.endswith("hata"):
            durum = "HATA"
            
            # Ekrana Hata Mesajı
            screen_output += f"**{word:<18} | {'':<15} | {'':<15} | {'':<15} | {durum:<10}**\n"
            screen_output += f"TAM HATA MESAJI: {analiz_tam}\n"
            
            # Log Dosyasına Hata Mesajı (Tam Analiz sütununa yazılır)
            log_output += f"{word:<25} | {lemma:<25} | {kok:<25} | {ekler:<25} | {durum:<10} | {cleaned_analiz_tam}\n"
            
        elif yontem == "atlandı":
            durum = "ATLANDI"
            
            # Ekrana Atlandı Mesajı
            screen_output += f"**{word:<18} | {'':<15} | {'':<15} | {'':<15} | {durum:<10}**\n"
            
            # Log Dosyasına Atlandı Mesajı
            log_output += f"{word:<25} | {lemma:<25} | {kok:<25} | {ekler:<25} | {durum:<10} | {cleaned_analiz_tam}\n"
            
        else:
            # Normal analiz sonucu
            screen_output += f"{word:<18} | {kok:<15} | {ekler:<15} | {lemma:<15} | {durum:<10}\n"
            
            # Log Dosyasına Normal Analiz Sonucu
            log_output += f"{word:<25} | {lemma:<25} | {kok:<25} | {ekler:<25} | {durum:<10} | {cleaned_analiz_tam}\n"

    screen_output += "="*80 + "\n"
    log_output += "-"*160 + "\n"
    
    # Log dosyasını APPEND (ekleme) modunda aç ve yaz
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_output)
        print(f"✅ Sonuçlar {log_file} dosyasına başarıyla kaydedildi.")
    except Exception as e:
        print(f"\n❌ KRİTİK LOG HATASI: Sonuçlar {log_file} dosyasına yazılamadı. Hata: {e}")
        
    # Ekrana yaz
    print(screen_output)


def interactive_mode():
    """Kullanıcıdan girdi alarak sürekli analiz yapan ana döngü."""
    
    while True:
        user_input = input("❓ Analiz edilecek kelime(ler)i girin (Çıkmak için 'EXIT'):\n> ").strip().lower()
        
        if user_input == "exit":
            break
        
        if not user_input:
            continue
            
        words_to_analyze = [w.strip() for w in user_input.split() if w.strip()]
        
        if words_to_analyze:
            print("... Analiz yapılıyor, lütfen bekleyin...")
            # Analizi gerçekleştir
            results = analyze_batch(words_to_analyze)
            
            # Sonuçları ekrana bas ve LOG dosyasına kaydet
            print_and_log_results(results, LOG_FILE_NAME)


if __name__ == "__main__":
    
    print("==============================================")
    print("      Zemberek İnteraktif Kelime Analiz       ")
    print("      (Sonuçlar LOG dosyasına kaydediliyor)   ")
    print("==============================================")
    
    # JVM'yi başlat ve Zemberek'i hazırla
    setup_jvm()
    
    # İnteraktif modu başlat
    interactive_mode()
    
    # İşlem bittiğinde JVM'yi kapat
    shutdown_jvm()
    
    print("Uygulama başarıyla kapatıldı.")
