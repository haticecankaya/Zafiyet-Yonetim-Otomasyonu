# main.py
import streamlit as st
import json
import pandas as pd
import time
from src.risk_engine import hesapla_anlik_risk
from src.jira_client import test_jira_connection, create_jira_issue
from src.data_loader import load_datasets

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Zafiyet Yönetim Otomasyonu", layout="wide", page_icon="🛡️")

# --- STATE YÖNETİMİ ---
if 'giris_yapildi' not in st.session_state:
    st.session_state['giris_yapildi'] = False
if 'jira_config' not in st.session_state:
    st.session_state['jira_config'] = {}
if 'df_corpus' not in st.session_state:
    st.session_state['df_corpus'], st.session_state['df_epss'] = load_datasets()

# --- YARDIMCI FONKSİYON: TICKET HAZIRLIK ---
def prepare_and_create_ticket(json_row):
    """UI verisini hazırlar ve modüle gönderir."""
    # 1. Veri Zenginleştirme (UI State'den okuma burada yapılır)
    cve_id = json_row.get('cve_id', 'Bilinmiyor')
    ip_adres = json_row.get('ip', 'Bilinmiyor')
    
    severity = "UNKNOWN"
    cvss_score = 0.0
    risk_nedeni = "Veri bulunamadı"
    cve_tanimi = "Tanım bulunamadı."
    vector = "Bilinmiyor"

    # Corpus'tan Tanım Bulma
    if st.session_state['df_corpus'] is not None:
        df1 = st.session_state['df_corpus']
        matches = df1[df1['cve_id'] == cve_id]
        if not matches.empty:
            cve_tanimi = matches.iloc[0]['description_data']

    # EPSS'den Risk Hesaplama
    if st.session_state['df_epss'] is not None:
        df2 = st.session_state['df_epss']
        matches = df2[df2['cve_id'] == cve_id]
        if not matches.empty:
            data_row = matches.iloc[0]
            vector = data_row.get('attack_vector', vector)
            # Modül Çağrısı
            severity, cvss_score, risk_nedeni = hesapla_anlik_risk(data_row)

    # 2. Jira Veri Paketinin Hazırlanması
    summary = f"[{severity}] {ip_adres} üzerinde {cve_id} (Skor: {cvss_score})"
    description = f"""
    *Otomatik Risk Analiz Raporu*
    --------------------------------------------------
    *Hedef IP:* {ip_adres}
    *CVE ID:* {cve_id}
    *RİSK:* {severity} ({cvss_score})
    *NEDEN:* {risk_nedeni}
    *Vektör:* {vector}

    *Tanım:*
    {cve_tanimi}
    """
    
    issue_data = {
        'summary': summary,
        'description': description,
        'priority': 'High' if severity in ['CRITICAL', 'HIGH'] else 'Medium'
    }

    # 3. Jira Modülüne Gönderim
    return create_jira_issue(st.session_state['jira_config'], issue_data)

# --- UI BİLEŞENLERİ ---
def sidebar_section():
    with st.sidebar:
        st.header("⚙️ JIRA Ayarları")
        with st.form("jira_config_form"):
            j_url = st.text_input("Jira URL", value=st.session_state['jira_config'].get('url', ''))
            j_user = st.text_input("Kullanıcı E-posta", value=st.session_state['jira_config'].get('user', ''))
            j_token = st.text_input("API Token", type="password", value=st.session_state['jira_config'].get('token', ''))
            j_project = st.text_input("Proje Key", value=st.session_state['jira_config'].get('project', ''))
            j_issuetype = st.text_input("Kayıt Tipi", value=st.session_state['jira_config'].get('issuetype', 'Task'))

            c1, c2 = st.columns(2)
            if c1.form_submit_button("Test Et 🔌"):
                if not j_url or not j_token:
                    st.error("URL ve Token gerekli.")
                else:
                    status, msg, _ = test_jira_connection(j_url.strip(), j_user.strip(), j_token.strip(), j_project.strip())
                    if status: st.success(msg)
                    else: st.error(msg)
            
            if c2.form_submit_button("Kaydet 💾"):
                st.session_state['jira_config'] = {
                    'url': j_url.strip(), 'user': j_user.strip(), 
                    'token': j_token.strip(), 'project': j_project.strip(), 
                    'issuetype': j_issuetype.strip()
                }
                st.success("Kaydedildi!")
        
        st.divider()
        if st.session_state['df_corpus'] is not None:
            st.success("Veritabanları Hazır (CSV).")
        else:
            st.warning("CSV dosyaları eksik.")

def login_section():
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.header("🔒 Giriş Paneli")
        with st.form("giris"):
            u = st.text_input("Kullanıcı Adı")
            p = st.text_input("Şifre", type="password")
            if st.form_submit_button("Giriş"):
                if u == "admin" and p == "1234":
                    st.session_state['giris_yapildi'] = True
                    st.rerun()
                else:
                    st.error("Hatalı giriş")

def main_app():
    sidebar_section()
    col_baslik, col_cikis = st.columns([6, 1])
    col_baslik.header("📂 Zafiyet Yönetim Paneli")
    if col_cikis.button("Çıkış"):
        st.session_state['giris_yapildi'] = False
        st.rerun()
    
    st.divider()
    uploaded = st.file_uploader("Rapor Yükle (final_report.json)", type=['json'])

    if uploaded:
        try:
            data = json.load(uploaded)
            df = pd.DataFrame(data)
            st.info(f"Analiz edilen zafiyet sayısı: {len(df)}")
            
            # Toplu İşlem
            if st.button("Tümüne Ticket Aç", type="primary"):
                if not st.session_state['jira_config'].get('token'):
                    st.error("Lütfen önce Jira ayarlarını yapın.")
                else:
                    bar = st.progress(0)
                    success_count = 0
                    for i, row in df.iterrows():
                        status, _ = prepare_and_create_ticket(row)
                        if status: success_count += 1
                        bar.progress((i + 1) / len(df))
                    bar.empty()
                    st.success(f"{success_count}/{len(df)} işlem tamamlandı.")

            # Liste Görünümü
            for idx, row in df.iterrows():
                c1, c2 = st.columns([1, 7], vertical_alignment="center")
                if c1.button("Ticket 🎫", key=f"btn_{idx}"):
                    status, msg = prepare_and_create_ticket(row)
                    if status: st.toast(f"Başarılı: {msg}", icon="✅")
                    else: st.error(msg)
                
                with c2.expander(f"{row.get('cve_id')} - {row.get('ip')}"):
                    st.json(row.to_dict())

        except Exception as e:
            st.error(f"Dosya okuma hatası: {e}")

# --- ÇALIŞTIRMA ---
if __name__ == "__main__":
    if st.session_state['giris_yapildi']:
        main_app()
    else:
        login_section()