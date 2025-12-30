

def hesapla_anlik_risk(row_df2):
    """
    EPSS ve CVSS verilerine dayanarak risk skoru ve seviyesi hesaplar.
    """
    # 1. CISA KEV Kontrolü (Acil Durum)
    if row_df2.get('cisa_kev') is True:
        return "CRITICAL", 10.0, "ACİL: Aktif Saldırı Var (CISA KEV)"

    # 2. Temel Puanların Alınması
    base = row_df2.get('base_score', 0)
    impact = row_df2.get('impact_score', 0)
    exploit = row_df2.get('exploitability_score', 0)
    vector = row_df2.get('attack_vector', 'UNKNOWN')

    # 3. Ağırlıklı Hesaplama
    ham_puan = (base * 0.5) + (impact * 0.3) + (exploit * 0.2)

    # 4. Vektör Cezası (Network üzerinden ise risk artar)
    if vector == 'NETWORK':
        ham_puan += 1.5

    # 5. Normalizasyon (Max 10.0)
    final_score = min(ham_puan, 10.0)
    final_score = round(final_score, 1)

    # 6. Etiketleme
    if final_score >= 9.0:
        return "CRITICAL", final_score, "Yüksek Skor + Kritik Faktörler"
    elif final_score >= 7.0:
        return "HIGH", final_score, "Yüksek Riskli"
    elif final_score >= 4.0:
        return "MEDIUM", final_score, "Orta Seviye"
    else:
        return "LOW", final_score, "Düşük Seviye"