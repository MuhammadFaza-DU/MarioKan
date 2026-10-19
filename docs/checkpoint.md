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
