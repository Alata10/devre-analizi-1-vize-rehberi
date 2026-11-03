# Devre Analizi I — Vize Rehberi (Tuna Göksu)

Canlı site: https://alata10.github.io/devre-analizi-1-vize-rehberi/

Sınav formatı: 4 klasik soru, hepsi bağımlı kaynaklı —
1. Maksimum güç transferi · 2. Kaynak dönüşümü / süperpozisyon · 3. Düğüm gerilimleri / çevre akımları · 4. Güç hesabı.

## Özellikler
- Çalışma yapraklarındaki tüm bağımlı kaynaklı sorular, adım adım (hiçbir cebir adımı atlanmadan), KaTeX ile dizilmiş matematik
- Her soru için kitaptaki orijinal şekil + schemdraw ile yeniden çizilmiş, düğümleri işaretli çözüm şeması
- Detaylı anlatım / sınav kağıdı / adım adım görünümleri
- İlerleme takibi (tarayıcıda saklanır), gece/gündüz modu, arama, son gece özeti, 90 dakikalık deneme sınavları

## Geliştirme
```
pip install schemdraw ziamath ziafont pillow
python build/site.py                 # index.html + circuits/*.svg üretir
python build/preview.py q1 --shot    # tek içerik dosyasını önizle
python build/verify/q1b_verify.py    # sayısal doğrulama
```
İçerik: `build/content/*.py` (şartname: `build/CONTENT_SPEC.md`).
