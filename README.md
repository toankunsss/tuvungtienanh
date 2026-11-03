# Từ vựng tiếng Anh Global Success (lớp 1 → 12)

Bộ dữ liệu **từ vựng theo từng unit** của bộ sách giáo khoa **Tiếng Anh Global Success**
(NXB Giáo dục Việt Nam, bộ *Kết nối tri thức với cuộc sống*) từ lớp 1 đến lớp 12, lưu dưới dạng **JSON** (kèm bản **CSV**).

Mỗi từ có: **từ**, **từ loại**, **phiên âm IPA giọng Anh (UK) và giọng Mỹ (US)**, **file giọng đọc UK và US (MP3)**, **nghĩa tiếng Việt** và **câu ví dụ kèm bản dịch tiếng Việt**.

> ⚠️ **Đọc kỹ phần [Trạng thái dữ liệu](#trạng-thái-dữ-liệu) trước khi dùng.**
> Mỗi unit có trường `status`: `sourced` = danh sách từ đã được đối chiếu với nguồn trên mạng;
> `unverified` = bản nháp, **chưa** được đối chiếu, có thể thiếu từ hoặc có từ không thuộc sách.

---

## Mục lục

- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Định dạng dữ liệu](#định-dạng-dữ-liệu)
- [Cách sử dụng](#cách-sử-dụng)
- [Phát âm: IPA và giọng đọc UK / US](#phát-âm-ipa-và-giọng-đọc-uk--us)
- [Trạng thái dữ liệu](#trạng-thái-dữ-liệu)
- [Nguồn và độ chính xác](#nguồn-và-độ-chính-xác)
- [Đóng góp / sửa dữ liệu](#đóng-góp--sửa-dữ-liệu)

---

## Cấu trúc thư mục

```
.
├── data/                    # DỮ LIỆU GỐC – mỗi lớp 1 file (sửa ở đây)
│   ├── grade-01.json
│   ├── ...
│   └── grade-12.json
├── audio/                   # Giọng đọc MP3
│   ├── uk/<từ>.mp3          #   giọng Anh (British)
│   ├── us/<từ>.mp3          #   giọng Mỹ (American)
│   └── manifest.json        #   cách sinh từng file (văn bản hay IPA)
├── dist/                    # File sinh tự động từ data/ (đừng sửa tay)
│   ├── all.json             # Tất cả các lớp trong 1 file (dạng lồng nhau)
│   ├── flat.json            # Mỗi phần tử là 1 từ (dạng phẳng, dễ lọc)
│   ├── stats.json           # Thống kê số từ theo lớp / unit
│   └── csv/grade-XX.csv     # Bản CSV (UTF-8 BOM, mở thẳng bằng Excel)
├── schema/grade.schema.json # JSON Schema mô tả định dạng 1 file lớp
└── scripts/
    ├── validate.py          # Kiểm tra lỗi dữ liệu
    ├── build.py             # Sinh thư mục dist/
    ├── ipa_us.py            # Sinh IPA giọng Mỹ từ từ điển CMU
    ├── ipa_us_overrides.json#   IPA Mỹ viết tay cho từ không có trong CMU
    ├── make_audio.py        # Sinh giọng đọc UK / US
    └── readme_tables.py     # Cập nhật bảng trạng thái trong README
```

## Định dạng dữ liệu

### File một lớp – `data/grade-XX.json`

```json
{
  "grade": 6,
  "series": "Global Success",
  "book_title": "Tiếng Anh 6 – Global Success",
  "publisher": "NXB Giáo dục Việt Nam",
  "units": [
    {
      "unit": 1,
      "title": "My new school",
      "title_vi": "Ngôi trường mới của tôi",
      "status": "sourced",
      "sources": ["https://..."],
      "words": [
        {
          "word": "activity",
          "pos": "n",
          "ipa_uk": "/ækˈtɪvəti/",
          "ipa_us": "/ækˈtɪvəti/",
          "audio_uk": "audio/uk/activity.mp3",
          "audio_us": "audio/us/activity.mp3",
          "meaning": "hoạt động",
          "example": "We have many activities at school.",
          "example_vi": "Ở trường chúng mình có nhiều hoạt động."
        }
      ]
    }
  ]
}
```

| Trường | Ý nghĩa |
|---|---|
| `unit` | Số thứ tự unit (không tính các bài Review) |
| `title` / `title_vi` | Tên unit tiếng Anh / tiếng Việt |
| `status` | `sourced` hoặc `unverified` (xem bên dưới) |
| `sources` | Các trang web đã dùng để đối chiếu danh sách từ |
| `words[].word` | Từ / cụm từ |
| `words[].pos` | Từ loại (bảng dưới) |
| `words[].ipa_uk` | Phiên âm IPA giọng Anh (British), nằm giữa hai dấu `/ /` |
| `words[].ipa_us` | Phiên âm IPA giọng Mỹ (American) |
| `words[].audio_uk` | Đường dẫn file MP3 giọng Anh (tính từ gốc repo) |
| `words[].audio_us` | Đường dẫn file MP3 giọng Mỹ |
| `words[].meaning` | Nghĩa tiếng Việt |
| `words[].example` | Câu ví dụ tiếng Anh |
| `words[].example_vi` | Bản dịch tiếng Việt của câu ví dụ |

**Từ loại (`pos`)**

| Mã | Nghĩa | Mã | Nghĩa |
|---|---|---|---|
| `n` | danh từ | `prep` | giới từ |
| `v` | động từ | `conj` | liên từ |
| `adj` | tính từ | `pron` | đại từ |
| `adv` | trạng từ | `det` | từ hạn định |
| `num` | số từ | `exclam` | thán từ |
| `phr` | cụm từ | `phr v` | cụm động từ |
| `idiom` | thành ngữ | `modal v` / `aux v` | động từ khuyết thiếu / trợ động từ |

### File phẳng – `dist/flat.json`

```json
[
  {
    "grade": 6, "unit": 1, "unit_title": "My new school", "status": "sourced",
    "word": "activity", "pos": "n", "ipa_uk": "/ækˈtɪvəti/", "ipa_us": "/ækˈtɪvəti/",
    "audio_uk": "audio/uk/activity.mp3", "audio_us": "audio/us/activity.mp3",
    "meaning": "hoạt động", "example": "We have many activities at school.",
    "example_vi": "Ở trường chúng mình có nhiều hoạt động."
  }
]
```

## Cách sử dụng

### 1. Lấy trực tiếp qua URL (không cần tải repo)

```
https://raw.githubusercontent.com/toankunsss/tuvungtienanh/main/data/grade-06.json
https://raw.githubusercontent.com/toankunsss/tuvungtienanh/main/dist/all.json
https://raw.githubusercontent.com/toankunsss/tuvungtienanh/main/dist/flat.json
```

> Nếu repo để **private** thì URL raw cần token; muốn dùng công khai hãy để repo ở chế độ public.

### 2. JavaScript / TypeScript (web, React, Node)

```js
const BASE = "https://raw.githubusercontent.com/toankunsss/tuvungtienanh/main";

// Lấy từ vựng Unit 3 lớp 6
const grade = await fetch(`${BASE}/data/grade-06.json`).then(r => r.json());
const unit3 = grade.units.find(u => u.unit === 3);
unit3.words.forEach(w => console.log(`${w.word}  UK ${w.ipa_uk}  US ${w.ipa_us} – ${w.meaning}`));

// Phát giọng đọc
const play = (w, accent = "us") => new Audio(`${BASE}/${w[`audio_${accent}`]}`).play();
play(unit3.words[0], "uk");   // giọng Anh
play(unit3.words[0], "us");   // giọng Mỹ

// Chỉ lấy các từ đã có nguồn xác minh
const flat = await fetch(`${BASE}/dist/flat.json`).then(r => r.json());
const verified = flat.filter(w => w.status === "sourced");

// Tìm một từ ở mọi lớp
const hits = flat.filter(w => w.word.toLowerCase() === "environment");
```

### 3. Python

```python
import json

with open("data/grade-09.json", encoding="utf-8") as f:
    grade9 = json.load(f)

for unit in grade9["units"]:
    print(f"Unit {unit['unit']}: {unit['title']} ({len(unit['words'])} từ)")
    for w in unit["words"]:
        print(f"  {w['word']:<20} UK {w['ipa_uk']:<18} US {w['ipa_us']:<18} {w['meaning']}")
```

Dùng pandas với bản phẳng:

```python
import pandas as pd

df = pd.read_json("dist/flat.json")
df[(df.grade == 11) & (df.unit == 1)]            # Lớp 11, Unit 1
df[df.status == "sourced"].groupby("grade").size()  # Số từ đã xác minh mỗi lớp
```

### 4. Excel / Google Sheets / Anki / Quizlet

- Mở file `dist/csv/grade-XX.csv` bằng Excel hoặc import vào Google Sheets (mã hóa UTF-8).
- **Anki**: *File → Import* file CSV, ánh xạ cột `word` vào mặt trước và `ipa_uk` / `ipa_us` + `meaning` vào mặt sau. Muốn có âm thanh: chép các file trong `audio/` vào thư mục `collection.media` của Anki và thêm cột `[sound:tên-file.mp3]`.
- **Quizlet**: copy 2 cột `word` và `meaning` rồi dán vào ô *Import*.

### 5. Chạy các script (sau khi sửa dữ liệu)

Cần Python 3.10 trở lên. `validate.py`, `build.py`, `readme_tables.py` không cần thư viện ngoài.

```bash
python3 scripts/validate.py
```

```bash
python3 scripts/build.py
```

```bash
python3 scripts/readme_tables.py
```

- `validate.py` kiểm tra số unit của từng lớp, từ loại hợp lệ, IPA đúng dạng `/.../`, từ trùng lặp, unit `sourced` phải có nguồn… Có thể chỉ kiểm tra vài lớp: `python3 scripts/validate.py 6 7`.
- `build.py` sinh lại toàn bộ `dist/` từ `data/`.
- `readme_tables.py` cập nhật bảng trạng thái bên dưới.

Khi **thêm hoặc sửa từ**, sinh lại IPA Mỹ và giọng đọc cho từ mới (cần `pip install cmudict kokoro-onnx soundfile`, `ffmpeg`, và 2 file model ở [kokoro-onnx releases](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0)):

```bash
python3 scripts/ipa_us.py
```

```bash
python3 scripts/make_audio.py --model /đường/dẫn/thư-mục-model
```

`make_audio.py` chỉ sinh file còn thiếu; thêm `--force` để sinh lại tất cả.

## Phát âm: IPA và giọng đọc UK / US

| | Giọng Anh (UK) | Giọng Mỹ (US) |
|---|---|---|
| Trường IPA | `ipa_uk` | `ipa_us` |
| Kiểu ký hiệu | Cambridge / Oxford UK: `/ˈwɔːtə(r)/`, `/ɡəʊ/`, `/hɒt/` | Cambridge US: `/ˈwɑːtɚ/`, `/ɡoʊ/`, `/hɑːt/` |
| Nguồn IPA | Biên soạn theo chuẩn từ điển Anh – Anh | Sinh tự động từ **CMU Pronouncing Dictionary** (Carnegie Mellon) rồi chuyển sang ký hiệu Cambridge US; ~70 từ không có trong CMU được viết tay trong `scripts/ipa_us_overrides.json` |
| Giọng đọc | `audio/uk/*.mp3` – giọng nữ Anh `bf_emma` | `audio/us/*.mp3` – giọng nữ Mỹ `af_heart` |

- Giọng đọc được tạo bằng mô hình **Kokoro-82M** (giấy phép Apache-2.0), tốc độ 0.9×, MP3 mono 48 kbps.
- Với mỗi từ, cách đọc của mô hình được so với IPA trong dữ liệu. Nếu khớp, mô hình đọc từ như bình thường; nếu lệch (ví dụ *live* động từ /lɪv/, các từ như *dance, class* mà giọng Anh của mô hình đọc theo kiểu miền Bắc nước Anh), file được đọc **theo đúng IPA của dữ liệu**. Chi tiết từng file nằm trong `audio/manifest.json` (`mode`: `text` hoặc `ipa`).
- Từ giống nhau ở nhiều lớp dùng chung 1 file âm thanh.
- Đây là **giọng máy (TTS)**, không phải giọng thu âm của sách. Với tên riêng tiếng Việt (*Hoan Kiem Lake, Bai Dinh Pagoda…*) cách đọc chỉ mang tính tham khảo.

## Trạng thái dữ liệu

- ✅ **`sourced`**: danh sách từ của unit được đối chiếu với các trang trong `sources`.
- ⚠️ **`unverified`**: bản nháp, **chưa đối chiếu được** với nguồn nào (soạn từ hiểu biết chung về sách). Dùng tạm được để ôn tập, nhưng **không nên coi là chuẩn sách giáo khoa** cho tới khi được kiểm tra lại.

<!-- AUTO:START -->
| Lớp | Số unit | Số từ | Unit đã có nguồn (`sourced`) | Unit chưa xác minh (`unverified`) |
|---:|---:|---:|---|---|
| 1 | 16 | 83 | 1–16 | – |
| 2 | 16 | 66 | 1–16 | – |
| 3 | 20 | 214 | 1–20 | – |
| 4 | 20 | 193 | 1–9 | 10–20 |
| 5 | 20 | 202 | 1–18 | 19–20 |
| 6 | 12 | 348 | – | 1–12 |
| 7 | 12 | 230 | – | 1–12 |
| 8 | 12 | 240 | – | 1–12 |
| 9 | 12 | 302 | 1–12 | – |
| 10 | 10 | 222 | 1–10 | – |
| 11 | 10 | 301 | 1–10 | – |
| 12 | 10 | 137 | 1–2 | 3–10 |
| **Tổng** | | **2538** | | |

<details><summary><b>Lớp 1</b> – Tiếng Anh 1 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | In the school playground | Ở sân chơi trường học | 4 | ✅ sourced |
| 2 | In the dining room | Trong phòng ăn | 6 | ✅ sourced |
| 3 | At the street market | Ở chợ đường phố | 5 | ✅ sourced |
| 4 | In the bedroom | Trong phòng ngủ | 6 | ✅ sourced |
| 5 | At the fish and chip shop | Ở cửa hàng cá và khoai tây chiên | 7 | ✅ sourced |
| 6 | In the classroom | Trong lớp học | 7 | ✅ sourced |
| 7 | In the garden | Trong vườn | 5 | ✅ sourced |
| 8 | In the park | Trong công viên | 4 | ✅ sourced |
| 9 | In the shop | Trong cửa hàng | 5 | ✅ sourced |
| 10 | At the zoo | Ở vườn thú | 4 | ✅ sourced |
| 11 | At the bus stop | Ở trạm xe buýt | 7 | ✅ sourced |
| 12 | At the lake | Ở bờ hồ | 4 | ✅ sourced |
| 13 | In the school canteen | Ở căng tin trường học | 4 | ✅ sourced |
| 14 | In the toy shop | Ở cửa hàng đồ chơi | 4 | ✅ sourced |
| 15 | At the football match | Ở trận bóng đá | 7 | ✅ sourced |
| 16 | At home | Ở nhà | 4 | ✅ sourced |

</details>

<details><summary><b>Lớp 2</b> – Tiếng Anh 2 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | At my birthday party | Ở bữa tiệc sinh nhật của tớ | 4 | ✅ sourced |
| 2 | In the backyard | Ở sân sau | 5 | ✅ sourced |
| 3 | At the seaside | Ở bờ biển | 5 | ✅ sourced |
| 4 | In the countryside | Ở nông thôn | 4 | ✅ sourced |
| 5 | In the classroom | Trong lớp học | 4 | ✅ sourced |
| 6 | On the farm | Ở nông trại | 4 | ✅ sourced |
| 7 | In the kitchen | Trong nhà bếp | 4 | ✅ sourced |
| 8 | In the village | Ở ngôi làng | 3 | ✅ sourced |
| 9 | In the grocery store | Ở cửa hàng tạp hóa | 5 | ✅ sourced |
| 10 | At the zoo | Ở vườn thú | 3 | ✅ sourced |
| 11 | In the playground | Ở sân chơi | 4 | ✅ sourced |
| 12 | At the café | Ở quán cà phê | 4 | ✅ sourced |
| 13 | In the maths class | Trong giờ học toán | 5 | ✅ sourced |
| 14 | At home | Ở nhà | 4 | ✅ sourced |
| 15 | In the clothes shop | Ở cửa hàng quần áo | 4 | ✅ sourced |
| 16 | At the campsite | Ở khu cắm trại | 4 | ✅ sourced |

</details>

<details><summary><b>Lớp 3</b> – Tiếng Anh 3 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | Hello | Xin chào | 8 | ✅ sourced |
| 2 | Our names | Tên của chúng mình | 17 | ✅ sourced |
| 3 | Our friends | Bạn bè của chúng mình | 7 | ✅ sourced |
| 4 | Our bodies | Cơ thể của chúng mình | 10 | ✅ sourced |
| 5 | My hobbies | Sở thích của mình | 11 | ✅ sourced |
| 6 | Our school | Trường của chúng mình | 8 | ✅ sourced |
| 7 | Classroom instructions | Hiệu lệnh trong lớp học | 12 | ✅ sourced |
| 8 | My school things | Đồ dùng học tập của mình | 8 | ✅ sourced |
| 9 | Colours | Màu sắc | 11 | ✅ sourced |
| 10 | Break time activities | Hoạt động giờ ra chơi | 10 | ✅ sourced |
| 11 | My family | Gia đình của mình | 13 | ✅ sourced |
| 12 | Jobs | Nghề nghiệp | 6 | ✅ sourced |
| 13 | My house | Ngôi nhà của mình | 11 | ✅ sourced |
| 14 | My bedroom | Phòng ngủ của mình | 13 | ✅ sourced |
| 15 | At the dining table | Bên bàn ăn | 15 | ✅ sourced |
| 16 | My pets | Thú cưng của mình | 11 | ✅ sourced |
| 17 | Our toys | Đồ chơi của chúng mình | 11 | ✅ sourced |
| 18 | Playing and doing | Chơi và làm | 10 | ✅ sourced |
| 19 | Outdoor activities | Hoạt động ngoài trời | 11 | ✅ sourced |
| 20 | At the zoo | Ở vườn thú | 11 | ✅ sourced |

</details>

<details><summary><b>Lớp 4</b> – Tiếng Anh 4 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | My friends | Bạn bè của mình | 14 | ✅ sourced |
| 2 | Time and daily routines | Thời gian và các hoạt động hằng ngày | 9 | ✅ sourced |
| 3 | My week | Tuần của mình | 15 | ✅ sourced |
| 4 | My birthday party | Bữa tiệc sinh nhật của mình | 21 | ✅ sourced |
| 5 | Things we can do | Những việc chúng mình có thể làm | 9 | ✅ sourced |
| 6 | Our school facilities | Cơ sở vật chất trường chúng mình | 9 | ✅ sourced |
| 7 | Our timetables | Thời khóa biểu của chúng mình | 10 | ✅ sourced |
| 8 | My favourite subjects | Môn học yêu thích của mình | 11 | ✅ sourced |
| 9 | Our sports day | Ngày hội thể thao của chúng mình | 12 | ✅ sourced |
| 10 | Our summer holidays | Kỳ nghỉ hè của chúng mình | 6 | ⚠️ unverified |
| 11 | My home | Nhà của mình | 8 | ⚠️ unverified |
| 12 | Jobs | Nghề nghiệp | 10 | ⚠️ unverified |
| 13 | Appearance | Ngoại hình | 8 | ⚠️ unverified |
| 14 | Daily activities | Hoạt động hằng ngày | 7 | ⚠️ unverified |
| 15 | My family's weekends | Những ngày cuối tuần của gia đình mình | 7 | ⚠️ unverified |
| 16 | Weather | Thời tiết | 8 | ⚠️ unverified |
| 17 | In the city | Ở thành phố | 8 | ⚠️ unverified |
| 18 | At the shopping centre | Ở trung tâm mua sắm | 8 | ⚠️ unverified |
| 19 | The animal world | Thế giới động vật | 7 | ⚠️ unverified |
| 20 | At summer camp | Ở trại hè | 6 | ⚠️ unverified |

</details>

<details><summary><b>Lớp 5</b> – Tiếng Anh 5 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | All about me! | Tất cả về tôi | 17 | ✅ sourced |
| 2 | Our homes | Nhà của chúng ta | 9 | ✅ sourced |
| 3 | My foreign friends | Những người bạn nước ngoài của tôi | 14 | ✅ sourced |
| 4 | Our free-time activities | Các hoạt động thời gian rảnh của chúng ta | 10 | ✅ sourced |
| 5 | My future job | Công việc tương lai của tôi | 12 | ✅ sourced |
| 6 | Our school rooms | Các phòng học ở trường của chúng ta | 15 | ✅ sourced |
| 7 | Our favourite school activities | Các hoạt động ở trường mà chúng ta yêu thích | 8 | ✅ sourced |
| 8 | In our classroom | Trong lớp học của chúng ta | 12 | ✅ sourced |
| 9 | Our outdoor activities | Các hoạt động ngoài trời của chúng ta | 9 | ✅ sourced |
| 10 | Our school trip | Chuyến đi của trường chúng ta | 7 | ✅ sourced |
| 11 | Family time | Thời gian bên gia đình | 7 | ✅ sourced |
| 12 | Our Tet holiday | Kỳ nghỉ Tết của chúng ta | 10 | ✅ sourced |
| 13 | Our special days | Những ngày đặc biệt của chúng ta | 8 | ✅ sourced |
| 14 | Staying healthy | Giữ gìn sức khỏe | 8 | ✅ sourced |
| 15 | Our health | Sức khỏe của chúng ta | 10 | ✅ sourced |
| 16 | Seasons and the weather | Các mùa và thời tiết | 13 | ✅ sourced |
| 17 | Stories for children | Những câu chuyện dành cho trẻ em | 10 | ✅ sourced |
| 18 | Means of transport | Phương tiện giao thông | 8 | ✅ sourced |
| 19 | Places of interest | Những địa điểm tham quan | 8 | ⚠️ unverified |
| 20 | Our summer holidays | Kỳ nghỉ hè của chúng ta | 7 | ⚠️ unverified |

</details>

<details><summary><b>Lớp 6</b> – Tiếng Anh 6 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | My new school | Ngôi trường mới của tôi | 35 | ⚠️ unverified |
| 2 | My house | Ngôi nhà của tôi | 31 | ⚠️ unverified |
| 3 | My friends | Những người bạn của tôi | 31 | ⚠️ unverified |
| 4 | My neighbourhood | Khu phố của tôi | 33 | ⚠️ unverified |
| 5 | Natural wonders of Viet Nam | Những kỳ quan thiên nhiên của Việt Nam | 28 | ⚠️ unverified |
| 6 | Our Tet holiday | Kỳ nghỉ Tết của chúng ta | 27 | ⚠️ unverified |
| 7 | Television | Truyền hình | 28 | ⚠️ unverified |
| 8 | Sports and games | Thể thao và trò chơi | 31 | ⚠️ unverified |
| 9 | Cities of the world | Các thành phố trên thế giới | 25 | ⚠️ unverified |
| 10 | Our houses in the future | Ngôi nhà của chúng ta trong tương lai | 26 | ⚠️ unverified |
| 11 | Our greener world | Thế giới xanh hơn của chúng ta | 27 | ⚠️ unverified |
| 12 | Robots | Người máy | 26 | ⚠️ unverified |

</details>

<details><summary><b>Lớp 7</b> – Tiếng Anh 7 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | Hobbies | Sở thích | 21 | ⚠️ unverified |
| 2 | Healthy Living | Lối sống lành mạnh | 22 | ⚠️ unverified |
| 3 | Community Service | Phục vụ cộng đồng | 18 | ⚠️ unverified |
| 4 | Music and Arts | Âm nhạc và nghệ thuật | 20 | ⚠️ unverified |
| 5 | Food and Drink | Đồ ăn và thức uống | 20 | ⚠️ unverified |
| 6 | A Visit to a School | Chuyến thăm một ngôi trường | 15 | ⚠️ unverified |
| 7 | Traffic | Giao thông | 19 | ⚠️ unverified |
| 8 | Films | Phim ảnh | 20 | ⚠️ unverified |
| 9 | Festivals around the World | Lễ hội trên khắp thế giới | 20 | ⚠️ unverified |
| 10 | Energy Sources | Các nguồn năng lượng | 21 | ⚠️ unverified |
| 11 | Travelling in the Future | Đi lại trong tương lai | 15 | ⚠️ unverified |
| 12 | English-speaking Countries | Các nước nói tiếng Anh | 19 | ⚠️ unverified |

</details>

<details><summary><b>Lớp 8</b> – Tiếng Anh 8 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | Leisure Time | Thời gian rảnh rỗi | 17 | ⚠️ unverified |
| 2 | Life in the Countryside | Cuộc sống ở nông thôn | 20 | ⚠️ unverified |
| 3 | Teenagers | Thanh thiếu niên | 21 | ⚠️ unverified |
| 4 | Ethnic Groups of Viet Nam | Các dân tộc của Việt Nam | 19 | ⚠️ unverified |
| 5 | Our Customs and Traditions | Phong tục và truyền thống của chúng ta | 17 | ⚠️ unverified |
| 6 | Lifestyles | Lối sống | 16 | ⚠️ unverified |
| 7 | Environmental Protection | Bảo vệ môi trường | 23 | ⚠️ unverified |
| 8 | Shopping | Mua sắm | 17 | ⚠️ unverified |
| 9 | Natural Disasters | Thảm họa thiên nhiên | 27 | ⚠️ unverified |
| 10 | Communication in the Future | Giao tiếp trong tương lai | 21 | ⚠️ unverified |
| 11 | Science and Technology | Khoa học và công nghệ | 18 | ⚠️ unverified |
| 12 | Life on Other Planets | Sự sống trên các hành tinh khác | 24 | ⚠️ unverified |

</details>

<details><summary><b>Lớp 9</b> – Tiếng Anh 9 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | Local community | Cộng đồng địa phương | 41 | ✅ sourced |
| 2 | City life | Cuộc sống thành phố | 22 | ✅ sourced |
| 3 | Healthy living for teens | Sống khỏe cho thanh thiếu niên | 22 | ✅ sourced |
| 4 | Remembering the past | Nhớ về quá khứ | 29 | ✅ sourced |
| 5 | Our experiences | Những trải nghiệm của chúng ta | 25 | ✅ sourced |
| 6 | Vietnamese lifestyle: then and now | Lối sống của người Việt: xưa và nay | 16 | ✅ sourced |
| 7 | Natural wonders of the world | Các kỳ quan thiên nhiên của thế giới | 21 | ✅ sourced |
| 8 | Tourism | Du lịch | 12 | ✅ sourced |
| 9 | World Englishes | Các biến thể tiếng Anh trên thế giới | 30 | ✅ sourced |
| 10 | Planet Earth | Hành tinh Trái Đất | 25 | ✅ sourced |
| 11 | Electronic devices | Thiết bị điện tử | 35 | ✅ sourced |
| 12 | Career choices | Lựa chọn nghề nghiệp | 24 | ✅ sourced |

</details>

<details><summary><b>Lớp 10</b> – Tiếng Anh 10 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | Family life | Cuộc sống gia đình | 39 | ✅ sourced |
| 2 | Humans and the environment | Con người và môi trường | 23 | ✅ sourced |
| 3 | Music | Âm nhạc | 14 | ✅ sourced |
| 4 | For a better community | Vì một cộng đồng tốt đẹp hơn | 12 | ✅ sourced |
| 5 | Inventions | Những phát minh | 12 | ✅ sourced |
| 6 | Gender equality | Bình đẳng giới | 22 | ✅ sourced |
| 7 | Viet Nam and international organisations | Việt Nam và các tổ chức quốc tế | 30 | ✅ sourced |
| 8 | New ways to learn | Những cách học mới | 12 | ✅ sourced |
| 9 | Protecting the environment | Bảo vệ môi trường | 36 | ✅ sourced |
| 10 | Ecotourism | Du lịch sinh thái | 22 | ✅ sourced |

</details>

<details><summary><b>Lớp 11</b> – Tiếng Anh 11 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | A long and healthy life | Cuộc sống lâu dài và khỏe mạnh | 28 | ✅ sourced |
| 2 | The generation gap | Khoảng cách thế hệ | 25 | ✅ sourced |
| 3 | Cities of the future | Thành phố trong tương lai | 26 | ✅ sourced |
| 4 | ASEAN and Viet Nam | ASEAN và Việt Nam | 30 | ✅ sourced |
| 5 | Global warming | Sự nóng lên toàn cầu | 27 | ✅ sourced |
| 6 | Preserving our heritage | Bảo tồn di sản của chúng ta | 30 | ✅ sourced |
| 7 | Education options for school-leavers | Các lựa chọn học tập cho học sinh tốt nghiệp phổ thông | 30 | ✅ sourced |
| 8 | Becoming independent | Trở nên độc lập | 32 | ✅ sourced |
| 9 | Social issues | Các vấn đề xã hội | 35 | ✅ sourced |
| 10 | The ecosystem | Hệ sinh thái | 38 | ✅ sourced |

</details>

<details><summary><b>Lớp 12</b> – Tiếng Anh 12 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | Life stories we admire | Những câu chuyện cuộc đời chúng ta ngưỡng mộ | 34 | ✅ sourced |
| 2 | A multicultural world | Một thế giới đa văn hóa | 31 | ✅ sourced |
| 3 | Green living | Lối sống xanh | 10 | ⚠️ unverified |
| 4 | Urbanisation | Đô thị hóa | 10 | ⚠️ unverified |
| 5 | The world of work | Thế giới việc làm | 10 | ⚠️ unverified |
| 6 | Artificial intelligence | Trí tuệ nhân tạo | 9 | ⚠️ unverified |
| 7 | The world of mass media | Thế giới truyền thông đại chúng | 9 | ⚠️ unverified |
| 8 | Wildlife conservation | Bảo tồn động vật hoang dã | 10 | ⚠️ unverified |
| 9 | Career paths | Con đường sự nghiệp | 7 | ⚠️ unverified |
| 10 | Lifelong learning | Học tập suốt đời | 7 | ⚠️ unverified |

</details>
<!-- AUTO:END -->

## Nguồn và độ chính xác

- **Danh sách từ của mỗi unit** được tổng hợp và đối chiếu từ các trang học liệu phổ biến (VietJack, Loigiaihay, Hoatieu, VnDoc, LangGo, PREP, ZIM, Mytour, 2048.vn, Quizlet…). URL cụ thể nằm trong trường `sources` của từng unit.
  Đây là các nguồn **tổng hợp của bên thứ ba**, không phải bảng Glossary in trong sách, và đôi khi không khớp nhau, nên:
  - một unit có thể **thiếu** vài từ so với sách, hoặc có vài từ sách không liệt kê;
  - các unit lớp 1–2 chỉ gồm các từ trọng tâm theo âm/chữ cái của bài (3–5 từ/unit).
- **Phiên âm IPA UK, từ loại, nghĩa tiếng Việt, câu ví dụ và bản dịch** được biên soạn theo chuẩn từ điển Anh – Anh (Cambridge / Oxford), không chép từ sách. Câu ví dụ được viết theo trình độ từng lớp (lớp 1–2: câu 3–6 từ; lớp 10–12: tối đa ~18 từ), không phải câu trích từ sách. **IPA US** và **giọng đọc** được sinh như mô tả ở mục [Phát âm](#phát-âm-ipa-và-giọng-đọc-uk--us).
- Một số **tên unit** chưa được nguồn nào xác nhận: lớp 1 Unit 8 (*In the park*), lớp 2 Unit 8 (*In the village*).

Nếu bạn có sách giáo khoa trong tay, hãy so với phần **Glossary** cuối sách và sửa giúp (xem bên dưới).

## Đóng góp / sửa dữ liệu

1. Sửa file trong `data/` (không sửa `dist/`).
2. Khi đã đối chiếu xong một unit với sách hoặc nguồn tin cậy: thêm URL / ghi chú vào `sources` và đổi `status` thành `"sourced"`.
3. Nếu thêm từ mới: chạy `ipa_us.py` rồi `make_audio.py`.
4. Chạy lần lượt `validate.py` → `build.py` → `readme_tables.py`.
5. Commit cả `data/`, `audio/`, `dist/` và `README.md`.

---

*Dữ liệu dùng cho mục đích học tập. Tên sách và tên unit thuộc về NXB Giáo dục Việt Nam. IPA Mỹ dựa trên CMU Pronouncing Dictionary (giấy phép BSD); giọng đọc tạo bằng Kokoro-82M (Apache-2.0).*
