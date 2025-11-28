# zembil

- **zembil** projesini güncel gelişmelere göre yeniliyoruz.
- Öncelikle Zemberek'in en son zemberek-full-0.17.2.jar sürümünü kullanacağız.
Eğer kendi jar dosyanızı oluşturmak isterseniz https://github.com/ahmetaa/zemberek-nlp adresindeki projeyi klonlayın, sonra da oradaki açıklamaları izleyerek Maven üzerinden kendi sürümünüzü derleyin.

zemberek_interaktif.py betiğini kullanarak Türkçe sözcükleri analiz edebilirsiniz.

1. Bu repoyu klonla:

   ```bash
   cd github
   git clone https://github.com/ahmetax/zembil.git
   cd zembil
   ```
   Sanal ortam kullanmanızı öneririm: (Aşağıdaki kodlar Ubuntu 24.04 içindir. Kendi sisteminize göre uyarlayın.)
   
   ```bash
   python3.12 -m venv e312
   source e312/bin/activate
   ```
2. Gerekli kütüphaneleri kurun:

   ```bash
   pip install jpype1
   ```
3. zemberek_interaktif.py betiğini kullanmak için aşağıdaki komutu verin:

   ```bash
   python zemberek_interaktif.py
   ```

Benim kullandığım python sürümü 3.12'dir. Fakat daha yeni sürümleri de kullanabilirsiniz.


