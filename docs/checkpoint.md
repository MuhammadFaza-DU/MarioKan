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
