# İçerik yazım şartnamesi (CONTENT_SPEC)

Site: **Devre Analizi I — Tuna Göksu vize rehberi.** Hedef kitle: konuyu hiç bilmeyen, son gece çalışan öğrenci.
Sınav: 4 klasik soru, hepsi **bağımlı kaynaklı**:
1. Maksimum güç transferi  2. Kaynak dönüşümü veya süperpozisyon  3. Düğüm gerilimleri veya çevre akımları  4. Güç hesabı (1–3'ü içeren)

Her içerik dosyası `build/content/<ad>.py` şunları dışa verir:

```python
from circuitkit import elm, ACCENT, NODE
def draw_xxx(d): ...            # schemdraw çizimi
CIRCUITS = {"p4-88": draw_xxx}  # şema adı -> fonksiyon  (circuits/<ad>.svg üretilir)
PROBLEMS = [dict(...), ...]
```

**Referans örnek: `build/content/q1.py` içindeki P4.87.** Üslup, ayrıntı düzeyi ve LaTeX biçimi onunla aynı olmalı.

## Problem sözlüğü alanları

| alan | açıklama |
|---|---|
| `id` | küçük harf, tire: `"p4-88"`, `"cy2-s2-d1"`, `"p2-10"` (sayfa içi bağlantı) |
| `topic` | 1, 2, 3 veya 4 |
| `code` | görünen kod: `"P4.88"`, `"ÇY2 · s2 · 1"` |
| `title` | kısa, bilgi veren başlık; inline matematik `$...$` serbest |
| `source` | `"Çalışma Yaprağı 4 s.1"` gibi |
| `image` | `img/` içindeki orijinal görselin dosya adı (ör. `"P4_88_ORIG.webp"`) |
| `circuit` | CIRCUITS anahtarı (yeniden çizilmiş çözüm şeması) |
| `circuit_caption` | şema altı kısa not (düğüm/akım isimlendirmesi) |
| `level` | 1 Temel · 2 Orta · 3 Zor |
| `question` | sorunun tam metni (HTML + `$...$`). Kitaptaki istenenlerin hepsi. |
| `strategy` | 3–5 maddelik çözüm planı (liste) |
| `steps` | adımlar listesi: `dict(title=..., body=..., math=..., note=...)` |
| `answer` | sonuç listesi, her öğe **saf LaTeX** (dolar işareti YOK): `r"R_o = 4\ \Omega"` |
| `exam` | sınav kağıdına yazılacak saf matematik, **tek** `\begin{aligned}...\end{aligned}` bloğu (dolar YOK) |
| `traps` | 2–4 adet "sık yapılan hata" (HTML + `$...$`) |

### Adım (`steps`) kuralları — EN ÖNEMLİ KISIM
- **Hiçbir cebir adımı atlanmaz.** Payda eşitleme (`/\times 30`), parantez açma, terim toplama, yerine koyma, sadeleştirme ayrı satırlarda.
- `body`: "aptala anlatır gibi" Türkçe açıklama (neden böyle yaptığımızı söyle). HTML + `$...$` inline matematik.
- `math`: display matematik, **dolar işareti kullanma**. Çok satırlıysa `\begin{aligned} ... \\ ... \end{aligned}`.
  Birimler `\ \text{V}`, `\ \Omega`, `\ \text{A}`, `\ \text{W}`. Türkçe kelime: `\text{yani ...}`.
  Sonuç satırını `\boxed{...}` ile vurgula. Denklem etiketleri `\qquad \text{(I)}`.
- `note` (opsiyonel): kısa ipucu / tahtada hocanın yaptığı şey.
- Düğüm KCL kuralı sitede tek tip: **çıkan akımlar +, giren akımlar −, toplam = 0**. Çevre KVL: saat yönünde dolaş, önce karşılaşılan işaret.
- Güç: **pasif işaret kuralı** — akım + uçtan giriyorsa $p = +vi$; $p>0$ güç harcar (emer), $p<0$ güç üretir. Güç sorularında mutlaka $\sum p = 0$ sağlaması yap.
- Python raw string kullan: `r"""..."""`. `body` normal string ise ters bölüyü iki kez yaz (`"$v_\\Delta$"`).

## DOĞRULUK — PAZARLIKSIZ
- Eski sitedeki çözümlere **güvenme** (P4.87'de akım yönü hatası bulundu, sonuç yanlıştı). Her soruyu orijinal görselden
  (`img/*.webp`, read_file ile aç) baştan oku: her direnç değeri, her kaynak yönü/kutbu, her akım okunun yönü, her +/− işareti.
- Her problemi Python ile (fractions.Fraction veya numpy) **bağımsız olarak çöz** ve adımlardaki her ara sayıyı bununla karşılaştır.
  Doğrulama betiklerini `build/verify/<ad>_verify.py` olarak bırak (çalıştırınca tüm sonuçları assert etsin).
- Güç sorularında $\sum p = 0$ sayısal olarak sağlanmalı.
- Nilsson & Riedel'in yayınlanmış cevaplarını biliyorsan karşılaştır; tutmuyorsa devreyi tekrar oku.

## Devre şeması kuralları (schemdraw, `circuitkit`)
- Şema, orijinal şeklin **topolojik olarak birebir** aynısı olmalı; yerleşim de mümkün olduğunca benzer (soldan sağa aynı sırada kollar).
- Kaynak yönleri: `SourceV().up()` → + üstte; `.down()` → + altta; `.reverse()` çevirir. Akım kaynağı `.up()` → ok yukarı.
  Bağımlı kaynaklar: `SourceControlledV` (+/− baklava), `SourceControlledI` (oklu baklava). Yük için `ResistorVar`.
- Kontrol değişkeni etiketleri (`$v_\\Delta$`, `$i_x$` ve okları) `color=ACCENT`; düğüm adları (`$V_1$`) `color=NODE`.
- Etiketler çizgilerle/başka etiketlerle **çakışmamalı**. Gerekirse `loc='top'/'bottom'/'left'/'right'`, `ofst=`, eleman uzunluğu (`d.unit*0.6`) ile oyna.
- Referans düğüme `elm.Ground()` koy; terminaller `elm.Dot(open=True).label('a')`.
- Çizim sonrası `python build/preview.py <ad> --shot` çalıştır, PNG parçalarını read_file ile **mutlaka aç ve kontrol et**:
  şema orijinalle aynı mı, etiket çakışması var mı, KaTeX hatası (kırmızı metin) var mı. Düzelt, tekrar çek.

## Yasaklar
- Emoji kullanma (başlık, metin, not — hiçbir yerde).
- `<code>` içinde formül yazma; formüller KaTeX ile.
- Abartılı/argo ton yok; samimi ama net, öğretmen gibi.
- Başka dosyalara (q1.py, render.py, style.css, app.js) dokunma; sadece kendi içerik dosyan ve kendi verify betiğin.
