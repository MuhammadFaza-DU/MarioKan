# Checkpoint — Progres & Riwayat Kerja

File ini adalah **satu-satunya sumber progres** proyek. Setiap sesi kerja
menambah entri. Tujuannya: siapa pun (manusia atau agent) bisa tahu posisi
proyek tanpa membaca ulang seluruh riwayat chat.

## Cara pakai

- Tambah entri **di paling atas** (terbaru dulu).
- Format: `## YYYY-MM-DD — <judul singkat>`
- Isi minimal: apa yang dikerjakan, **bukti** (SIM/SYN/BOARD), apa yang gagal,
  apa langkah berikutnya.
- Jangan hapus entri lama. Kalau ada koreksi, tulis koreksinya sebagai entri baru.
- Kalau sesuatu belum dites, tulis "belum dites" — jangan dihilangkan.

---

## 2026-10-22 (lanjutan 2) — Nama final proposal ditetapkan (rename)

**Keputusan pemilik**
Nama file proposal final = **`Proposal_P1_Muhammad Faza Difa'ulhaq.pdf`**
(format yang dipakai saat mengunggah ke BRONE, sama dengan nama saat pertama
dikirim). Nama-nama iterasi `rev` / `rev2` / `rev3` **tidak dipakai lagi**.

**Dikerjakan**
- `docs/proposal/Proposal-P1-MarioKan-rev3-2026-10-22.pdf` →
  `docs/proposal/Proposal_P1_Muhammad Faza Difa'ulhaq.pdf` (isi byte-identik,
  274.168 B, tidak ada perubahan dokumen).
- Entri checkpoint sebelumnya ditandai koreksinya (lihat catatan *Koreksi nama*
  di dua entri 2026-10-22 di bawah) agar penamaan tidak ambigu.

**Kondisi `docs/proposal/` sekarang (satu-satunya yang ada)**

```
docs/proposal/Proposal_P1_Muhammad Faza Difa'ulhaq.pdf   274.168 B  <- FINAL
docs/proposal/gambar/diagram-blok.png                    114.008 B  <- sumber Gambar 1
```

**Bukti**
- `Get-ChildItem docs\proposal -Recurse -File` → hanya 2 file di atas.
- Ukuran 274.168 B sama persis dengan `rev3` sebelum rename → rename murni,
  tidak ada kerusakan/regenerasi.
- Root repo tetap 5 file publik; `git status` bersih (folder `docs/proposal/`
  gitignored).

**Berikutnya**
- ~~Sinkronkan Q13.8 ke `docs/PRD.md` §4.5 dan `README.md`~~
  → **SUDAH DIKERJAKAN** 2026-10-22 (lanjutan 4, lihat entri paling atas).

---

## 2026-10-22 (lanjutan 4) — Q12.8 → Q13.8 disinkronkan ke PRD + README

**Latar**
Proposal final sudah memakai **Q13.8**, tetapi `docs/PRD.md` §4.5 dan
`README.md` masih menulis **Q12.8** — klaim yang **salah aritmetika**:
20-bit signed Q12.8 hanya menjangkau ±2.047,996, sedangkan level terlebar
212 metatile × 16 px = 3.392 px. Ini inkonsistensi terakhir yang tersisa
setelah proposal dibereskan.

**Dikerjakan**
- `docs/PRD.md` §4.5 (baris 361–368):
  - `Q12.8 (20-bit signed)` → **`Q13.8 (21-bit signed: 1 sign + 12 integer + 8 fraksi)`**
  - ditambah jangkauan eksplisit **±4.095,996** + headroom **703,996 px**
  - ditambah catatan bahwa Q12.8 **tidak cukup** (bukan hanya Q8.8)
  - baris konversi koordinat layar: `Q12.8` → `Q13.8`
- `docs/PRD.md` §6 tabel deviasi **D-10**: keputusan diubah ke Q13.8 +
  kolom alasan mencatat riwayat koreksinya (Q12.8 sempat dipakai, dikoreksi
  2026-10-22).
- `README.md` (baris 32–35): `Q12.8` → **`Q13.8`**, ditambah penjelasan singkat
  21-bit signed, ±4095.996 px, dan mengapa Q12.8 gagal.

**Bukti aritmetika (dihitung, bukan dikira)**
```
Q13.8  21-bit signed : min -4096.000000  max 4095.996094  ->  +-4095.996
Q12.8  20-bit signed : min -2048.000000  max 2047.996094  ->  +-2047.996
Q8.8   16-bit signed : min  -128.000000  max  127.996094  ->   +-127.996
level terlebar : 212 x 16 = 3392 px
Q13.8 headroom : 703.996094 px   -> cukup
Q12.8 cukup    : False
```

