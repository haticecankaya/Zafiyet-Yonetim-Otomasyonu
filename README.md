# Zafiyet Yönetim Otomasyonu (Vulnerability Management Automation)

Bu proje, JSON formatındaki zafiyet tarama raporlarını analiz eden, EPSS ve CISA KEV verileriyle risk skorlaması yapan ve Jira üzerinde otomatik bilet (ticket) açan bir siber güvenlik aracıdır.

## 🚀 Özellikler
* **Otomatik Ayrıştırma:** JSON tarama çıktılarını işler.
* **Risk Analizi:** CVSS, EPSS ve CISA KEV verilerine göre dinamik skorlama.
* **Entegrasyon:** Jira REST API ile otomatik görev oluşturma.
* **Güvenlik:** STRIDE tehdit modeline uygun mimari.

## 🛠️ Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone [https://github.com/KULLANICI_ADIN/REPO_ADIN.git](https://github.com/KULLANICI_ADIN/REPO_ADIN.git)
   cd REPO_ADIN
   ```

2. Gereksinimleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. Veri Setlerini yükleyin
Bu proje, boyutları nedeniyle GitHub deposuna yüklenmemiş olan harici veri setlerine ihtiyaç duyar. Projeyi çalıştırmadan önce aşağıdaki adımları takip ederek veri setlerini manuel olarak eklemelisiniz:
Proje ana dizininde **`data`** adında yeni bir klasör oluşturun.
Aşağıdaki Kaggle bağlantısından gerekli veri setlerini indirin:
    * 🔗 [Vulnerability Management Datasets (Kaggle)](https://www.kaggle.com/datasets/francescomanzoni/vulnerability-management-datasets)
İndirdiğiniz arşivden çıkan aşağıdaki iki CSV dosyasını oluşturduğunuz `data/` klasörüne kopyalayın:
    * `cve_corpus.csv`
    * `cve_cisa_epss_enriched_dataset.csv`
⚠️ **Önemli Not:** Kodun hatasız çalışması için dosya isimlerinin yukarıdaki gibi olduğundan ve dosyaların `data/` klasörü içinde yer aldığından emin olunuz.
 
4. Uygulamayı başlatın:
   ```bash
   streamlit run main.py
   

## 🧪 Testler
Projedeki birim testleri çalıştırmak için:
```bash
pytest
