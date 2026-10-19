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