**Sisa penyebutan `Q12.8` (sengaja, bukan inkonsistensi)**
- `docs/checkpoint.md` — entri-entri historis di bawah, memang mencatat
  temuan saat itu.
- `docs/PRD.md` baris 364 & 522 — disebut sebagai **pembanding** ("Q12.8 tidak
  cukup") dan sebagai **riwayat koreksi** di D-10. Bukan klaim aktif.

**Berikutnya**
- Tidak ada pekerjaan dokumen yang tertunda. Berikutnya = mulai RTL fase 1
  (analisis modul repo acuan) setelah judul disetujui dosen.

---

## 2026-10-22 (lanjutan 3) — Metadata PDF dibersihkan

**Latar**
Metadata internal PDF final masih menyimpan nama kerja lama:
`title = "Proposal-Proyek-1-MarioKan_Rev - Google Dokumen"`. Kalau dosen membuka
*Properties* di PDF reader, yang muncul nama draf, bukan judul proposal.

**Dikerjakan** (`PyMuPDF`, script di `.tmp/` — scratch, tidak di-commit)
- `title` → `Proposal Proyek Akhir - MarioKan: Implementasi Game Platformer
  Bergaya Super Mario Bros Berbasis FPGA Basys 3 dengan Bahasa VHDL`
- `author` → 7 nama anggota (dipisah `;`)
- `subject` → `Proposal Proyek 1 - Mata Kuliah Sistem Digital Lanjut`
- `keywords` → `FPGA; Basys 3; Artix-7 XC7A35T; VHDL; game platformer; 1920x1080; MarioKan`
- `creator` / `producer` / `creationDate` **dibiarkan apa adanya** (jujur:
  Chrome + Skia/PDF m155 = memang ekspor Google Docs). Tidak dipalsukan.

**Jebakan yang ditemukan (penting untuk siapa pun yang mengedit PDF ini)**
1. `saveIncr()` → metadata tampil baru, **tetapi objek lama tetap ada di byte
   file**; `strings`/grep masih menemukan `MarioKan_Rev`. Tidak cukup.
2. `save(..., clean=True)` → **MERUSAK RENDERING**. Terukur: 2,5%–10,6% piksel
   berbeda per halaman pada dpi 110; spasi antar kata hilang sehingga teks
   terbaca `DENGANBAHASAVHDLkarena`. **Jangan dipakai.**
3. `save(..., garbage=4, deflate=True)` **tanpa `clean`** → satu-satunya opsi
   yang benar: piksel **identik 12/12 halaman**, teks identik, string lama
   **hilang total**, ukuran 274.168 → 273.904 B.

**Bukti (semua terverifikasi, bukan asumsi)**
- `piksel identik = True` untuk 12 halaman @ dpi 110 (perbandingan
  `pixmap.samples` per halaman terhadap file sebelum diedit).
- `teks identik = True` (ekstraksi text-layer per halaman).
- Pencarian byte: `MarioKan_Rev` / `Google Dokumen` / `Proposal-Proyek-1-MarioKan`
  → **semuanya False**.
- Metadata akhir: title/author/subject/keywords sesuai di atas.
- Isi dokumen tetap: `seg[6:0], an[3:0]`, `W7/U7/U2/W4`, `U16 (led[0]) … L1`,
  `Q13.8` ada, `Q12.8` tidak ada, `Disusun Oleh` ada, `Disusuh` tidak ada,
  12 halaman, 2.026 kata.
- Render halaman 7 + OCR: tabel pin terbaca benar (baris seven-segment cocok).

**Cadangan**
- `.tmp/backup_before_metadata.pdf` (274.168 B) = PDF asli **sebelum** metadata
  diedit. Ada di `.tmp/` yang gitignored → **tidak ikut ter-commit**. Hapus
  kalau sudah yakin.

**Berikutnya**
- ~~Sama seperti entri sebelumnya (sinkron Q13.8 ke PRD + README)~~
  → **SUDAH DIKERJAKAN** 2026-10-22 (lanjutan 4).

---

## 2026-10-22 — Review proposal revisi pemilik vs rubrik + relokasi file

> **Koreksi nama (2026-10-22, lanjutan 2):** file hasil relokasi di entri ini
> sempat bernama `Proposal-P1-MarioKan-rev-2026-10-22.pdf`, lalu **dihapus**.
> Nama final yang berlaku sekarang: `Proposal_P1_Muhammad Faza Difa'ulhaq.pdf`.

**Dikerjakan**
- Membaca proposal revisi pemilik (ekspor Google Docs, 12 halaman, 2.012 kata,
  berjudul internal `Proposal-Proyek-1-MarioKan_Rev`) dan membandingkannya
  dengan `docs/rubrik.md`, `docs/PRD.md`, `README.md`, serta versi lama
  (`docs/proposal/Proposal-Proyek-1-MarioKan.pdf`, 10 halaman, 2.487 kata).
  > **Catatan (2026-10-22):** file pembanding ini **sudah dihapus**; angka
  > 10 hal / 2.487 kata dipertahankan sebagai riwayat pengukuran.
- Memindahkan PDF dari **root repo** ke `docs/proposal/` sebagai
  `Proposal-P1-MarioKan-rev-2026-10-22.pdf`. Root sebelumnya memuat dokumen
  akademik yang **belum di-ignore** → satu `git add -A` bisa membocorkannya ke
  repo publik.

**Bukti**
- `git status --untracked-files=all` → **bersih** setelah relokasi.
- Root kini hanya 5 file publik: `.gitattributes`, `.gitignore`, `AGENTS.md`,
  `CONTRIBUTING.md`, `README.md`.
- Tabel pin proposal dicek baris per baris terhadap
  `Basys-3-Master.xdc` resmi Digilent (diunduh, disimpan di `.tmp/`):
  clk/VGA/Hsync/Vsync/PS2/sw/btn/JA **cocok**; baris **LED** dan
  **seven-segment** salah urutan.

**Temuan (diserahkan ke pemilik untuk diperbaiki sendiri)**
- Typo hal. 1 `Disusuh` → `Disusun`.
- `led[15:0] U16 … L1` seharusnya `led[0]=U16 … led[15]=L1`;
  `seg[6:0], an[3:0] W7 … U2` seharusnya `seg[0]=W7…seg[6]=U7`,
  `an[0]=U2…an[3]=W4`.
- Klaim "Q12.8 (20 bit bertanda) menjangkau 3.392 px" **salah aritmetika**:
  20-bit signed Q12.8 maks ±2.047,996. Perlu Q13.8 (21-bit) atau x unsigned.
  Klaim sama ada di PRD §4.5 dan README → **belum diperbaiki**, menunggu
  keputusan pemilik.
- Caption Gambar 1 menumpuk tepi bawah gambar (bbox gambar berakhir y=625,0 pt,
  caption mulai y=620,1 pt → overlap ±4,9 pt).
- Label diagram efektif ≈4,6 pt saat dicetak (gambar 2046×1060 px di 15,09 cm).
- Tabel pecah halaman tanpa header berulang; satu header yatim (hal. 9).
- Cover kehilangan "Mata Kuliah: Sistem Digital Lanjut" + "S1".
- Judul §3 "Gambaran Kerja" ≠ istilah rubrik "Gambaran cara kerja".
- Tidak ada sitasi dalam teks meski daftar pustaka 10 entri; tidak ada
  pernyataan orisinalitas/atribusi aset.

**Status penilaian (pendapat, bukan nilai dosen)**
Keempat komponen rubrik (20/25/25/30) menurut penilaian reviewer berada di
**Level 5**; kekurangan ada di detail teknis & format, bukan substansi.

**Berikutnya**
- Pemilik memperbaiki sendiri di Google Docs → menyerahkan versi benar.
- ~~Menunggu keputusan: Q13.8 vs unsigned 20-bit~~ → **sudah diputuskan Q13.8**
  (dipakai di proposal final).
- ~~Sinkronkan ke `docs/PRD.md` §4.5 dan `README.md`~~
  → **SUDAH DIKERJAKAN** 2026-10-22 (lanjutan 4).

---

## 2026-10-22 (lanjutan) — Proposal FINAL ditetapkan + file lama dihapus

> **Koreksi nama (2026-10-22, lanjutan 2):** entri ini memakai label iterasi
> `rev`/`rev2`/`rev3` sebagai penanda kerja, **bukan** nama file final. Nama file
> final sekarang: `docs/proposal/Proposal_P1_Muhammad Faza Difa'ulhaq.pdf`
> (= isi `rev3`). Label iterasi di bawah dipertahankan sebagai riwayat.

**Latar**
Pemilik menyerahkan tiga iterasi perbaikan di hari yang sama. Iterasi ketiga
(`rev3`, 12 hal, 2.026 kata, dibuat 07:18 UTC) dinyatakan **final**.

**Riwayat iterasi (semua terverifikasi dari text-layer PDF)**

| Iterasi | Dibuat | Yang berubah |
|---|---|---|
| `rev` | 06:37 UTC | versi pertama dari pemilik (2.012 kata) |
| `rev2` | 07:05 UTC | `Disusuh`→`Disusun`, LED `U16 (led[0]) … L1 (led[15])`, Q12.8→**Q13.8** (hal. 5 & 9), tabel 4.1 jadi 1 halaman (font 10 pt) — **tapi kolom seg/an tertukar** |
| `rev3` | 07:18 UTC | kolom seven-segment dibetulkan: Sinyal `seg[6:0], an[3:0]`, Pin `W7 … U7 (seg), U2 … W4 (an)` |

**Dikerjakan**
- `docs/proposal/` dibersihkan atas instruksi pemilik. **Dihapus (4 file):**
  `Proposal-P1-MarioKan-rev-2026-10-22.pdf`,
  `Proposal-P1-MarioKan-rev2-2026-10-22.pdf`,
  `Proposal-Proyek-1-MarioKan.docx`, `Proposal-Proyek-1-MarioKan.pdf`
  (dua terakhir = deliverable lama 2026-10-19, 10 hal).
- **Tersisa saat itu:** `Proposal-P1-MarioKan-rev3-2026-10-22.pdf` (274.168 B)
  + `gambar/diagram-blok.png`. → **Sudah di-rename** jadi
  `Proposal_P1_Muhammad Faza Difa'ulhaq.pdf` (lihat entri lanjutan 2 di atas).

**Bukti**
- Tabel pin §4.1 `rev3` dicek ulang ke `Basys-3-Master.xdc`: baris
  seven-segment **cocok penuh** (`seg[0]=W7`…`seg[6]=U7`, `an[0]=U2`…`an[3]=W4`).
  Seluruh tabel pin kini **0 error**.
- `git status` bersih; root repo tetap 5 file publik.

**Cacat yang MASIH ADA di versi final (diketahui, diterima pemilik)**

> Berlaku untuk file final `Proposal_P1_Muhammad Faza Difa'ulhaq.pdf`.
> Semua terverifikasi ulang dari PDF final, bukan dari ingatan.

- Caption Gambar 1 masih menumpuk gambar (overlap **4,9 pt**).
- Daftar pustaka keluar margin kiri **1,27 cm** (entri di x=72 pt, body x=108 pt).
- Header tabel belum berulang (hal. 4, 8, 10, 11) + header yatim hal. 9.
- Kata `Seven-segmen` / `t` terpotong di kolom Perangkat.
- `±4.095,99` (eksaknya 4.095,996); `XC7A35TCpg236-1` (gaya beda).
- Judul §3 `Gambaran Kerja` ≠ istilah rubrik; cover tanpa `Mata Kuliah`/`S1`.
- Audio masih di kolom "Termasuk dalam proyek".
- **0 sitasi dalam teks** meski daftar pustaka 10 entri.

**Sudah benar di versi final (jangan diperbaiki lagi)**
- `Disusun Oleh` (bukan `Disusuh`).
- Tabel pin §4.1: `led[15:0]` → `U16 (led[0]) … L1 (led[15])`.
- Tabel pin §4.1: `seg[6:0], an[3:0]` → `W7 … U7 (seg), U2 … W4 (an)`.
- Fixed-point **Q13.8** (hal. 5 §3.2 dan hal. 9 §4.3.4) — bukan Q12.8 lagi.

**Berikutnya**
- ~~Sinkronkan Q13.8 ke `docs/PRD.md` §4.5 dan `README.md`~~
  → **SUDAH DIKERJAKAN** 2026-10-22 (lanjutan 4).
- Deliverable lama DOCX/PDF terhapus; bisa diregenerasi dari
  `tools/make_proposal.py` (34 KB, ada di disk, gitignored) bila diperlukan.

---

## 2026-10-19 (lanjutan 6) — `tools/make_proposal.py` dikeluarkan dari repo publik

**Latar**
Script generator proposal memuat teks proposal lengkap + daftar nama/NIM
anggota. Meski terlihat seperti tooling, isinya praktis membocorkan dokumen
akademik dalam bentuk kode. Pemilik memutuskan mengeluarkannya.

**Dikerjakan**
- `tools/make_proposal.py` di-`git rm --cached` dan masuk `.gitignore`.
  **File tetap ada di disk** (34.805 bytes) untuk dipakai pemilik.
- Riwayat ditulis ulang (`git filter-branch --index-filter`, 13 commit) agar
  script hilang dari seluruh riwayat, bukan hanya commit terakhir.
- Ketiga tag dibuat ulang agar menunjuk riwayat baru (sebelumnya masih
  menunjuk commit lama yang memuat script — sumber kebocoran).
- `README.md`: entri `make_proposal.py` dihapus dari daftar tools, ditambahkan
  ke daftar materi lokal.

**Bukti**
- `git rev-list --all --objects` → **tidak ada** objek bernama
  `make_proposal`, `rubrik`, `docs/brief/`, atau `docs/proposal/`.
- Tag diverifikasi menunjuk riwayat baru:
  `v1 → d575ef0`, `v2 → 623a117`, `v3 → c4d405f`.
- Force-push main + 3 tag sukses; `git ls-remote` mengonfirmasi remote.
- Tree publik (anonim, tanpa login) — **11 file**, tanpa satu pun dokumen
  akademik:
  `.gitattributes`, `.gitignore`, `AGENTS.md`, `CONTRIBUTING.md`, `README.md`,
  `docs/PRD.md`, `docs/checkpoint.md`, `docs/diagram/arsitektur.svg`,
  `tools/build.tcl`, `tools/make_architecture.py`, `tools/make_diagram.py`

**File lokal (tidak di-commit) — terverifikasi utuh**
`docs/rubrik.md` 3,3 KB · `docs/brief/ide-awal.md` 27,3 KB ·
`docs/brief/proyek-1.pdf` 201,9 KB · `docs/proposal/*.docx` 148,7 KB ·
`docs/proposal/*.pdf` 214,0 KB · `docs/proposal/gambar/diagram-blok.png`
111,3 KB · `tools/make_proposal.py` 34,0 KB

**Catatan**
- `reset --hard` dari `filter-branch` **tidak** menghapus file lokal kali ini,
  karena file akademik sudah berstatus untracked sejak pembersihan sebelumnya.
  Tetap di-backup lebih dulu sebagai pengaman.
- Pemilik akan mengganti `make_proposal.py` dengan versi bersih nanti
  (mis. template tanpa data anggota).

**Berikutnya**
- Menunggu: judul disepakati kelompok, deadline BRONE, model konverter
  VGA→HDMI → lalu fase 1 (analisis modul repo acuan).

---

## 2026-10-19 (lanjutan 5) — Audit lingkup kerja: git terisolasi, tidak ada file luar tersentuh

**Latar**
Pemilik menanyakan dua hal yang perlu dibuktikan, bukan diyakinkan:
(a) apakah ada dokumen akademik di luar folder project yang ikut terhapus,
(b) apakah `.git` menyebar ke folder lain.

**Hasil audit (semua terverifikasi)**

| Pemeriksaan | Hasil |
|---|---|
| `.git` di folder project | **ADA** — `...\Project-Terakhir-SDL\.git`, HEAD `refs/heads/main` |
| `.git` di folder induk (`VHDL`, `Project dan SourceCode`, `D:\Progamming`, `D:\`) | **TIDAK ADA** sama sekali |
| File di luar project yang terhapus | **TIDAK ADA** |
| `C:\Users\...\Downloads\Tugas 2 Conditional Programming_*.pdf` | **UTUH** |
| `WEBB\gamein`, `Aplikasi\Tazk`, `MATLAB`, `Lomba`, `Tes model`, `BEBAS CAMPURAN`, `Project C` | **SEMUA ADA** |
| Commit terakhir repo lain | Tazk `1a682e2` (2026-08-24), gamein `e55ddc2` (2026-10-19), Project_1 `1223b39` (2026-10-10) → **tidak berubah**, membuktikan tidak tersentuh |
| Operasi hapus sepanjang sesi | Hanya 3, semuanya di dalam project: `Remove-Item` PDF proposal (sebelum regenerate), `Move-Item` log Vivado ke `.tmp/`, `Rename-Item` folder project (gagal, ditunda) |
| Cakupan `git filter-branch --all` | Hanya ref **repo ini**: `refs/heads/main`, `refs/remotes/origin/main`, `refs/tags/stable-2026-10-19-v1`. Bukan repo lain di disk |

**Catatan teknis penting**
- `git rm -r --cached` hanya mengeluarkan dari index, **tidak** menghapus dari disk.
  Yang menghapus adalah efek samping `reset --hard` di akhir `filter-branch`,
  dan itu **terbatas di dalam repo ini**. Sudah dipulihkan penuh dari
  `.tmp/backup-akademik/`.
- Semua perintah git dijalankan dengan working directory = folder project ini;
  tidak pernah `cd` ke folder lain untuk urusan git.

**Status akhir**
- 19 file di project: 12 ter-track (publik) + 7 lokal (rubrik, brief ×2,
  proposal ×2, diagram, backup) — semuanya ada dan ukurannya sesuai.
- `git status` bersih → dokumen lokal tidak ter-track.

**Berikutnya**
- Menunggu keputusan: `tools/make_proposal.py` tetap publik atau dikeluarkan.
- Menunggu: judul disepakati kelompok, deadline BRONE, model konverter
  VGA→HDMI → lalu fase 1.

---

## 2026-10-19 (lanjutan 4) — Repo dijadikan PUBLIK + riwayat dibersihkan

**Dikerjakan**
- Repo diubah dari private → **PUBLIC** atas permintaan pemilik.
- Dokumen akademik dikeluarkan dari repo dan dari **seluruh riwayat git**:
  `docs/rubrik.md`, `docs/brief/`, `docs/proposal/`, dan `Ide-awal.md` (nama
  awal sebelum dipindah). Ditambahkan ke `.gitignore` (lokal-only).
- Riwayat ditulis ulang dengan `git filter-branch --index-filter` (10 commit),
  lalu `refs/original` dihapus, reflog di-expire, `git gc --prune=now`.
- Tag `stable-2026-10-19-v1` dibuat ulang di riwayat baru (menunjuk `0b76a83`).
- Proposal diregenerasi dengan **7 anggota** (tambah Irwanto Saputra Husni,
  255150300111001).

**Bukti**
- `gh repo view --json visibility` → `"PUBLIC"`, `isPrivate: false`
- Akses **anonim tanpa login**: `HTTP 200 | private=False | visibility=public`
- Tree publik (12 file): `.gitattributes`, `.gitignore`, `AGENTS.md`,
  `CONTRIBUTING.md`, `README.md`, `docs/PRD.md`, `docs/checkpoint.md`,
  `docs/diagram/arsitektur.svg`, `tools/build.tcl`,
  `tools/make_architecture.py`, `tools/make_diagram.py`, `tools/make_proposal.py`
- Riwayat lokal: `git rev-list --all --objects` → **tidak ada** objek bernama
  rubrik / docs-brief / docs-proposal / Ide-awal.
- Proposal: OCR halaman 1 mengonfirmasi 7 nama + NIM, termasuk Irwanto.

**Insiden & perbaikan**
- `git filter-branch` melakukan `reset --hard` di akhir sehingga file akademik
  **terhapus dari disk**. Sudah diantisipasi: sebelumnya di-backup ke
  `.tmp/backup-akademik/` → seluruh file berhasil dipulihkan dan terverifikasi
  (rubrik 3,3 KB; ide-awal 27,3 KB; proyek-1.pdf 201,9 KB; DOCX 148,7 KB;
  PDF 214 KB; diagram 111,3 KB).
- `git status` bersih → dokumen lokal benar-benar tidak ter-track.

**Batasan yang diketahui**
- Commit lama masih dapat diakses lewat **API GitHub jika SHA-nya diketahui**
  (mis. `c7d6e08`). Tidak terhubung ke branch/tag mana pun dan tidak bisa
  ditemukan lewat browsing, tetapi belum dipurge dari sisi GitHub. Pemilik
  memilih menerima risiko ini alih-alih menghapus repo.
- `tools/make_proposal.py` **tetap publik** dan memuat teks proposal serta daftar
  nama + NIM. Pemilik sudah menyetujui nama & NIM tampil publik.

**Berikutnya**
- Menunggu keputusan: apakah `tools/make_proposal.py` tetap publik atau
  dikeluarkan juga.
- Menunggu: judul disepakati kelompok, deadline BRONE, model konverter
  VGA→HDMI → lalu fase 1.

---

## 2026-10-19 (lanjutan 3) — README profesional, diagram SVG, checkpoint tag

**Dikerjakan**
- README ditulis ulang secara profesional: fokus rekayasa (arsitektur, video
  pipeline, status berbasis bukti), tanpa framing akademik.
- `tools/build.tcl` dibuat (sebelumnya disebut README tapi belum ada).
- Diagram ASCII di README diganti **SVG vektor** (`docs/diagram/arsitektur.svg`)
  karena box-drawing ASCII pecah di GitHub.
- `AGENTS.md` §5.0: aturan wajib menawarkan commit + tag + push setiap
  pekerjaan besar.

**Bukti**
- `build.tcl` dijalankan nyata: root ber-spasi ter-resolve benar, gagal dengan
  pesan jelas saat `src/` kosong (sesuai rancangan).
- SVG: XML valid (74 elemen), dirender Chrome headless 2× → 2400×2080 px,
  OCR membaca **29 label** dengan confidence 0.92–1.00.
- Tag `stable-2026-10-19-v1` dibuat (annotated) dan **ada di remote**
  (`git ls-remote --tags origin` mengonfirmasi).
- `git status` bersih; `main` sinkron dengan `origin/main`.

**Koreksi**
- Draft README pertama menulis "running on a Digilent Basys 3 board"
  (present tense) padahal belum ada RTL → dikoreksi jadi "targeting".
- README menyebut `tools/build.tcl` yang belum ada → file dibuat, bukan
  klaimnya yang dihapus.

**Belum terverifikasi**
- Tampilan README & SVG di GitHub (butuh jaringan + render browser; hanya
  diverifikasi lokal via Chrome).
- Badge di README belum dicek render-nya.

**Berikutnya**
- Menunggu: judul disepakati kelompok, konfirmasi deadline BRONE, model
  konverter VGA→HDMI, lalu mulai fase 1 (analisis modul repo acuan).

---

## 2026-10-19 (lanjutan 2) — Repo GitHub: private, contributor, batasan platform

**Dikerjakan**
- Repo dibuat dan dipublikasikan: **https://github.com/MuhammadFaza-DU/MarioKan**
- Visibilitas: **PRIVATE**.
- `CONTRIBUTING.md` diperluas: pembagian peran, alur branch/PR, aturan bukti,
  dan perintah mengundang collaborator.

**Bukti**
- `gh repo view MuhammadFaza-DU/MarioKan --json visibility` → `"PRIVATE"`
- `gh api repos/MuhammadFaza-DU/MarioKan --jq .private` → `true`
  (dua sumber independen, sepakat)
- `gh api .../collaborators --jq '.[].login'` → hanya `MuhammadFaza-DU`
- `gh api .../invitations` → kosong (belum ada undangan terkirim)
- `git ls-files` → 15 file; **tidak ada** bitstream, log Vivado, `.tmp/`,
  atau kredensial yang ter-commit.

**Gagal / tidak bisa (penting)**
- **Branch protection TIDAK dapat dipasang.** Dua jalur dicoba, dua-duanya
  ditolak **HTTP 403** dengan pesan "Upgrade to GitHub Pro or make this
  repository public to enable this feature":
  1. `PUT /branches/main/protection` (classic branch protection)
  2. `POST /rulesets` (repository rulesets)
- Artinya: aturan "jangan push langsung ke `main`" **hanya konvensi tertulis**,
  bukan paksaan teknis. Semua collaborator secara teknis tetap bisa push ke
  `main`. Ini dicatat juga di `CONTRIBUTING.md` agar tidak menyesatkan.
- Opsi untuk memaksakan: (a) upgrade akun ke **GitHub Pro**, atau (b) jadikan
  repo **publik** setelah tugas selesai.

**Keputusan**
- Undangan collaborator **dilakukan pemilik sendiri** (bukan oleh agent),
  memakai perintah `gh api --method PUT .../collaborators/<USERNAME> -f permission=push`
  yang sudah ditulis di `CONTRIBUTING.md`.
- Hak yang diberikan: **`push`** (bukan `admin`) → tidak bisa menghapus repo
  atau mengubah setting.

**Belum diverifikasi**
- Username GitHub kelima anggota belum diketahui → **belum ada yang diundang**.
- Belum ada Pull Request / branch dari kontributor (belum ada kontributor).

**Berikutnya**
- Pemilik mengundang 5 anggota dengan akses `push`, lalu mereka menerima
  undangan lewat email / halaman invitations.

---

## 2026-10-19 (lanjutan) — Proposal Proyek 1 (DOCX + PDF)

**Dikerjakan**
- Menyerap `docs/brief/proyek-1.pdf` → transkripsi terstruktur di `docs/rubrik.md`.
- Merapikan struktur dokumen: dokumen mentah dipindah ke `docs/brief/`.
- Menulis **proposal Proyek 1** sesuai 4 poin wajib dosen (judul, tujuan & fungsi,
  gambaran cara kerja, rencana implementasi).
- Membuat diagram blok sistem (PNG) via `tools/make_diagram.py`.
- Generator dokumen: `tools/make_proposal.py` (python-docx).
- Output: `docs/proposal/Proposal-Proyek-1-MarioKan.docx` + `.pdf`.
  > **Catatan (2026-10-22):** kedua file ini **sudah dihapus** dari disk atas
  > instruksi pemilik. Bisa diregenerasi dari `tools/make_proposal.py` bila perlu.

**Bukti**
- DOCX tersimpan, dikonversi ke PDF via Word COM: **10 halaman**, 2.455 kata.
- Teks terverifikasi lewat OCR PDF: cover tanpa nomor halaman, tidak ada baris
  tabel terpotong antar halaman, seluruh tabel & daftar pustaka tercetak utuh.
- Diagram terverifikasi lewat OCR PNG: 16 baris teks, confidence 0,98.

**Temuan penting**
- `websearch` mengembalikan **0 hasil**; Bing/Google/DuckDuckGo via fetch
  mengembalikan konten tidak relevan (GameHouse, Zhihu). Riset format proposal
  karena itu **tidak memakai sumber web** — disusun dari struktur akademik umum
  + penalaran atas rubrik. Ini keterbatasan yang harus diketahui.
- Referensi yang **terverifikasi aksesnya**: Digilent `Basys-3-Master.xdc`
  (isi file dibaca, pin cocok) dan README repo `FPGA-Mario` (penulis, toolchain).
  Referensi lain (UG472, UG473, UG901, IEEE 1076, CEA-861, Chapweske) adalah
  dokumen kanonik; URL AMD hanya memuat aplikasi JS saat diakses.

**Keputusan**
- Struktur proposal: **ikut persis 4 poin dosen** (bukan BAB I–III), atas
  permintaan pemilik.
- Judul dipakai: "MarioKan: Implementasi Game Platformer Bergaya Super Mario
  Bros. pada FPGA Basys 3 Menggunakan VHDL" — masih menunggu diskusi kelompok.
- Audio & mouse ditulis sebagai fitur dengan **catatan status jujur**
  (pengembangan lanjutan / opsional menunggu verifikasi).
- Bukti `SYN` (MMCM 148,4375 MHz, WNS +4,041 ns, bitstream) dimasukkan ke
  subbab 4.6 sebagai bukti kelayakan — mengangkat komponen rubrik terbesar (30%).

**Belum diverifikasi**
- Judul belum disepakati kelompok; daftar judul kelompok lain tidak bisa diakses.
- Tanggal pengumpulan proposal dari dosen: pemilik menyebut 23 Oktober 2026 23:59
  (perlu konfirmasi ulang di BRONE).
- Format resmi proposal tidak diberikan dosen; struktur mengikuti 4 poin wajib.

**Berikutnya**
- Review proposal oleh pemilik + kelompok → revisi bila perlu → unggah via BRONE.
- Setelah judul disetujui: mulai fase 1 (analisis modul repo acuan).

---

## 2026-10-19 — Fondasi: verifikasi toolchain & keputusan awal

**Dikerjakan**
- Membaca brief awal (`Ide-awal.md`) dan memeriksa repo sumber
  `nicklesimba/FPGA-Mario` (915 file, dapat diakses).
- Verifikasi toolchain Vivado di mesin ini.
- Menetapkan aturan kerja proyek (`AGENTS.md`) termasuk batas wilayah kerja.
- Menyiapkan kerangka repo (README, CONTRIBUTING, .gitignore, .gitattributes).

**Bukti**
- `SYN` — Vivado **v2026.1** di `D:\AMDDesignTools\2026.1\Vivado`.
  Device `xc7a35tcpg236-1` tersedia (30 varian `xc7a35t*`).
- `SYN` — Uji penuh desain *probe* (counter + `MMCME2_BASE`):
  `synth_design → opt → place → route → write_bitstream` **sukses**,
  0 error / 0 critical warning, **bitstream 2,19 MB** terbentuk.
- `SYN` — MMCM `CLKFBOUT_MULT_F=11.875`, `DIVCLK_DIVIDE=1`,
  `CLKOUT0_DIVIDE_F=8` menghasilkan `clk_pix` **148,438 MHz**
  (period 6,737 ns), **WNS +4,041 ns**, 0 DRC error.
  → Premis 1080p di speed grade `-1` **layak**, bukan spekulasi.
- Repo sumber: PNG sprite asli **tersedia** di
  `ECE385-HelperTools-master/.../sprite_originals/` (24 file) → tidak perlu
  rekonstruksi sprite dari ROM.
- Python 3.12 + Pillow 12.2.0 tersedia → tooling konversi sprite bisa jalan.

**Temuan penting**
- Path repo mengandung spasi (`Project dan SourceCode`) → Vivado memecah
  argumen. Workaround `[list $path]` sudah diverifikasi berfungsi.
  Rename folder induk **ditunda**: ada agent lain yang aktif di folder itu
  (proses `astro preview` PID 2324 di `WEBB\gamein`).
- Rename folder project sendiri juga gagal karena dikunci session yang sedang
  berjalan → dilakukan bersamaan saat rename induk nanti.
  > **Update 2026-10-22:** rename induk **SUDAH SELESAI**.
  > `D:\Progamming\Project dan SourceCode` -> `D:\Progamming\Project-SourceCode`.
  > Path repo sekarang **tidak mengandung spasi**, jadi masalah pemecahan argumen
  > Vivado di atas sudah tidak berlaku. Workaround `[list $path]` tetap dipakai.

**Keputusan**
- Audio **ditunda** ke pengembangan lanjutan (deviasi resmi dari brief —
  hardware audio belum tersedia). Wajib tercatat di PRD.
- Contributor: **dokumentasi & testing saja**, tidak menyentuh RTL.
- Knowledge graph tidak dipakai; progres dilacak di file ini.
- Konverter VGA→HDMI **sudah dimiliki** (TV hanya punya HDMI).

**Belum diverifikasi**
- Semua RTL game — belum ada.
- Uji papan fisik — belum ada.
- Perilaku konverter VGA→HDMI terhadap clock 148,4375 MHz — belum diuji.

**Berikutnya**
- Menunggu dari pemilik proyek: spesifikasi alat, rubrik penilaian,
  ketentuan tugas akhir → lalu menulis `docs/PRD.md`.
