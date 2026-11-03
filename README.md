# Từ vựng tiếng Anh Global Success (lớp 1 → 12)

Bộ dữ liệu **từ vựng theo từng unit** của bộ sách giáo khoa **Tiếng Anh Global Success**
(NXB Giáo dục Việt Nam, bộ *Kết nối tri thức với cuộc sống*) từ lớp 1 đến lớp 12, lưu dưới dạng **JSON** (kèm bản **CSV**).

Mỗi từ có: **từ**, **từ loại**, **phiên âm IPA giọng Anh (UK) và giọng Mỹ (US)**, **file giọng đọc UK và US (MP3)**, **nghĩa tiếng Việt** và **câu ví dụ kèm bản dịch tiếng Việt**.

> ⚠️ **Đọc kỹ phần [Trạng thái dữ liệu](#trạng-thái-dữ-liệu) trước khi dùng.**
> Mỗi unit có trường `status`: `official` = lấy trực tiếp từ sách giáo khoa / sách bài tập / sách giáo viên chính thức;
> `sourced` = lấy từ bản chép Glossary hoặc tài liệu giáo viên, hoặc đối chiếu với nhiều nguồn; `unverified` = chưa đối chiếu.

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

- 📗 **`official`**: danh sách từ lấy trực tiếp từ sách chính thức của NXB Giáo dục Việt Nam: bảng **Glossary** cuối SGK hoặc các trang bài học, sách bài tập, sách giáo viên.
- ✅ **`sourced`**: lấy từ **bản chép lại Glossary** (file Wordlist / Luyện viết từ vựng), **tài liệu giáo viên** (giáo án, đề cương, word list theo bài), hoặc đối chiếu nhiều trang học liệu. Rất sát sách nhưng **chưa so từng dòng với trang sách in**.
- ⚠️ **`unverified`**: bản nháp, chưa đối chiếu được.

Lý do nhiều lớp mới ở mức `sourced`: file SGK của các lớp 2–5 và 7–12 trong bộ tài liệu dùng để đối chiếu là **bản scan ảnh**, không trích được chữ, nên phải dùng bản chép Glossary / tài liệu giáo viên đi kèm. Lớp 6 đọc được Glossary nhưng thiếu trang 71 ở cả hai tập.

Một số unit lớp 7 có trường `audit.unconfirmed`: các từ hiện có trong unit nhưng chưa tìm thấy ở nguồn nào.

<!-- AUTO:START -->
| Lớp | Số unit | Số từ | Theo SGK (`official`) | Có nguồn (`sourced`) | Chưa xác minh (`unverified`) | Nguồn chính |
|---:|---:|---:|---|---|---|---|
| 1 | 16 | 60 | 1–16 | – | – | SBT + SGV Tiếng Anh 1 |
| 2 | 16 | 49 | – | 1–16 | – | Tài liệu tập huấn, giáo án, vở luyện từ |
| 3 | 20 | 177 | – | 1–20 | – | Giáo án, mind map |
| 4 | 20 | 205 | – | 1–20 | – | Đề cương ôn tập |
| 5 | 20 | 170 | – | 1–20 | – | Word list theo bài (đối chiếu giáo án) |
| 6 | 12 | 220 | 1–2, 7–8 | 3–6, 9–12 | – | Glossary SGK + trang bài học SGK |
| 7 | 12 | 277 | – | 1–12 | – | Đối chiếu web (VietJack, VnDoc…) |
| 8 | 12 | 274 | – | 1–12 | – | Bản chép Glossary (Luyện viết từ vựng 8) |
| 9 | 12 | 266 | – | 1–12 | – | Bản chép Glossary (Wordlist TA9) |
| 10 | 10 | 222 | – | 1–10 | – | Đối chiếu web |
| 11 | 10 | 244 | – | 1–10 | – | Bản chép Glossary (Wordlist TA11) |
| 12 | 10 | 247 | – | 1–10 | – | Bản chép Glossary (Wordlist TA12) |
| **Tổng** | | **2411** | | | | |

<details><summary><b>Lớp 1</b> – Tiếng Anh 1 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | In the school playground | Ở sân chơi trường học | 3 | 📗 official |
| 2 | In the dining room | Trong phòng ăn | 4 | 📗 official |
| 3 | At the street market | Ở chợ đường phố | 4 | 📗 official |
| 4 | In the bedroom | Trong phòng ngủ | 4 | 📗 official |
| 5 | At the fish and chip shop | Ở cửa hàng cá và khoai tây chiên | 4 | 📗 official |
| 6 | In the classroom | Trong lớp học | 4 | 📗 official |
| 7 | In the garden | Trong vườn | 4 | 📗 official |
| 8 | In the park | Trong công viên | 4 | 📗 official |
| 9 | In the shop | Trong cửa hàng | 4 | 📗 official |
| 10 | At the zoo | Ở vườn thú | 4 | 📗 official |
| 11 | At the bus stop | Ở trạm xe buýt | 4 | 📗 official |
| 12 | At the lake | Ở bờ hồ | 3 | 📗 official |
| 13 | In the school canteen | Ở căng tin trường học | 3 | 📗 official |
| 14 | In the toy shop | Ở cửa hàng đồ chơi | 4 | 📗 official |
| 15 | At the football match | Ở trận bóng đá | 4 | 📗 official |
| 16 | At home | Ở nhà | 3 | 📗 official |

</details>

<details><summary><b>Lớp 2</b> – Tiếng Anh 2 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | At my birthday party | Ở bữa tiệc sinh nhật của tớ | 3 | ✅ sourced |
| 2 | In the backyard | Ở sân sau | 3 | ✅ sourced |
| 3 | At the seaside | Ở bờ biển | 3 | ✅ sourced |
| 4 | In the countryside | Ở nông thôn | 3 | ✅ sourced |
| 5 | In the classroom | Trong lớp học | 3 | ✅ sourced |
| 6 | On the farm | Ở nông trại | 3 | ✅ sourced |
| 7 | In the kitchen | Trong nhà bếp | 3 | ✅ sourced |
| 8 | In the village | Ở ngôi làng | 3 | ✅ sourced |
| 9 | In the grocery store | Ở cửa hàng tạp hóa | 3 | ✅ sourced |
| 10 | At the zoo | Ở vườn thú | 3 | ✅ sourced |
| 11 | In the playground | Ở sân chơi | 3 | ✅ sourced |
| 12 | At the café | Ở quán cà phê | 3 | ✅ sourced |
| 13 | In the maths class | Trong giờ học toán | 4 | ✅ sourced |
| 14 | At home | Ở nhà | 3 | ✅ sourced |
| 15 | In the clothes shop | Ở cửa hàng quần áo | 3 | ✅ sourced |
| 16 | At the campsite | Ở khu cắm trại | 3 | ✅ sourced |

</details>

<details><summary><b>Lớp 3</b> – Tiếng Anh 3 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | Hello | Xin chào | 7 | ✅ sourced |
| 2 | Our names | Tên của chúng mình | 5 | ✅ sourced |
| 3 | Our friends | Bạn bè của chúng mình | 7 | ✅ sourced |
| 4 | Our bodies | Cơ thể của chúng mình | 9 | ✅ sourced |
| 5 | My hobbies | Sở thích của mình | 9 | ✅ sourced |
| 6 | Our school | Trường của chúng mình | 8 | ✅ sourced |
| 7 | Classroom instructions | Hiệu lệnh trong lớp học | 9 | ✅ sourced |
| 8 | My school things | Đồ dùng học tập của mình | 8 | ✅ sourced |
| 9 | Colours | Màu sắc | 9 | ✅ sourced |
| 10 | Break time activities | Hoạt động giờ ra chơi | 9 | ✅ sourced |
| 11 | My family | Gia đình của mình | 15 | ✅ sourced |
| 12 | Jobs | Nghề nghiệp | 9 | ✅ sourced |
| 13 | My house | Ngôi nhà của mình | 10 | ✅ sourced |
| 14 | My bedroom | Phòng ngủ của mình | 9 | ✅ sourced |
| 15 | At the dining table | Bên bàn ăn | 10 | ✅ sourced |
| 16 | My pets | Thú cưng của mình | 9 | ✅ sourced |
| 17 | Our toys | Đồ chơi của chúng mình | 9 | ✅ sourced |
| 18 | Playing and doing | Chơi và làm | 8 | ✅ sourced |
| 19 | Outdoor activities | Hoạt động ngoài trời | 8 | ✅ sourced |
| 20 | At the zoo | Ở vườn thú | 10 | ✅ sourced |

</details>

<details><summary><b>Lớp 4</b> – Tiếng Anh 4 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | My friends | Bạn bè của mình | 8 | ✅ sourced |
| 2 | Time and daily routines | Thời gian và các hoạt động hằng ngày | 12 | ✅ sourced |
| 3 | My week | Tuần của mình | 14 | ✅ sourced |
| 4 | My birthday party | Bữa tiệc sinh nhật của mình | 20 | ✅ sourced |
| 5 | Things we can do | Những việc chúng mình có thể làm | 10 | ✅ sourced |
| 6 | Our school facilities | Cơ sở vật chất trường chúng mình | 8 | ✅ sourced |
| 7 | Our timetables | Thời khóa biểu của chúng mình | 10 | ✅ sourced |
| 8 | My favourite subjects | Môn học yêu thích của mình | 8 | ✅ sourced |
| 9 | Our sports day | Ngày hội thể thao của chúng mình | 4 | ✅ sourced |
| 10 | Our summer holidays | Kỳ nghỉ hè của chúng mình | 8 | ✅ sourced |
| 11 | My home | Nhà của mình | 9 | ✅ sourced |
| 12 | Jobs | Nghề nghiệp | 10 | ✅ sourced |
| 13 | Appearance | Ngoại hình | 8 | ✅ sourced |
| 14 | Daily activities | Hoạt động hằng ngày | 10 | ✅ sourced |
| 15 | My family's weekends | Những ngày cuối tuần của gia đình mình | 12 | ✅ sourced |
| 16 | Weather | Thời tiết | 14 | ✅ sourced |
| 17 | In the city | Ở thành phố | 10 | ✅ sourced |
| 18 | At the shopping centre | Ở trung tâm mua sắm | 12 | ✅ sourced |
| 19 | The animal world | Thế giới động vật | 10 | ✅ sourced |
| 20 | At summer camp | Ở trại hè | 8 | ✅ sourced |

</details>

<details><summary><b>Lớp 5</b> – Tiếng Anh 5 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | All about me! | Tất cả về tôi | 7 | ✅ sourced |
| 2 | Our homes | Nhà của chúng ta | 8 | ✅ sourced |
| 3 | My foreign friends | Những người bạn nước ngoài của tôi | 9 | ✅ sourced |
| 4 | Our free-time activities | Các hoạt động thời gian rảnh của chúng ta | 8 | ✅ sourced |
| 5 | My future job | Công việc tương lai của tôi | 8 | ✅ sourced |
| 6 | Our school rooms | Các phòng học ở trường của chúng ta | 8 | ✅ sourced |
| 7 | Our favourite school activities | Các hoạt động ở trường mà chúng ta yêu thích | 8 | ✅ sourced |
| 8 | In our classroom | Trong lớp học của chúng ta | 8 | ✅ sourced |
| 9 | Our outdoor activities | Các hoạt động ngoài trời của chúng ta | 8 | ✅ sourced |
| 10 | Our school trip | Chuyến đi của trường chúng ta | 8 | ✅ sourced |
| 11 | Family time | Thời gian bên gia đình | 8 | ✅ sourced |
| 12 | Our Tet holiday | Kỳ nghỉ Tết của chúng ta | 9 | ✅ sourced |
| 13 | Our special days | Những ngày đặc biệt của chúng ta | 8 | ✅ sourced |
| 14 | Staying healthy | Giữ gìn sức khỏe | 10 | ✅ sourced |
| 15 | Our health | Sức khỏe của chúng ta | 8 | ✅ sourced |
| 16 | Seasons and the weather | Các mùa và thời tiết | 11 | ✅ sourced |
| 17 | Stories for children | Những câu chuyện dành cho trẻ em | 12 | ✅ sourced |
| 18 | Means of transport | Phương tiện giao thông | 8 | ✅ sourced |
| 19 | Places of interest | Những địa điểm tham quan | 8 | ✅ sourced |
| 20 | Our summer holidays | Kỳ nghỉ hè của chúng ta | 8 | ✅ sourced |

</details>

<details><summary><b>Lớp 6</b> – Tiếng Anh 6 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | My new school | Ngôi trường mới của tôi | 15 | 📗 official |
| 2 | My house | Ngôi nhà của tôi | 18 | 📗 official |
| 3 | My friends | Những người bạn của tôi | 17 | ✅ sourced |
| 4 | My neighbourhood | Khu phố của tôi | 22 | ✅ sourced |
| 5 | Natural wonders of Viet Nam | Những kỳ quan thiên nhiên của Việt Nam | 21 | ✅ sourced |
| 6 | Our Tet holiday | Kỳ nghỉ Tết của chúng ta | 19 | ✅ sourced |
| 7 | Television | Truyền hình | 19 | 📗 official |
| 8 | Sports and games | Thể thao và trò chơi | 18 | 📗 official |
| 9 | Cities of the world | Các thành phố trên thế giới | 15 | ✅ sourced |
| 10 | Our houses in the future | Ngôi nhà của chúng ta trong tương lai | 16 | ✅ sourced |
| 11 | Our greener world | Thế giới xanh hơn của chúng ta | 18 | ✅ sourced |
| 12 | Robots | Người máy | 22 | ✅ sourced |

</details>

<details><summary><b>Lớp 7</b> – Tiếng Anh 7 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | Hobbies | Sở thích | 25 | ✅ sourced |
| 2 | Healthy Living | Lối sống lành mạnh | 23 | ✅ sourced |
| 3 | Community Service | Phục vụ cộng đồng | 25 | ✅ sourced |
| 4 | Music and Arts | Âm nhạc và nghệ thuật | 24 | ✅ sourced |
| 5 | Food and Drink | Đồ ăn và thức uống | 22 | ✅ sourced |
| 6 | A Visit to a School | Chuyến thăm một ngôi trường | 18 | ✅ sourced |
| 7 | Traffic | Giao thông | 23 | ✅ sourced |
| 8 | Films | Phim ảnh | 27 | ✅ sourced |
| 9 | Festivals around the World | Lễ hội trên khắp thế giới | 25 | ✅ sourced |
| 10 | Energy Sources | Các nguồn năng lượng | 23 | ✅ sourced |
| 11 | Travelling in the Future | Đi lại trong tương lai | 17 | ✅ sourced |
| 12 | English-speaking Countries | Các nước nói tiếng Anh | 25 | ✅ sourced |

</details>

<details><summary><b>Lớp 8</b> – Tiếng Anh 8 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | Leisure time | Thời gian rảnh rỗi | 22 | ✅ sourced |
| 2 | Life in the countryside | Cuộc sống ở nông thôn | 23 | ✅ sourced |
| 3 | Teenagers | Thanh thiếu niên | 22 | ✅ sourced |
| 4 | Ethnic groups of Viet Nam | Các dân tộc của Việt Nam | 22 | ✅ sourced |
| 5 | Our customs and traditions | Phong tục và truyền thống của chúng ta | 24 | ✅ sourced |
| 6 | Lifestyles | Lối sống | 25 | ✅ sourced |
| 7 | Environmental protection | Bảo vệ môi trường | 18 | ✅ sourced |
| 8 | Shopping | Mua sắm | 20 | ✅ sourced |
| 9 | Natural disasters | Thảm họa thiên nhiên | 26 | ✅ sourced |
| 10 | Communication in the future | Giao tiếp trong tương lai | 23 | ✅ sourced |
| 11 | Science and technology | Khoa học và công nghệ | 28 | ✅ sourced |
| 12 | Life on other planets | Sự sống trên các hành tinh khác | 21 | ✅ sourced |

</details>

<details><summary><b>Lớp 9</b> – Tiếng Anh 9 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | Local community | Cộng đồng địa phương | 25 | ✅ sourced |
| 2 | City life | Cuộc sống thành phố | 21 | ✅ sourced |
| 3 | Healthy living for teens | Sống khỏe cho thanh thiếu niên | 19 | ✅ sourced |
| 4 | Remembering the past | Nhớ về quá khứ | 21 | ✅ sourced |
| 5 | Our experiences | Những trải nghiệm của chúng ta | 24 | ✅ sourced |
| 6 | Vietnamese lifestyles: then and now | Lối sống của người Việt: xưa và nay | 21 | ✅ sourced |
| 7 | Natural wonders of the world | Các kỳ quan thiên nhiên của thế giới | 21 | ✅ sourced |
| 8 | Tourism | Du lịch | 24 | ✅ sourced |
| 9 | World Englishes | Các biến thể tiếng Anh trên thế giới | 25 | ✅ sourced |
| 10 | Planet Earth | Hành tinh Trái Đất | 22 | ✅ sourced |
| 11 | Electronic devices | Thiết bị điện tử | 21 | ✅ sourced |
| 12 | Career choices | Lựa chọn nghề nghiệp | 22 | ✅ sourced |

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
| 1 | A long and healthy life | Cuộc sống lâu dài và khỏe mạnh | 33 | ✅ sourced |
| 2 | The generation gap | Khoảng cách thế hệ | 20 | ✅ sourced |
| 3 | Cities of the future | Thành phố trong tương lai | 20 | ✅ sourced |
| 4 | ASEAN and Viet Nam | ASEAN và Việt Nam | 25 | ✅ sourced |
| 5 | Global warming | Sự nóng lên toàn cầu | 26 | ✅ sourced |
| 6 | Preserving our heritage | Bảo tồn di sản của chúng ta | 22 | ✅ sourced |
| 7 | Education options for school-leavers | Các lựa chọn học tập cho học sinh tốt nghiệp phổ thông | 18 | ✅ sourced |
| 8 | Becoming independent | Trở nên độc lập | 27 | ✅ sourced |
| 9 | Social issues | Các vấn đề xã hội | 31 | ✅ sourced |
| 10 | The ecosystem | Hệ sinh thái | 22 | ✅ sourced |

</details>

<details><summary><b>Lớp 12</b> – Tiếng Anh 12 – Global Success</summary>

| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |
|---:|---|---|---:|---|
| 1 | Life stories we admire | Những câu chuyện cuộc đời chúng ta ngưỡng mộ | 33 | ✅ sourced |
| 2 | A multicultural world | Một thế giới đa văn hóa | 28 | ✅ sourced |
| 3 | Green living | Lối sống xanh | 22 | ✅ sourced |
| 4 | Urbanisation | Đô thị hóa | 16 | ✅ sourced |
| 5 | The world of work | Thế giới việc làm | 20 | ✅ sourced |
| 6 | Artificial intelligence | Trí tuệ nhân tạo | 23 | ✅ sourced |
| 7 | The world of mass media | Thế giới truyền thông đại chúng | 30 | ✅ sourced |
| 8 | Wildlife conservation | Bảo tồn động vật hoang dã | 28 | ✅ sourced |
| 9 | Career paths | Con đường sự nghiệp | 23 | ✅ sourced |
| 10 | Lifelong learning | Học tập suốt đời | 24 | ✅ sourced |

</details>
<!-- AUTO:END -->

## Nguồn và độ chính xác

- **Danh sách từ** của mỗi unit lấy từ bộ tài liệu Global Success lớp 1–12 (SGK, SBT, SGV, giáo án, wordlist) được chia sẻ công khai trên Google Drive. Cụ thể từng lớp xem cột *Nguồn chính* ở bảng trên và trường `sources` của từng unit. Lớp 7 và lớp 10 chưa có bản Glossary đọc được nên vẫn dựa trên đối chiếu các trang học liệu (VietJack, VnDoc, LangGo, ZIM…).
- **Nghĩa tiếng Việt** và **phiên âm UK** của các lớp lấy từ Glossary/wordlist được giữ theo nguồn. Chỉ sửa lỗi gõ, lỗi nhận dạng chữ (OCR) và vài nghĩa sai rõ ràng (ví dụ *intelligence* "tình báo" → "trí thông minh, trí tuệ" trong unit về AI).
- Lớp 1–2 chỉ gồm các **từ trọng tâm theo âm/chữ cái** của bài (3–4 từ/unit). Unit lớp 1–2 có thêm `letter_sound` (âm/chữ cái) và `patterns` (mẫu câu của bài).
- **Câu ví dụ và bản dịch** do Claude viết theo trình độ từng lớp (lớp 1–2: câu 3–6 từ; lớp 10–12: tối đa ~18 từ), không phải câu trích từ sách. **IPA US** và **giọng đọc** được sinh như mô tả ở mục [Phát âm](#phát-âm-ipa-và-giọng-đọc-uk--us).

Để đạt mức `official` cho tất cả các lớp, cần một bản SGK **có lớp chữ** (PDF tìm được chữ) hoặc ảnh chụp các trang Glossary cuối sách. Nếu bạn có, gửi vào là có thể đối chiếu từng dòng.

## Đóng góp / sửa dữ liệu

1. Sửa file trong `data/` (không sửa `dist/`).
2. Khi đã đối chiếu xong một unit với sách hoặc nguồn tin cậy: thêm URL / ghi chú vào `sources` và đổi `status` thành `"sourced"`.
3. Nếu thêm từ mới: chạy `ipa_us.py` rồi `make_audio.py`.
4. Chạy lần lượt `validate.py` → `build.py` → `readme_tables.py`.
5. Commit cả `data/`, `audio/`, `dist/` và `README.md`.

---

*Dữ liệu dùng cho mục đích học tập. Tên sách và tên unit thuộc về NXB Giáo dục Việt Nam. IPA Mỹ dựa trên CMU Pronouncing Dictionary (giấy phép BSD); giọng đọc tạo bằng Kokoro-82M (Apache-2.0).*
