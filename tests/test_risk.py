import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.risk_engine import hesapla_anlik_risk

# TEST 1: CISA KEV (Acil Durum) Kontrolü
def test_cisa_kev_critical():
    data = {'cisa_kev': True, 'base_score': 5.0}
    severity, score, _ = hesapla_anlik_risk(data)
    assert severity == "CRITICAL"
    assert score == 10.0

# TEST 2: Network Vektör Cezası
def test_network_vector_boost():
    data = {
        'base_score': 5, 'impact_score': 5, 'exploitability_score': 5, 
        'attack_vector': 'NETWORK', 'cisa_kev': False
    }
    _, score, _ = hesapla_anlik_risk(data)
    assert score == 6.5

# TEST 3: Düşük Risk Kontrolü
def test_low_risk():
    data = {'base_score': 2, 'impact_score': 1, 'exploitability_score': 1}
    severity, _, _ = hesapla_anlik_risk(data)
    assert severity == "LOW"

# TEST 4: Maksimum Skor Sınırı (Boundary Test)
def test_score_cap():
    data = {
        'base_score': 10, 'impact_score': 10, 'exploitability_score': 10, 
        'attack_vector': 'NETWORK' 
    }
    _, score, _ = hesapla_anlik_risk(data)
    assert score == 10.0

# TEST 5: Eksik Veri Yönetimi
def test_empty_input():
    severity, score, _ = hesapla_anlik_risk({})
    assert score == 0.0
    assert severity == "LOW"