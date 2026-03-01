<img width="1856" height="912" alt="image" src="https://github.com/user-attachments/assets/d50fd1c2-84d5-4269-8911-2f0291bcfe92" />
<img width="1870" height="907" alt="image" src="https://github.com/user-attachments/assets/4008b7ff-5137-48a6-9ff7-6ab01ed2f70c" />


# 🧺 Melisa'nın Mutfağı

> Aile için tasarlanmış, akıllı ve kullanımı kolay bir alışveriş listesi uygulaması.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?style=flat-square&logo=flask)
![License](https://img.shields.io/badge/Lisans-MIT-green?style=flat-square)

---

## 📸 Özellikler

| Özellik | Açıklama |
|---|---|
| ✅ Ürün Seçimi | Kategorilere göre düzenlenmiş ürün listesi, checkbox ile seçim |
| ➕ Ürün Ekle / Sil | Excel tablosuna kalıcı olarak yeni ürün ekle veya mevcut ürünü sil |
| 🔢 Miktar & Birim | Her ürüne miktar (+/−) ve birim (Kg, Adet, Paket…) ayarla |
| ♥ Favoriler | Sık kullandığın ürünleri favorile, tek sekmede gör |
| 🔍 Arama | Tüm kategorilerde anlık ürün arama |
| 💾 Otomatik Kayıt | Checkbox, miktar veya birim değiştiğinde liste sunucuya otomatik kaydolur |
| 📋 Geçmiş Listeler | Her kaydedilen listeye isim ver, sonra görüntüle veya geri yükle |
| 📦 Stok Takibi | Her ürüne ✅ Var / ⚠️ Azalıyor / ❌ Yok durumu ata, uyarı al |
| 👨‍🍳 Tarife Göre Alışveriş | Yemek adı yaz, Claude AI malzeme listesini otomatik oluştursun |
| 🖨️ Yazdır | Seçili ürünleri kategoriye göre sıralı, logolu çıktı al |
| 💬 Hoşgeldin Mesajları | Her açılışta farklı, kişisel bir karşılama mesajı |

---

## 🚀 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- pip

### Adımlar

```bash
# 1. Repoyu klonla
git clone https://github.com/kullanici-adin/melisanin-mutfagi.git
cd melisanin-mutfagi

# 2. Bağımlılıkları yükle
pip install flask pandas openpyxl

# 3. Uygulamayı başlat
python app.py
```

Tarayıcıda `http://localhost:5000` adresini aç.

---

## 📁 Dosya Yapısı

```
melisanin-mutfagi/
│
├── app.py                        # Flask backend — tüm API endpoint'leri
├── alisveris_listesi.xlsx        # Ürün veritabanı (Excel, sayfalar = kategoriler)
├── melisaninmutfagilogo.png      # Uygulama logosu
│
├── templates/
│   └── index.html                # Tek sayfa frontend (HTML + CSS + JS)
│
├── secimler.json                 # Seçili ürünler (otomatik oluşur)
├── favoriler.json                # Favori ürün ID'leri (otomatik oluşur)
├── gecmis_listeler.json          # Kaydedilmiş geçmiş listeler (otomatik oluşur)
└── stok_durumu.json              # Ürün stok durumları (otomatik oluşur)
```

> `index.html` dosyasını `templates/` klasörüne koy. JSON dosyaları ilk çalıştırmada otomatik oluşur.

---

## 🗂️ Excel Yapısı

`alisveris_listesi.xlsx` dosyasında her sayfa bir kategoridir.  
Her sayfada şu sütunlar bulunur:

| Sütun | Açıklama | Örnek |
|---|---|---|
| `ID` | Benzersiz ürün kodu | `MS01` |
| `Alt Kategori` | Ürün alt grubu | `Yaprak Sebzeler` |
| `Ürün Adı` | Ürünün adı | `Ispanak` |
| `Varsayılan Birim` | Varsayılan ölçü birimi | `Kg` |
| `Notlar` | İsteğe bağlı açıklama | `Taze tercih et` |

Desteklenen kategoriler: `Meyve ve Sebze`, `Et ve Tavuk`, `Süt ve Süt Ürünleri`, `Temel Gıda`, `İçecek`, `Temizlik Malzemesi`, `Fırın ve Pasta`

Yeni kategori eklemek için Excel dosyasına yeni bir sayfa eklemeniz yeterli, uygulama onu otomatik olarak algılar.

---

## 🔌 API Endpoint'leri

| Method | Endpoint | Açıklama |
|---|---|---|
| `GET` | `/` | Ana sayfa |
| `GET` | `/logo` | Logo dosyasını serve et |
| `POST` | `/kaydet` | Seçili ürünleri kaydet |
| `GET` | `/gecmis` | Geçmiş listeleri getir |
| `POST` | `/gecmis-yukle` | Geçmiş listeyi yükle |
| `POST` | `/gecmis-sil` | Geçmiş kaydı sil |
| `POST` | `/stok-guncelle` | Ürün stok durumunu güncelle |
| `GET` | `/stok-uyari` | Azalan/biten ürünleri listele |
| `POST` | `/favori-guncelle` | Favori ekle/çıkar |
| `POST` | `/urun-ekle` | Yeni ürün ekle |
| `POST` | `/urun-sil` | Ürün sil |
| `POST` | `/liste-temizle` | Tüm seçimleri sıfırla |
| `GET` | `/alt-kategoriler/<kategori>` | Kategorinin alt gruplarını getir |

---

## 🛠️ Kullanılan Teknolojiler

**Backend**
- [Flask](https://flask.palletsprojects.com/) — Python web framework
- [Pandas](https://pandas.pydata.org/) — Excel okuma/yazma
- [OpenPyXL](https://openpyxl.readthedocs.io/) — Excel engine

**Frontend**
- Vanilla JavaScript (framework yok)
- CSS Custom Properties ile tasarım sistemi
- [DM Sans + DM Serif Display](https://fonts.google.com/) — Google Fonts

**AI**
- [Anthropic Claude API](https://www.anthropic.com/) — Tarife göre alışveriş önerisi

---

## 📄 Lisans

MIT License — dilediğin gibi kullanabilirsin.

---

<p align="center">
  Sevgiyle yapıldı 🧡
</p>
