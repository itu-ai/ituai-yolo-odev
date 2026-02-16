# 🎮 ITU AI CLUB YOLO ODEVI

## Amaç

Bu projede basit bir 2D oyunu klavyeyle kontrol ediyoruz. Sonra kafa hareketleriyle kontrol edeceğiz. Kafa hareketlerini algılamak için YOLO adlı yapay zeka modelini kullanacağız.

## Kütüphaneler

```bash
pip install pygame ultralytics opencv-python
```

---

## Bölüm 1 — Klavyeli Oyun (`oyun.py`)

```bash
python oyun.py
```

← → ok tuşlarıyla yukarıdan düşen bloklardan kaçın.

Kodun tamamı tek bir döngüden oluşuyor. Her döngüde sırasıyla şunlar yapılıyor:
- Klavyeden girdi alınıyor
- Düşmanlar aşağı kaydırılıyor
- Çarpışma kontrolü yapılıyor
- Ekrana her şey çiziliyor

Bizim için önemli olan kısım girdi alma. Klavye versiyonunda bu iş 4 satırla halloluyor:

```python
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    player.x -= PLAYER_SPEED
if keys[pygame.K_RIGHT]:
    player.x += PLAYER_SPEED
```

---

## Bölüm 2 — YOLO Nedir?

YOLO (You Only Look Once), bir görüntüdeki nesneleri ve insanları gerçek zamanlı olarak algılayabilen bir yapay zeka modeli.
docs.ultralytics.com/models/yolov8/

Biz YOLO'nun **pose** versiyonunu kullanacağız. Bu versiyon insan vücudunda 17 anahtar noktayı (keypoint) tespit ediyor: burun, gözler, kulaklar, omuzlar vs.

Bize lazım olan iki tanesi:
- **Keypoint 1** → sol göz
- **Keypoint 2** → sağ göz

Kafanın hangi yöne eğik olduğunu anlamak için iki gözün ekrandaki yüksekliğine bakıyoruz:

```
   Düz:            Sola eğik:       Sağa eğik:
   O    O             O                    O
                         O              O
```

Sol göz sağ gözden aşağıdaysa → kafa sola eğik. Tam tersi → sağa eğik.

---

## Bölüm 3 — YOLO Versiyonuna Geçiş

`oyun_klavye.py` dosyasını kopyalayıp `oyun_yolo.py` olarak kaydedin. Şimdi 4 adımda bu dosyayı dönüştüreceğiz.

### Adım 1 — import'ları ekle

Webcam için OpenCV, yapay zeka için YOLO gerekiyor:

```python
import cv2
from ultralytics import YOLO
```

### Adım 2 — Model ve kamerayı hazırla

Pygame kurulumunun hemen altına şunları ekleyin:

```python
model = YOLO("yolov8n-pose.pt")
camera = cv2.VideoCapture(0)
```

İlk satır YOLO'nun pose modelini yüklüyor (ilk çalıştırmada otomatik iniyor, ~6 MB). İkinci satır webcam'i açıyor.

### Adım 3 — Klavye girdisini kafa eğme ile değiştir

Asıl değişiklik bu. Eski 4 satırı silip yerine şunu koyuyoruz:

```python
ok, frame = camera.read()
frame=cv2.flip(frame,1)
results = model(frame, verbose=False)
```

İlk iki satır kameradan bir kare alıp aynalıyor (aynalama sayesinde sağa hareket ettiğinizde ekranda da sağa gidiyor). Üçüncü satır bu kareyi YOLO'ya veriyor.

YOLO'dan dönen sonuçlardan göz koordinatlarını çekiyoruz:

```python
keypoints = results[0].keypoints.data[0]
left_eye = keypoints[1]
right_eye = keypoints[2]
```

Her keypoint `[x, y, güven_skoru]` şeklinde bir dizi. Yani left_eye.[1] sol gözün `y` değerini veriyor. Gözler arasındaki yükseklik farkını kullanarak karakteri kontrol edin

### Adım 4 — Kamera önizlemesini ekrana koy (opsiyonel)

Oynarken webcam görüntüsünü köşede görmek işe yarıyor. Çizim bölümüne şunu ekliyoruz:

```python
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
preview = cv2.resize(frame_rgb, (160, 120))
cam_surface = pygame.surfarray.make_surface(preview.swapaxes(0, 1))
screen.blit(cam_surface, (430, 10))
```

---


## Sonuç

Yapılan tek şey girdinin kaynağını değiştirmek oldu:

| Klavye versiyonu | YOLO versiyonu |
|-----------------|----------------|
| `pygame.key.get_pressed()` | `model(frame)` + göz karşılaştırması |
| Tuşa basılır | Kafa eğilir |
| 4 satır | ~15 satır |

Oyun mantığı — düşmanlar, skor, çarpışma — hiçbirine dokunulmadı.

---

## Ayarları değiştirme (opsiyonel)

- **`PLAYER_SPEED`** — Oyuncunun hareket hızı
- **`ENEMY_SPEED`** — Blokların düşme hızı
- **`SPAWN_INTERVAL`** — Küçültürseniz daha sık blok gelir

---
