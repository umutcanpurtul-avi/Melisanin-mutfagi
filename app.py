from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import json
import os
from datetime import datetime

app = Flask(__name__)
EXCEL_FILE = 'alisveris_listesi.xlsx'
DATA_FILE = 'secimler.json'
FAV_FILE = 'favoriler.json'
GECMIS_FILE = 'gecmis_listeler.json'
STOK_FILE = 'stok_durumu.json'

KATEGORI_IKONLARI = {
    'Meyve ve Sebze': '🥦',
    'Et ve Tavuk': '🥩',
    'Süt ve Süt Ürünleri': '🧀',
    'Temel Gıda': '🌾',
    'İçecek': '🧃',
    'Temizlik Malzemesi': '🧹',
    'Fırın ve Pasta': '🍞',
}

def excel_oku():
    return pd.read_excel(EXCEL_FILE, sheet_name=None)

def secimleri_getir():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def favorileri_getir():
    if os.path.exists(FAV_FILE):
        with open(FAV_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def gecmis_getir():
    if os.path.exists(GECMIS_FILE):
        with open(GECMIS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def stok_getir():
    if os.path.exists(STOK_FILE):
        with open(STOK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

@app.route('/')
def index():
    try:
        veriler = excel_oku()
        kategoriler = list(veriler.keys())
        kayitli_secimler = secimleri_getir()
        favoriler = favorileri_getir()
        stok = stok_getir()
        return render_template('index.html',
                               veriler=veriler,
                               kategoriler=kategoriler,
                               secimler=kayitli_secimler,
                               favoriler=favoriler,
                               stok=stok,
                               ikonlar=KATEGORI_IKONLARI)
    except Exception as e:
        return f"Hata: {e}. Excel dosyasını kontrol et."

@app.route('/logo')
def serve_logo():
    for fname in ['melisaninmutfagilogo.png', 'logo.png']:
        if os.path.exists(fname):
            return send_from_directory('.', fname)
    return '', 404

@app.route('/kaydet', methods=['POST'])
def kaydet():
    secilenler = request.json.get('secilenler', {})
    isim = request.json.get('isim', '')
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(secilenler, f, ensure_ascii=False)
    
    # Geçmişe kaydet (eğer ürün varsa)
    if secilenler:
        gecmis = gecmis_getir()
        simdi = datetime.now()
        yeni_kayit = {
            'id': simdi.strftime('%Y%m%d_%H%M%S'),
            'tarih': simdi.strftime('%d.%m.%Y'),
            'saat': simdi.strftime('%H:%M'),
            'isim': isim or simdi.strftime('%d %B %Y'),
            'urun_sayisi': len(secilenler),
            'liste': secilenler
        }
        gecmis.insert(0, yeni_kayit)
        gecmis = gecmis[:20]  # Son 20 listeyi tut
        with open(GECMIS_FILE, 'w', encoding='utf-8') as f:
            json.dump(gecmis, f, ensure_ascii=False)
    
    return jsonify({"status": "success"})

@app.route('/gecmis', methods=['GET'])
def gecmis_listele():
    return jsonify(gecmis_getir())

@app.route('/gecmis-yukle', methods=['POST'])
def gecmis_yukle():
    kayit_id = request.json.get('id')
    gecmis = gecmis_getir()
    kayit = next((k for k in gecmis if k['id'] == kayit_id), None)
    if not kayit:
        return jsonify({"status": "error", "message": "Kayıt bulunamadı"}), 404
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(kayit['liste'], f, ensure_ascii=False)
    return jsonify({"status": "success", "liste": kayit['liste']})

@app.route('/gecmis-sil', methods=['POST'])
def gecmis_sil():
    kayit_id = request.json.get('id')
    gecmis = gecmis_getir()
    gecmis = [k for k in gecmis if k['id'] != kayit_id]
    with open(GECMIS_FILE, 'w', encoding='utf-8') as f:
        json.dump(gecmis, f, ensure_ascii=False)
    return jsonify({"status": "success"})

@app.route('/stok-guncelle', methods=['POST'])
def stok_guncelle():
    data = request.json
    urun_id = data.get('id')
    durum = data.get('durum')  # 'var', 'azaliyor', 'yok'
    stok = stok_getir()
    if durum is None:
        stok.pop(urun_id, None)
    else:
        stok[urun_id] = durum
    with open(STOK_FILE, 'w', encoding='utf-8') as f:
        json.dump(stok, f, ensure_ascii=False)
    return jsonify({"status": "success", "stok": stok})

@app.route('/stok-uyari', methods=['GET'])
def stok_uyari():
    """Azalan/biten ürünleri döndür"""
    stok = stok_getir()
    veriler = excel_oku()
    uyarilar = []
    for kat, df in veriler.items():
        for _, row in df.iterrows():
            uid = str(row['ID'])
            if stok.get(uid) in ('azaliyor', 'yok'):
                uyarilar.append({
                    'id': uid,
                    'ad': row['Ürün Adı'],
                    'kategori': kat,
                    'durum': stok[uid]
                })
    return jsonify(uyarilar)

@app.route('/favori-guncelle', methods=['POST'])
def favori_guncelle():
    data = request.json
    urun_id = data.get('id')
    favoriler = favorileri_getir()
    if urun_id in favoriler:
        favoriler.remove(urun_id)
        durum = 'removed'
    else:
        favoriler.append(urun_id)
        durum = 'added'
    with open(FAV_FILE, 'w', encoding='utf-8') as f:
        json.dump(favoriler, f, ensure_ascii=False)
    return jsonify({"status": "success", "action": durum, "favoriler": favoriler})

@app.route('/urun-sil', methods=['POST'])
def urun_sil():
    data = request.json
    kat = data.get('kategori')
    urun_id = data.get('id')
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=kat)
        df = df[df['ID'] != urun_id]
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, sheet_name=kat, index=False)
        favoriler = favorileri_getir()
        if urun_id in favoriler:
            favoriler.remove(urun_id)
            with open(FAV_FILE, 'w', encoding='utf-8') as f:
                json.dump(favoriler, f, ensure_ascii=False)
        stok = stok_getir()
        stok.pop(urun_id, None)
        with open(STOK_FILE, 'w', encoding='utf-8') as f:
            json.dump(stok, f, ensure_ascii=False)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/urun-ekle', methods=['POST'])
def urun_ekle():
    data = request.json
    kat = data.get('kategori')
    ad = data.get('urun_adi', '').strip()
    birim = data.get('birim')
    alt_kat = data.get('alt_kategori', 'Genel').strip() or 'Genel'

    if not ad:
        return jsonify({"status": "error", "message": "Ürün adı boş olamaz"}), 400

    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=kat)
        prefix = ''.join([c for c in kat if c.isupper()])[:2]
        if len(prefix) < 2:
            prefix = kat[:2].upper()
        mevcut_ids = df['ID'].tolist()
        num = len(df) + 1
        yeni_id = f"{prefix}{num:02d}"
        while yeni_id in mevcut_ids:
            num += 1
            yeni_id = f"{prefix}{num:02d}"

        yeni_satir = pd.DataFrame([{
            "ID": yeni_id, "Alt Kategori": alt_kat,
            "Ürün Adı": ad, "Varsayılan Birim": birim, "Notlar": ""
        }])

        alt_kat_satirlari = df[df['Alt Kategori'] == alt_kat]
        if not alt_kat_satirlari.empty:
            son_index = alt_kat_satirlari.index[-1]
            df = pd.concat([df.iloc[:son_index + 1], yeni_satir, df.iloc[son_index + 1:]], ignore_index=True)
        else:
            df = pd.concat([df, yeni_satir], ignore_index=True)

        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, sheet_name=kat, index=False)
        return jsonify({"status": "success", "id": yeni_id, "alt_kategori": alt_kat})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/liste-temizle', methods=['POST'])
def liste_temizle():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump({}, f)
    return jsonify({"status": "success"})

@app.route('/alt-kategoriler/<kategori>')
def alt_kategoriler(kategori):
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=kategori)
        cats = df['Alt Kategori'].dropna().unique().tolist()
        return jsonify(cats)
    except:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)