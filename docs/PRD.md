# PRD — MarioKan

**Versi:** 0.2 (rancangan; rincian teknis terbuka tetap usulan)
**Dibuat:** 2026-10-19
**Diperbarui:** 2026-11-12
**Pemilik:** Muhammad Faza
**Status:** D0 disetujui; DOCX P2 tersedia untuk review pemilik. Diagnostik input terpisah lulus SIM/SYN, belum diprogram dan belum BOARD. Lihat CHECKPOINTS.md untuk progres terkini dan §7 untuk pertanyaan yang masih terbuka.

> Dokumen ini **menggantikan** `Ide-awal.md` sebagai sumber requirement.
> `Ide-awal.md` tetap disimpan sebagai referensi teknis (fakta board, PS/2,
> MMCM, pinout), tetapi **tidak lagi mengikat**. Setiap perbedaan dicatat di §6.

---

## 1. Executive Summary

### Problem Statement

Tugas akhir membutuhkan sistem digital yang dibangun dari nol di FPGA dan
didemokan langsung di papan: bukan aplikasi software, bukan mikrokontroler.
Tantangannya adalah merancang sistem yang cukup kompleks untuk dinilai serius
(game interaktif penuh: fisika, musuh, state machine, video resolusi tinggi)
tetapi tetap muat dan *timing-closed* di FPGA kecil berspeed grade terendah
(`XC7A35T-1`), tanpa framebuffer eksternal, tanpa CPU lunak, dan tanpa codec
audio.

### Proposed Solution

Game platformer 2D bergaya *Super Mario Bros.* yang berjalan **100% di fabric
FPGA** dalam VHDL: renderer *racing-the-beam* (tanpa framebuffer) pada
**1920×1080 @ 60 Hz**, logika game berjalan pada clock pixel yang sama dengan
*clock-enable* 60 Hz, kendali penuh lewat keyboard USB/PIC24/PS/2 atau lima
tombol papan (mouse opsional), fisika *fixed-point*,
dan FSM game lengkap (menu → main → mati/menang → game over).

Pendekatan kunci: **resolusi logika 384×216 di-upscale integer ×5** ke 1080p.
Satu nilai piksel logika ditampilkan pada area 5×5 piksel layar. Pemakaian
ulang hasil dapat mengurangi pekerjaan, tetapi tidak otomatis menyediakan
25 clock berturut-turut untuk setiap fetch; jadwal port/ROM dan pipeline tetap
harus dihitung serta diuji.

### Success Criteria (terukur)

| # | Kriteria | Cara ukur |
|---|---|---|
| SC-1 | Bitstream dihasilkan untuk `xc7a35tcpg236-1` | `write_bitstream` sukses, file `.bit` ada |
| SC-2 | **WNS ≥ 0** dan **WHS ≥ 0** pada clock pixel | `report_timing_summary` |
| SC-3 | **0 latch** terinferensi, 0 critical warning | laporan sintesis |
| SC-4 | Semua port top punya `PACKAGE_PIN` + `IOSTANDARD` | 0 warning `NSTD-1` / `UCIO-1` |
| SC-5 | Utilisasi di bawah kapasitas board | `report_utilization` (LUT ≤ 20.800, FF ≤ 41.600, BRAM ≤ 50, DSP ≤ 90) |
| SC-6 | Gambar tampil stabil 1080p nominal 60 Hz pada monitor melalui VGA langsung | uji papan pada monitor yang mendukung mode tersebut, tidak ada tearing/blank |
| SC-7 | Game dapat dimainkan penuh melalui keyboard maupun lima tombol papan: menu → level → menang | uji papan untuk setiap jalur secara terpisah, skenario uji tertulis |
| SC-8 | Semua aturan menang/kalah terpicu sesuai §4.6 | testbench + uji papan |

### 1.1 Konteks akademik & deliverable

Proyek ini adalah tugas akhir mata kuliah **Sistem Digital Lanjut**, dikerjakan
bertahap. Tahap yang sedang berjalan: **Proyek 2: Perancangan Arsitektur**
(sumber aktif: `docs/brief/proyek-2.pdf`; instruksi P1 dan rubrik lamanya tetap
referensi di `docs/brief/proyek-1.pdf` / `docs/rubrik.md`). Semuanya dokumen
**lokal**, tidak di-commit ke repo publik.

| Deliverable | Isi | Status |
|---|---|---|
| **D0 — Proposal judul** | Judul, tujuan & fungsi, cara kerja (input/proses/output), rencana implementasi VHDL di Basys 3. PDF diunggah via BRONE | **final dan disetujui** berdasarkan konfirmasi pemilik 2026-11-12; tanggal persetujuan sebenarnya/status unggah tidak diverifikasi. PDF P1 tetap byte-identik. |
| **P2: Perancangan arsitektur** | Diagram, fungsi/antarmuka, alur, rencana VHDL dan pengujian; rincian pada lampiran | DOCX lokal di `docs/proposal/proyek-2/`, untuk review pemilik; bukan persetujuan otomatis seluruh usulan teknis atau bukti game bekerja. |
| D1 — RTL + bitstream | Semua modul §4.4, `build.tcl`, XDC, bitstream | belum ada |
| D2 — Laporan kuliah | Dokumen akademik terpisah dari PRD | belum ada |
| D3 — Slide / video demo | Materi presentasi + rekaman board | belum ada |
| D4 — Dokumentasi teknis | `PORTING_NOTES.md`, diagram arsitektur, `CHECKPOINTS.md` | sebagian |

Bobot rubrik D0: kesesuaian judul **20%**, tujuan & fungsi **25%**, cara kerja &
I/O **25%**, **kelayakan implementasi 30%**. Komponen terbesar justru punya
bukti empiris (`SYN`, §4.2) → proposal dapat menampilkan angka, bukan janji.

**Jadwal:** batas maksimum **2 bulan** sejak 2026-10-19; target internal lebih
cepat, kualitas diutamakan. Eksekusi direncanakan memakai **beberapa agent
paralel dengan satu agent pengontrol**, sehingga task harus dipecah menjadi unit
dengan batas file yang jelas dan tidak saling menimpa.

---

## 2. User Experience & Functionality

### 2.1 Persona

| Persona | Kebutuhan |
|---|---|
| **Penguji/dosen** | Melihat sistem berjalan di papan dalam < 1 menit: colok VGA, nyalakan, main. Menilai kelengkapan fitur + kualitas teknis (timing, arsitektur). |
| **Pemain (teman/keluarga)** | Bisa langsung paham kontrol tanpa manual; ada menu, high score, aturan jelas. |
| **Kontributor repo** | Bisa memahami arsitektur, menambah dokumentasi/testbench, tanpa merusak RTL. |

### 2.2 User Stories

Pemetaan tombol papan, reset saklar, dan pemetaan keyboard disetujui dalam
pembahasan terpisah pada 2026-11-12 (D-13, D-14, D-15). Persetujuan tersebut
tidak berarti seluruh rancangan P2 telah disetujui atau input sudah diuji.

**US-1 — Boot & menu**
Sebagai penguji, saya ingin papan langsung menampilkan menu setelah dinyalakan,
supaya saya tahu sistem hidup tanpa perlu menekan apa pun.
- AC: dalam ≤ 1 detik setelah `locked` MMCM, layar menampilkan logo + opsi menu.
- AC: opsi **START**, **HOW TO PLAY**, dan tampilan **HIGH SCORE** terlihat.
- AC: opsi aktif tersorot jelas (warna/ikon berbeda).

**US-2 — Navigasi keyboard**
Sebagai pemain, saya ingin memilih menu dengan keyboard, supaya bisa main tanpa mouse.
- AC: `↑`/`↓` memindahkan sorotan, `Enter` memilih, dengan bunyi konfirmasi (bila audio aktif).
- AC: navigasi tidak bisa "nyangkut" — satu tekan = satu langkah (debounce + edge detect).

**US-3 — Navigasi mouse** *(fitur `4b` — hanya berlaku bila jalur mouse terbukti ada)*
Sebagai pemain, saya ingin mengklik menu dengan mouse.
- AC: kursor bergerak sesuai gerakan mouse, di-*clamp* ke area layar.
- AC: hover mengubah sorotan, klik kiri memilih.
- AC: bila mouse tidak terdeteksi, kursor disembunyikan; kendali penuh tetap harus tersedia melalui keyboard atau lima tombol papan.
- AC: bila jalur mouse **tidak terbukti ada** (§4.3), fitur ini batal dan **tidak dihitung** sebagai kekurangan.

**US-4 — Bermain**
Sebagai pemain, saya ingin berjalan, berlari, dan melompat dengan responsif.
- AC: jalan dengan `←`/`→` atau `A`/`D`; lari dengan `Shift`/`Z`.
- AC: lompat dengan `Space`/`↑`/`W`; **tinggi lompat bergantung lama tombol ditahan**.
- AC: gerakan tidak menembus tile padat (tabrakan X dan Y diselesaikan terpisah).

**US-5 — Musuh**
Sebagai pemain, saya ingin Goomba berjalan dan bisa diinjak.
- AC: Goomba berjalan, berbalik di dinding dan di tepi platform.
- AC: diinjak dari atas → animasi *squished* → hilang + skor; suara hanya jika audio kelak diaktifkan.
- AC: disentuh dari samping/bawah saat *small* → mati; saat *big/fire* → menyusut + invincible ±2 detik (berkedip).

**US-6 — Power-up & item**
Sebagai pemain, saya ingin memukul blok `?` dan mengambil jamur/bunga.
- AC: blok `?` dipukul dari bawah → mengeluarkan koin **atau** jamur (animasi naik) → berubah jadi blok kosong.
- AC: jamur bergerak, disentuh → Mario *big* (sprite 16×32) + skor; suara hanya jika audio kelak diaktifkan.
- AC: saat Mario *big*, blok `?` berikutnya mengeluarkan **bunga api** → Mario *fire*.
- AC: saat *fire*, tombol lari/aksi menembakkan **fireball** (memantul di tanah, membunuh Goomba, jumlah aktif dibatasi).

**US-7 — Koin & skor**
Sebagai pemain, saya ingin melihat skor dan koin bertambah.
- AC: koin +1 dan skor bertambah; HUD menampilkan `SCORE`, `COINS`, `WORLD 1-1`, `TIME`, `LIVES`.
- AC: 100 koin = +1 nyawa.

**US-8 — Kamera**
Sebagai pemain, saya ingin level terasa lebih luas dari layar.
- AC: kamera mengikuti Mario secara horizontal, **tidak pernah mundur**.
- AC: level lebih lebar dari layar (≥ 100 metatile).

**US-9 — Mati & game over**
Sebagai penguji, saya ingin aturan kalah jelas dan konsisten.
- AC: mati karena (a) menyentuh Goomba dari samping/bawah saat *small*, (b) jatuh ke jurang, (c) waktu habis.
- AC: urutan mati: animasi `mario_dead` → nyawa −1 → respawn **atau** GAME OVER bila nyawa 0. Musik berhenti hanya relevan jika audio kelak diaktifkan.
- AC: nyawa awal **3**, tampil di HUD dan LED.

**US-10 — Menang**
Sebagai penguji, saya ingin kondisi menang yang jelas.
- AC: menyentuh tiang bendera → animasi meluncur turun → bonus skor berdasar ketinggian → bonus sisa waktu → layar `COURSE CLEAR` + skor.
- AC: high score diperbarui bila skor lebih tinggi.

**US-11 — Pause**
Sebagai pemain, saya ingin menjeda permainan.
- AC: `P`/`Esc` menghentikan seluruh logika game (animasi & timer berhenti), layar menampilkan indikator pause.
- AC: menekan lagi melanjutkan dari kondisi persis sebelum pause.

**US-12 — Kontributor**
Sebagai kontributor, saya ingin tahu apa yang boleh saya ubah.
- AC: `CONTRIBUTING.md` menjelaskan peran, alur branch/PR, dan aturan bukti.
- AC: perubahan RTL melalui review pemilik; pembatasan kontributor adalah aturan kerja. CODEOWNERS/ruleset belum diverifikasi aktif dan tidak dianggap sebagai pengamanan teknis yang sudah terpasang.

**US-13: Kendali penuh lewat lima tombol papan (disetujui 2026-11-12)**
Sebagai pemain, saya ingin memakai tombol bawaan papan tanpa memasang keyboard.
- AC: tombol atas/bawah memindahkan pilihan menu satu langkah per penekanan;
  tombol tengah mengonfirmasi atau memulai permainan.
- AC: saat bermain, kiri/kanan untuk bergerak, atas untuk lompat, bawah untuk
  lari/aksi, dan tengah untuk pause/lanjut.
- AC: satu penekanan atas memulai satu lompatan; lama tahan mengatur tinggi.
  Menahan atas terus tidak menyebabkan lompatan baru otomatis setelah mendarat.
- AC: menahan bawah bersama arah membuat Mario berlari. Jika menjadi Fire
  Mario, satu penekanan bawah meminta satu tembakan, tunduk pada batas bola
  api aktif; menahan bawah tidak menembak berulang otomatis.
- AC: kombinasi arah + bawah + atas didukung untuk berlari sambil melompat.
- AC: satu penekanan tengah hanya menghasilkan satu aksi; tombol yang masih
  ditahan setelah START tidak langsung memicu pause. Harus dilepas dan ditekan lagi.
- AC: reset memakai keputusan terpisah D-14; pemetaan keyboard mengikuti D-15.

### 2.3 Non-Goals (v1)

- Multi-level sebagai target wajib dan world map. Target minimum tetap satu
  level lengkap; empat peta tambahan hanya pengembangan opsional setelah level
  wajib lulus pengujian, memakai mekanik dan aset bersama (D-12).
- Save state persisten (high score hilang saat power-off — batasan hardware, dicatat).
- Multiplayer.
- Level editor runtime.
- Enemy selain Goomba (Koopa, Piranha, dsb).
- Audio (ditunda — lihat §6 deviasi D-1).
- Musik orisinal hasil gubahan penuh (bila audio diaktifkan nanti: melodi pendek orisinal, bukan transkripsi tema Nintendo).
- Dukungan mouse+keyboard bersamaan **dijamin** (bergantung USB hub — lihat risiko R-3).

### 2.4 Anti-Goals (kegagalan walau "secara teknis jalan")

- Game berjalan tetapi hanya di simulasi, tidak pernah terlihat di papan.
- Bitstream dihasilkan tetapi WNS negatif (tidak stabil di suhu/tegangan nyata).
- Fitur "ada di kode" tetapi tidak bisa dipicu pemain.
- Menyembunyikan fitur yang belum selesai, bukan menandainya.
- Menyalin arsitektur NIOS II/Qsys/codec DE2 ke proyek ini.

---

## 3. AI System Requirements

**Tidak berlaku.** Proyek ini tidak memakai model AI di dalam sistem. Agent AI
hanya dipakai sebagai alat bantu pengembangan (di luar produk).

---

## 4. Technical Specifications

### 4.1 Target hardware (fakta, terverifikasi)

| Item | Nilai | Status |
|---|---|---|
| FPGA | Artix-7 `XC7A35T-1CPG236C` | `SYN` — part tersedia di Vivado |
| Kapasitas | ±20.800 LUT, 41.600 FF, 50 BRAM36, 90 DSP, 5 MMCM | datasheet |
| Clock board | 100 MHz, pin `W5` | `SYN` |
| VGA | DAC resistor **4 bit/kanal** (12-bit, 4096 warna) | brief + XDC |
| USB-HID | 1 port, via PIC24 → tampak sebagai **PS/2** (`PS2Clk` C17, `PS2Data` B17) | brief |
| Audio | **tidak ada codec**, tidak ada HDMI | fakta board |
| Memori eksternal | **tidak ada** SDRAM/DDR yang boleh diandalkan | fakta board |
| Papan fisik | **tersedia di tangan pemilik** | dikonfirmasi |
| Display | Jalur utama **VGA langsung ke monitor**. Monitor uji harus dipinjam; unit monitor demo belum ditentukan | laporan pemilik 2026-11-12; model dan dukungan 1080p melalui VGA belum terverifikasi |
| Toolchain | Vivado **2026.1** di `D:\AMDDesignTools\2026.1\Vivado` | `SYN` |

### 4.2 Video pipeline

**Timing CEA-861, 1920×1080 @ 60 Hz, polaritas sync positif:**

| | Active | Front porch | Sync | Back porch | Total |
|---|---|---|---|---|---|
| Horizontal (px) | 1920 | 88 | 44 | 148 | **2200** |
| Vertikal (baris) | 1080 | 4 | 5 | 36 | **1125** |

**Clock pixel: 148,4375 MHz** — `MMCME2_BASE`:
`CLKFBOUT_MULT_F=11.875`, `DIVCLK_DIVIDE=1`, `CLKOUT0_DIVIDE_F=8`
→ VCO 1187,5 MHz (dalam batas 600–1200 untuk `-1`) → 148,4375 MHz
(deviasi sekitar **−0,042%** dari 148,5 MHz). Deviasi terhitung tidak menjamin
monitor tertentu menerima mode ini; kompatibilitas masukan VGA harus diuji.
Status: **`SYN` arsip probe MMCM + counter**, bukan renderer/game. Laporan final
`.tmp/probe/rpt_timing.txt`: period 6,737 ns, WNS +4,043 ns, WHS +0,254 ns;
laporan DRC menunjukkan 0 temuan. Angka +4,041/+0,238 ns yang disebut pada
materi awal berasal dari estimated timing router, bukan laporan final.

**Resolusi logika: 384×216**, di-upscale integer **×5** → 1920×1080 tepat.

- Grid tile 8×8 → **48×27 tile**.
- Strip HUD 24 px (3 baris tile) di atas + area bermain 192 px (24 baris tile) = 216 px.
- Upscale memakai **dua counter sub-piksel 0..4** (x dan y), **bukan pembagi**.
- **Tanpa framebuffer.** Arsitektur *racing the beam*: tilemap di BRAM, sprite
  ROM di BRAM, prioritas layer dihitung per piksel logika.
- `hsync`, `vsync`, `de`, dan RGB **diregister bersamaan** agar sejajar.
- Pipeline jalur piksel minimal 4 tahap (koordinat → alamat ROM → data → palette → output).
- Modul timing dapat diparameterkan lewat generic untuk pengujian, tetapi
  **mode operasional v1 tetap hanya 1080p dan grid logika 384×216 dikunci**.
  Pemilik menegaskan pilihan 1080p saja pada 2026-11-12; usulan beberapa mode
  tampilan tidak diambil. Perubahan resolusi atau penambahan mode merupakan
  perubahan requirement yang perlu persetujuan baru, bukan fitur fallback yang
  boleh diaktifkan diam-diam. Mitigasi utama kegagalan timing adalah pipeline.

**Warna:** sprite disimpan sebagai **indeks palet 4-bit** (0 = transparan),
dengan **4 bank palet × 16 entri × 12 bit** (64 entri total, ROM 64×12).
Setiap sprite/tile membawa **2 bit bank-select** di metadata-nya. Output ke VGA 4-4-4.

> Alasan banking: satu palet global hanya memberi 15 warna terpakai untuk
> Mario (small/big/fire), Goomba, jamur, bunga api, fireball, koin, blok,
> bata, tanah, pipa, awan, tiang, kursor, font, dan logo — terlalu sempit dan
> kegagalannya baru terlihat sebagai *quantisation mush* di fase aset.
> Biaya banking: 1 ROM 64×12 bit + 2 bit metadata per entri sprite.
> **Keputusan builder (2026-10-19).**

### 4.3 Input

**Dua jalur kendali penuh (keputusan pemilik 2026-11-12)**

Keyboard USB eksternal melalui PIC24/PS/2 dan lima tombol papan sama-sama
wajib diimplementasikan. Pemain boleh memakai salah satunya, termasuk untuk
menu dan pause; mode tombol papan tidak bergantung pada keyboard terpasang.
Ini requirement, bukan hasil pengujian SIM/SYN/BOARD.

**Keyboard (wajib, pemetaan disetujui 2026-11-12, D-15)**
- `ps2_rx`: sinkronisasi 2-FF, deteksi falling edge, frame 11 bit
  (start, 8 data LSB-first, parity ganjil, stop), cek parity, timeout.
- `kbd_decoder`: scancode **set 2**, tangani prefix `E0` (extended) dan `F0`
  (break). Keluaran = **status tombol ditahan** (bukan event sesaat).
- Pemetaan berikut disetujui setelah tabel dan contoh penggunaan dijelaskan:

| Fungsi | Tombol |
|---|---|
| Kiri / Kanan | `←` `→` atau `A` `D` |
| Lompat | `Space` / `↑` / `W` |
| Lari / tembak | `Left Shift` / `Z` |
| Menu naik/turun | `↑` `↓` |
| Pilih | `Enter` |
| Pause | `P` / `Esc` |

Alternatif tombol berarti cukup memakai salah satunya. Contoh berlari sambil
melompat ke kanan: tahan `D` + `Left Shift`, lalu tekan `Space`. Aturan
tekan/tahan sama dengan jalur papan: lama tahan lompat memengaruhi tinggi,
satu penekanan lompat tidak berulang otomatis, dan satu penekanan aksi
meminta satu bola api hanya saat Fire Mario serta batas bola aktif mengizinkan.
Menahan aksi bersama arah tetap berfungsi untuk lari, bukan tembakan otomatis.
Menu/pause satu aksi per penekanan. Make code berulang dari keyboard yang
masih ditahan tidak boleh dianggap sebagai penekanan fisik baru.
Reset tetap memakai `sw[0]` pada kedua jalur, bukan tombol keyboard tambahan.

**Lima tombol papan (pemetaan dan tekan/tahan disetujui 2026-11-12)**

| Keadaan | Tombol papan | Fungsi |
|---|---|---|
| Menu | Atas `btnU` / bawah `btnD` | Pindah pilihan satu langkah per penekanan |
| Menu | Tengah `btnC` | Konfirmasi atau mulai |
| Bermain | Kiri `btnL` / kanan `btnR` | Bergerak selama ditahan |
| Bermain | Atas `btnU` | Satu lompatan per penekanan; tinggi dipengaruhi lama tahan |
| Bermain | Bawah `btnD` | Tahan bersama arah untuk lari; sekali tekan untuk satu tembakan jika Fire Mario dan batas bola aktif memungkinkan |
| Bermain / pause | Tengah `btnC` | Pause / lanjut, satu aksi per penekanan |

Contoh dan perilaku rinci ada di `docs/INPUT_GUIDE.md`. Kebutuhan kendali
saklar `sw[15:12]` + `btnU` pada D-8 digantikan jalur penuh lima tombol pada
D-13; D-8 tetap disimpan sebagai riwayat, bukan kewajiban aktif.

**Reset sesi permainan (disetujui pemilik 2026-11-12, D-14)**

- `sw[0] = 1`: sesi dibatalkan dan game ditahan dalam keadaan reset.
- `sw[0] = 0` setelah reset: masuk menu, tidak otomatis bermain.
- START berikutnya memulai permainan baru: tiga nyawa, skor/koin nol, waktu
  awal, dan blok/peta kembali ke keadaan awal. Posisi dan entitas diinisialisasi
  untuk permainan baru.
- High score yang tersimpan tidak dihapus oleh reset saklar; tetap bersifat
  volatil, tanpa janji bertahan setelah daya mati atau FPGA diprogram ulang.
- Saklar yang sama berlaku saat pemain memakai keyboard ataupun tombol papan.
  Tekan biasa tombol tengah tetap konfirmasi/pause, bukan reset; tidak ada
  fungsi reset tekan lama yang disetujui.
- Ini reset logika sesi, bukan penghapusan konfigurasi FPGA atau penulisan
  flash. Semantik respawn setelah mati tetap berbeda, lihat §4.6.

Rancangan RTL harus membedakan inisialisasi awal perangkat dari reset sesi
agar high score tidak ikut dihapus oleh `sw[0]`. Pemulihan peta pada permainan
baru perlu prosedur inisialisasi tersendiri; rincian memori dan latensinya
ditetapkan pada tahap arsitektur, bukan dianggap sudah diimplementasikan.

**Mouse (opsional, graceful degradation — status: belum tervalidasi)**
- `ps2_tx`: kirim `0xFF` (reset) → tunggu `0xFA 0xAA 0x00` → `0xF4` (enable reporting).
- Parser paket 3 byte (tombol, ΔX, ΔY; bit tanda & overflow), akumulasi posisi, clamp.
- Kursor 8×8/16×16, hover + klik kiri pada tombol menu.
- Bila tidak ada paket mouse valid dalam N detik, kursor disembunyikan;
  kendali penuh tetap tersedia melalui keyboard atau lima tombol papan.

**Batasan protokol yang harus diakui (temuan builder check, 2026-10-19):**
Basys3 hanya punya **satu** pasangan PS/2 (`PS2Clk` C17 / `PS2Data` B17). PS/2
**tidak addressable** — tidak ada ID perangkat di dalam frame. Paket mouse
3-byte punya framing 11-bit dan parity ganjil yang **identik** dengan tiga
scancode keyboard, sehingga `ps2_rx` tidak bisa membedakan perangkat hanya
dari framing. Selain itu `ps2_tx` harus memakai jalur open-drain yang sama
dengan keyboard yang sedang aktif bicara → arbitrase arah harus dirancang.

**Konsekuensi keputusan:**
- Keyboard dan lima tombol papan adalah dua jalur penuh yang wajib dirancang
  dan diuji untuk v1; keduanya belum terbukti berfungsi pada game.
- **Mouse berstatus fitur opsional `4b`**, dikerjakan **hanya jika** terbukti
  ada jalur perangkat mouse yang bisa dibedakan (mis. PIC24 mengekspos
  pasangan PS/2 kedua, atau bukti firmware meneruskan trafik mouse).
- Bila tidak terbukti: `ps2_tx`, `mouse_decoder`, dan kursor **dibatalkan dari
  scope**, menu tetap harus berfungsi via keyboard atau lima tombol papan. Ini **bukan** kegagalan
  fitur — ini keputusan berbasis bukti.
- **Bukti yang dibutuhkan:** dokumen/pengujian yang menunjukkan apakah PIC24
  Basys3 mengekspos dua pasangan PS/2 atau melakukan multiplexing. Sampai itu
  ada, mouse tidak dijanjikan.

### 4.4 Arsitektur modul

**Diagram umum yang disetujui pemilik 2026-11-12:**
[`docs/diagram/arsitektur.drawio`](diagram/arsitektur.drawio), sumber native
editable untuk diagram umum repo dan P2 (D-16). Pemilik mengirim screenshot
tampilan draw.io dan meminta memakai diagram ini.

Diagram mencakup 12 blok fungsi: Clock & Reset, Input Processing, Game
Controller, Player, Enemy, Items / Blocks, Collision Detection, Game Data,
Level Memory, Asset Memory, Video Generator, dan Status Display. Keyboard
USB melalui PIC24, lima tombol, clock papan, saklar reset, monitor VGA, LED
dan seven-segment menjadi masukan/keluaran eksternal yang terlihat.

Satu blok adalah fungsi sistem dan dapat memuat beberapa entity VHDL.
Panah dua kepala mewakili pertukaran melalui sinyal satu arah yang terpisah,
bukan penggunaan `inout` di modul internal. Distribusi clock/boot reset
bersama ditulis sebagai catatan agar diagram umum tetap mudah dibaca.
Mouse opsional dan audio tertunda tidak digambar sebagai fungsi baseline.

Persetujuan diagram bukan persetujuan seluruh rincian RTL atau bukti
SIM/SYN/BOARD. Draf tabel antarmuka/uraian dan ekspor resmi draw.io sudah
tersedia pada DOCX lokal P2; rincian baru tetap usulan sebelum dikunci.
SVG lama dan kandidat SVG detail tidak lagi menjadi acuan diagram aktif.

**Hierarki file yang diharapkan** (nama boleh disesuaikan, pemisahan dipertahankan):

```
src/
  top_basys3.vhd        -- hanya wiring + pin
  clk_gen.vhd           -- MMCME2_BASE (UNISIM)
  reset_sync.vhd
  vga_timing.vhd        -- generic untuk uji; mode operasional hanya 1080p
  scaler.vhd            -- koordinat layar -> koordinat logika (counter, tanpa divider)
  renderer.vhd          -- prioritas layer, palette lookup, output RGB444
  palette_pkg.vhd, tile_rom.vhd, level_rom.vhd, sprite_rom_*.vhd, font_rom.vhd
  ps2_rx.vhd, ps2_tx.vhd, kbd_decoder.vhd, mouse_decoder.vhd, input_mux.vhd
  board_input.vhd       -- rencana: sinkronisasi, debounce, status dan event tombol
  game_pkg.vhd          -- konstanta, tipe, fixed-point, enum state
  game_ctrl.vhd         -- FSM utama
  player.vhd            -- fisika & state Mario
  enemy_goomba.vhd, goomba_ctrl.vhd
  item_mushroom.vhd, item_fireflower.vhd, fireball.vhd, coin.vhd, qblock.vhd
  collision.vhd         -- tile & AABB
  hud_text.vhd
  seg7_mux.vhd
constraints/basys3.xdc
tools/sprites2vhdl.py, tools/build.tcl
sim/tb_*.vhd
docs/PRD.md, docs/PORTING_NOTES.md, CHECKPOINTS.md
```

**Audio** (`audio_synth.vhd`, `sfx_rom.vhd`, `bgm_rom.vhd`, `pwm_dac.vhd`)
didesain tetapi **tidak masuk v1** — lihat §6.

### 4.5 Aturan RTL (wajib)

- Bahasa: **VHDL** (VHDL-2008 diizinkan, diset per file). Constraint: **XDC**.
- Hanya `ieee.numeric_std`. **Dilarang** `std_logic_arith`, `std_logic_unsigned`, `std_logic_signed`.
- **Satu clock pixel** dari MMCM. Tidak ada derived clock dari counter — pakai **clock-enable**.
- Tick game 60 Hz diturunkan dari awal blanking vertikal (`frame_start`).
- Semua input asinkron lewat **sinkronisasi 2-FF**; tombol/PS/2 diberi debounce/glitch filter.
- Reset sistem dilepas **sinkron setelah `locked` stabil**; ditahan selama inisialisasi. Reset sesi dibedakan dari boot agar high score tidak ikut dihapus; kehilangan clock/lock diuji tersendiri.
- Tanpa latch, tanpa loop kombinasional. `Inferred latch` = **bug**, harus nol.
- Pembacaan BRAM **sinkron**; latensi pipeline dihitung dan sync disejajarkan.
- Tanpa `real`/floating point di logika sintesis → **fixed-point**, didefinisikan di `game_pkg.vhd`:
  - **Posisi dunia (`world_x`, `world_y`, `camera_x`) = Q13.8** (21-bit `signed`:
    1 sign + 12 integer + 8 fraksi) → jangkauan **±4.095,996**.
    Level terlebar 212 metatile × 16 px = **3392 px**, jadi Q13.8 memenuhi
    dengan sisa **703,996 px**. Q12.8 (20-bit `signed`) hanya menjangkau
    ±2.047,996 → **tidak cukup**; Q8.8 (±127,996) jauh lebih tidak cukup.
  - **Kecepatan (`vel_x`, `vel_y`) = Q8.8** (16-bit `signed`) — cukup untuk
    rentang kecepatan realistis dengan presisi sub-piksel.
  - Konversi ke koordinat layar: ambil bit integer dari Q13.8 (geser 8, tanpa divider).
- Pembagian/modulo konstanta non-pangkat-2 **dilarang** di jalur piksel.
- `inout` hanya di top untuk `PS2Clk`/`PS2Data` dengan buffer open-drain.

### 4.6 Aturan game (eksplisit, harus diimplementasikan persis)

**FSM utama:**
```
BOOT → MENU → (HOW_TO_PLAY) → PLAYING ⇄ PAUSED
                                  ├─(mati)──► DYING → (nyawa>0 ? PLAYING : GAME_OVER)
                                  └─(tiang bendera)──► LEVEL_CLEAR
GAME_OVER / LEVEL_CLEAR ──(konfirmasi papan/keyboard)──► MENU
```

**Kalah** — Mario kehilangan satu kesempatan bila salah satu terjadi:
1. Menyentuh Goomba dari **samping/bawah** saat **small**.
   Saat **big/fire**: menyusut ke small + invincibility ±2 detik (berkedip), **tidak mati**.
2. **Jatuh ke jurang** (Y melewati batas bawah layar).
3. **Waktu habis** (timer HUD mencapai 0).

Urutan mati: animasi `mario_dead` → nyawa −1 →
respawn di awal level (bila nyawa > 0) → GAME OVER bila 0. **Nyawa awal 3.**
Musik/SFX bukan syarat baseline; penghentian musik hanya berlaku bila audio
opsional kelak diaktifkan sesuai D-1.

**Semantik respawn (dikunci — menentukan arsitektur tilemap):**

| State | Saat mati → respawn |
|---|---|
| Tilemap (blok `?` yang sudah terpakai, bata pecah) | **TIDAK di-reset** saat respawn; tidak menjalankan pemulihan peta permainan baru. Satu tilemap mutable tetap digunakan. |
| `SCORE`, `COINS` | **Dipertahankan** |
| `TIME` | **Di-reset** ke nilai awal level |
| Posisi Mario, kamera | **Di-reset** ke awal level |
| Musuh & item aktif | **Di-reset** (semua kembali ke posisi awal) |
| Nyawa | −1 |

> Konsekuensi yang diterima: pemain yang menghabiskan semua blok power-up lalu
> mati bisa lanjut sebagai *small* tanpa akses bunga api. Ini **bukan** bug.
> Keputusan respawn 2026-10-19 tetap berlaku. Keputusan reset sesi D-14 pada
> 2026-11-12 mewajibkan peta awal untuk permainan baru, bukan saat respawn.
> Pernyataan lama tanpa ROM salinan/FSM reload tidak boleh ditafsirkan sebagai
> larangan menyediakan mekanisme pemulihan peta permainan baru. Sumber data
> awal dan cara pemulihannya masih harus dirancang serta dihitung memorinya.

**Menang:** menyentuh **tiang bendera** di akhir level → animasi meluncur turun →
bonus skor berdasar ketinggian sentuh + bonus sisa waktu → `LEVEL_CLEAR`
→ tampil `COURSE CLEAR` + skor → kembali ke menu, high score diperbarui.
Jingle hanya berlaku bila audio kelak diaktifkan; mouse/klik hanya jika fitur
opsional 4b terbukti, bukan pengganti konfirmasi papan/keyboard.

**Mekanik:**

| Elemen | Perilaku |
|---|---|
| Jalan/lari | Percepatan & gesekan fixed-point; kecepatan maks jalan < lari |
| Lompat | Impuls awal + tinggi variabel (tahan = lebih tinggi), gravitasi konstan, kecepatan jatuh dibatasi |
| Tabrakan tile | Sumbu X dan Y diselesaikan terpisah; tipe: kosong/padat/`?`/bata/pipa/tanah |
| Goomba | Jalan, berbalik di dinding/tepi; diinjak → squished → hilang (+skor) |
| Blok `?` | Dipukul dari bawah → koin atau jamur (animasi naik) → jadi blok kosong |
| Jamur | Bergerak; kena Mario → big (+skor) |
| Bunga api | Dari blok `?` saat big → fire; tombol lari menembak fireball (pantul, batas jumlah) |
| Koin | +skor; 100 koin = +1 nyawa |
| Kamera | Scroll horizontal mengikuti Mario, **tidak mundur** |
| HUD | `SCORE`, `COINS`, `WORLD 1-1`, `TIME`, `LIVES` via `font_rom` |

**Level wajib:** satu level lengkap, ≈100–212 metatile lebar, 12 metatile tinggi.
Wajib memuat: **≥ 2 jurang, ≥ 4 Goomba, ≥ 3 blok `?` (koin/jamur/bunga),
pipa, tangga akhir, tiang bendera.** Format level harus mudah diubah
(teks → ROM VHDL lewat skrip).

**Pengembangan opsional, disepakati pemilik 2026-11-12:** hingga empat level
tambahan setelah satu level wajib berhasil dibuktikan. Perbedaannya berupa
susunan peta dan tingkat kesulitan, dengan mekanik dan aset bersama. Empat
level tambahan bukan syarat pemenuhan target minimum dan tidak boleh
mengurangi kelengkapan atau pengujian level wajib. Rincian perpindahan level
dan status yang dibawa ke level berikutnya belum diputuskan; dirancang jika
pengembangan opsional diaktifkan, bukan dianggap sudah tersedia.

### 4.7 Aset

- Sumber sprite = **PNG asli** di repo acuan
  (`ECE385-HelperTools-master/.../sprite_originals/`). Audit langsung 2026-11-12
  membaca **30 PNG** pada commit `077d8a510f398e90e20650698b9795cc2d5f797e`.
  Ini inventaris sumber, **bukan aset target yang sudah siap**: dimensi dan
  palet belum seragam, dan belum semua kebutuhan gambar terpenuhi. Lihat
  `docs/ASSET_FEASIBILITY.md` untuk temuan dan anggaran memori awal.
- `tools/sprites2vhdl.py` (Pillow): PNG → kuantisasi palet 16 warna (12-bit) →
  ROM indeks piksel VHDL. Indeks 0 = transparan.
- Sprite minimal: Mario small (diam, jalan ×3, lompat), Mario big (diam, jalan ×3,
  lompat), Mario mati, Goomba (jalan ×2, squished), jamur, bunga api,
  fireball (2 frame), koin (4 frame), blok `?` (2 frame + kosong), bata, tanah,
  pipa, awan, semak/bukit, tiang bendera, kursor, font, logo.
- Mario menghadap kiri = **mirror pembacaan alamat**, bukan sprite terpisah.
- Atribusi repo asal (Nikhil Simha, Pranith Bottu) + catatan hak cipta Nintendo
  wajib ada di README.

### 4.8 Constraint & build

- `constraints/basys3.xdc` mengacu **Basys-3-Master.xdc resmi Digilent**
  (tabel pin di brief hanya titik awal, wajib dicocokkan).
- Input asinkron (PS/2, tombol, saklar): `set_false_path` hanya ke FF pertama sinkronisasi, bukan menutupi jalur FF kedua/logika inti yang wajib ditiming.
- Semua port top **wajib** punya `PACKAGE_PIN` + `IOSTANDARD`.
- `tools/build.tcl`: `read_vhdl` → `read_xdc` → `synth_design -top top_basys3
  -part xc7a35tcpg236-1` → `opt/place/route` → `report_timing_summary`,
  `report_utilization`, `report_clock_utilization`, `report_drc` → `write_bitstream`.
- **Karena path repo mengandung spasi:** setiap argumen path di Tcl **wajib**
  dibungkus `[list ...]` (sudah diverifikasi).

### 4.9 Verifikasi

Tabel berikut untuk **game produksi**, bukan diagnostik terpisah. Bukti yang
tersedia sekarang: SIM `tb_input_probe` untuk input mentah/receiver byte;
SYN `input_probe_top` pada 148,4375 MHz, WNS +2,068 ns / WHS +0,128 ns,
99 LUT/216 FF, 0 latch/DRC/critical warning. Berkas di `.tmp/diagnostics/`,
bitstream belum diprogram dan BOARD belum dites. Ini tidak membuktikan
decoder pemetaan, FSM game, VGA atau keseluruhan rancangan telah lulus.

| Testbench | Isi | Status |
|---|---|---|
| `tb_vga_timing` | total 2200×1125, lebar sync, posisi `de` | belum ada |
| `tb_ps2` | frame scancode set 2 (make/break/`E0`), parity salah ditolak; kombinasi arah+aksi+lompat; make berulang saat ditahan tidak menggandakan aksi menu/pause/tembak | belum ada |
| `tb_board_input` | debounce; tekan/tahan/lepas; kombinasi arah+aksi+lompat; tidak ada START lalu PAUSE dari penekanan tengah yang sama | belum ada |
| `tb_player` | tinggi lompat variabel, gravitasi, tabrakan lantai/dinding | belum ada |
| `tb_game_ctrl` | semua transisi FSM: mati (Goomba/jurang/waktu), menang | belum ada |
| `tb_session_reset` | sw[0] ditahan 1 lalu 0 kembali menu tanpa otomatis bermain; START baru mengembalikan tiga nyawa, skor/koin nol, waktu/blok awal; high score tidak terhapus; respawn tetap mempertahankan tilemap | belum ada |
| `tb_audio` | frekuensi nada sesuai tabel | ditunda bersama audio |

**Definition of Done** = SC-1 … SC-8 di §1, ditambah:
- `PORTING_NOTES.md` berisi pemetaan modul lama → baru, keputusan desain,
  batasan, dan daftar hal yang **harus diuji di board**.
- Tidak ada klaim "berjalan di hardware" tanpa bukti `BOARD`.

---

## 5. Risks & Roadmap

### 5.1 Risiko teknis

| ID | Risiko | Dampak | Mitigasi |
|---|---|---|---|
| R-1 | Timing closure gagal di 148,4375 MHz untuk renderer penuh (speed grade `-1`) | Tinggi | Pipeline jalur piksel ≥4 tahap; register semua output; jaga logika kombinasional tetap dangkal. **Mitigasi utama = pipeline.** Tidak boleh mengurangi resolusi atau menambah mode tanpa persetujuan baru pemilik |
| R-2 | Monitor pinjaman atau monitor demo tidak menerima 1080p nominal 60 Hz melalui VGA; model keduanya belum dipastikan | Tinggi | Cari tahu model dan dukungan mode masukan, lalu **uji di fase 2** dengan pola warna. Pilih monitor yang mendukung target tetap 1080p. Jangan menyamakan keberadaan port VGA dengan dukungan resolusi atau mengubah mode diam-diam. Konverter tidak dibutuhkan untuk jalur VGA langsung |
| R-3 | Jalur PS/2 ke PIC24 belum pernah diuji; keyboard+mouse pada satu pasangan PS/2 tidak bisa dibedakan dari framing | Tinggi | Uji keyboard nyata melalui PIC24. Lima tombol papan menjadi jalur penuh lain. Mouse tetap opsional dan hanya dikerjakan jika jalurnya terbukti |
| R-9 | Salah satu jalur kendali gagal atau penekanan beberapa tombol tidak diproses benar | Tinggi | Uji keyboard dan lima tombol terpisah, termasuk arah+aksi+lompat. Cegah penekanan tengah yang sama memicu START lalu PAUSE; jalur lain tidak menggantikan kewajiban membuktikan setiap jalur yang direncanakan |
| R-4 | BRAM/Logic tidak cukup setelah semua fitur masuk | Sedang | Ukur utilisasi tiap fase; sprite indeks 4-bit; tilemap padat; siapkan degradasi (kurangi frame animasi) |
| R-5 | Scope "lengkap sesuai brief" tidak selesai dalam 1–2 bulan | Tinggi | Fase berurutan dengan gate; fitur non-kritis dipangkas lebih dulu, dicatat sebagai deviasi |
| R-6 | Path mengandung spasi memecah Tcl | Rendah | `[list $path]` di semua script; rencana pindah path |
| R-7 | Audio tidak bisa dibuktikan (hardware belum ada) | Sedang | Ditunda resmi sebagai deviasi D-1; desain disiapkan untuk fase lanjutan |
| R-8 | Mesin build 16 GB RAM; Vivado 1080p bisa lambat | Rendah | Build batch, hindari GUI untuk iterasi |
| R-10 | Uji papan bergantung siklus "build → flash → lapor" manual; setiap gate `BOARD` butuh round trip | Sedang | Rancang **observabilitas on-board sejak fase 2**: pola uji warna, layar status (mode video, hasil input terdeteksi), kode LED/7-seg. Setiap flash harus memberi informasi diagnostik maksimal |

### 5.2 Roadmap (fase berurutan, tidak boleh loncat)

| Fase | Isi | Gate (bukti) |
|---|---|---|
| **0. Proposal judul (D0)** | Judul, tujuan & fungsi, cara kerja, rencana implementasi + bukti kelayakan (`SYN`) | Dokumen disetujui berdasarkan konfirmasi pemilik 2026-11-12. Tanggal persetujuan sebenarnya/status unggah BRONE belum diverifikasi, bukan penghalang menulis P2 |
| **1. Analisis** | Ringkasan perilaku modul repo acuan (fisika, goomba, item), daftar asumsi | Perbandingan platform/antarmuka dan draf P2 tersedia; tinjauan pemilik/penguncian parameter serta audit perilaku rinci belum selesai |
| **2. Fondasi video** | `clk_gen`, `reset_sync`, `vga_timing`, `scaler`, pola uji warna, XDC, `build.tcl` | `SYN` WNS≥0 + **`BOARD`** gambar stabil melalui VGA pada monitor yang mendukung 1080p |
| **3. Aset** | `sprites2vhdl.py`, palet, ROM sprite/tile/font/level | `SIM` render statis benar |
| **4. Input** | Keyboard: `ps2_rx` + `kbd_decoder`; papan: sinkronisasi, debounce, status/event lima tombol; mouse opsional `4b` | `SIM` + `BOARD` kedua jalur wajib diuji terpisah, termasuk kombinasi tombol dan tekan/tahan/lepas |
| **5. Gameplay inti** | `player` (fisika, tabrakan), kamera, animasi | `SIM` + `BOARD` Mario bisa bergerak |
| **6. Entitas** | Goomba, blok `?`, jamur, bunga api, fireball, koin, skor | `SIM` + `BOARD` interaksi benar |
| **7. Game FSM** | menu, pause, mati, game over, menang, HUD, timer, nyawa | `SIM` + `BOARD` alur lengkap |
| **8. Audio** | *(ditunda — §6 D-1)* | — |
| **9. Integrasi** | timing closure, utilisasi, dokumentasi, daftar uji board | `SYN` + `BOARD` + DoD |
| **10. Peta tambahan (opsional)** | Hingga empat peta tambahan dengan mekanik/aset bersama; hanya setelah satu level lengkap lulus fase sebelumnya | Uji tiap peta dan perpindahannya serta regresi SIM/SYN/BOARD; tidak menjadi syarat target minimum |

---

## 6. Deviasi dari brief (`Ide-awal.md`)

| ID | Brief | Keputusan | Alasan | Disetujui |
|---|---|---|---|---|
| **D-1** | Audio wajib: 3 kanal synth, SFX, BGM, PWM ke Pmod | **Ditunda** ke pengembangan lanjutan; desain tetap didokumentasikan | Hardware audio belum tersedia; tidak bisa dibuktikan bersuara | Pemilik, 2026-10-19 |
| **D-2** | `Ide-awal.md` = sumber requirement | **Digantikan** PRD ini; `Ide-awal.md` hanya referensi teknis | Dokumen awal tidak berbasis brief tugas akhir | Pemilik, 2026-10-19 |
| **D-3** | 1080p wajib | **Dipertahankan, hanya 1080p untuk v1**; tidak menambahkan mode kompatibilitas | Probe membuktikan clock, bukan game. Pilihan 1080p saja ditegaskan kembali setelah pembahasan fleksibilitas monitor; perubahan mode memerlukan persetujuan baru | Pemilik, 2026-10-19; ditegaskan 2026-11-12 |
| **D-4** | — (tidak dibahas) | Progres dilacak di `CHECKPOINTS.md`, bukan knowledge graph | Proyek tidak berjangka panjang/masif | Pemilik, 2026-10-19 |
| **D-5** | — (tidak dibahas) | Kontributor hanya menyentuh `docs/` + `sim/` | Interface RTL harus dikunci agar tidak regresi | Pemilik, 2026-10-19 |
| **D-6** | Peringatan mouse+keyboard | Mouse opsional; keyboard wajib. D-13 menambahkan lima tombol sebagai jalur penuh lain | Hanya 1 port USB-HID; hub belum tersedia | PRD; diperbarui mengikuti D-13 |
| **D-7** | Brief menyebut "satu ROM palet 16 entri" | **4 bank palet × 16 entri** (2 bit bank-select per sprite) | 15 warna terpakai terlalu sempit untuk 17 jenis aset; kegagalan baru terlihat di fase aset | Builder, 2026-10-19 |
| **D-8** | Input hanya keyboard + mouse | Riwayat: jalur cadangan `sw[15:12]` + `btnU`; kebutuhan aktif **digantikan D-13** | Mitigasi lama dipertahankan sebagai riwayat, bukan kewajiban kendali saklar tambahan | Builder, 2026-10-19; digantikan keputusan pemilik 2026-11-12 |
| **D-9** | Mouse "wajib untuk menu" | Mouse **de-scoped ke fitur opsional 4b** | Satu pasangan PS/2 tidak addressable; mouse & keyboard tidak bisa dibedakan dari framing | Builder, 2026-10-19 |
| **D-10** | Brief menyebut fixed-point "mis. Q8.8" | **Q13.8 untuk posisi**, Q8.8 untuk kecepatan | Q8.8 saturasi di ±127,996; level butuh sampai 3392 px. Sempat ditulis Q12.8, tetapi 20-bit signed hanya mencapai ±2.047,996 → **dikoreksi ke Q13.8 (21-bit)** 2026-10-22 | Builder, 2026-10-19; koreksi 2026-10-22 |
| **D-11** | Perangkat tampilan sebelumnya direncanakan TV HDMI dengan konverter | **Jalur utama VGA langsung ke monitor** | Pemilik memilih monitor VGA sebagai layar utama. Monitor uji akan dipinjam dan unit demo belum ditentukan; model/kecocokan 1080p tetap perlu dibuktikan. Tidak memerlukan konverter pada jalur utama ini | Pemilik, 2026-11-12 |
| **D-12** | Satu level sebagai lingkup awal | **Satu level lengkap wajib; hingga empat level tambahan opsional** | Peta berbeda dengan mekanik/aset bersama. Tambahan dilakukan setelah dasar satu level terbukti; bukan lima level wajib dan bukan lima set fitur baru | Pemilik, 2026-11-12 |
| **D-13** | Keyboard utama dan kendali saklar cadangan | **Dua jalur penuh wajib: keyboard dan lima tombol papan**; pemetaan papan beserta tekan/tahan disetujui | Atas/bawah untuk menu, tengah konfirmasi; kiri/kanan bergerak, atas lompat, bawah lari/bola api, tengah pause. Reset diputuskan terpisah pada D-14; pemetaan keyboard pada D-15 | Pemilik, 2026-11-12 |
| **D-14** | Pemicu dan efek reset belum dipilih | **sw[0] aktif 1 menahan reset; kembali 0 menuju menu; START memulai permainan baru, high score dipertahankan** | Pemilik memilih saklar lalu menyetujui urutan dan efek setelah penjelasan. Reset sesi terpisah dari respawn; konfigurasi FPGA tidak dihapus | Pemilik, 2026-11-12 |
| **D-15** | Pemetaan keyboard awal belum dikonfirmasi pada sesi P2 | **Pemetaan keyboard dan aturan tekan/tahan disetujui** | Panah/A-D bergerak; Space/atas/W lompat; Shift kiri/Z lari/bola api; atas/bawah menu; Enter konfirmasi; P/Esc pause. Reset tetap sw[0], satu aksi per penekanan fisik, tanpa tembakan otomatis | Pemilik, 2026-11-12 |
| **D-16** | Diagram umum sebelumnya dibuat sebagai SVG otomatis | **Diagram umum native draw.io, hitam-putih dan mudah dipahami, disetujui sebagai acuan repo/P2** | Blok fungsi tetap mencakup modul, koneksi dan I/O; Player/Enemy/Items terpisah, label English singkat. Sumber editable .drawio, bukan gambar tertanam. Detail entity/sinyal berada pada tabel/uraian | Pemilik, 2026-11-12, setelah review screenshot |

---

## 7. Keputusan pemilik & pertanyaan terbuka

### 7.1 Sudah dijawab (2026-10-19)

| ID | Pertanyaan | Jawaban | Dampak ke PRD |
|---|---|---|---|
| Q-1 | Spesifikasi alat | **Basys 3, Xilinx Artix-7 `XC7A35T-1CPG236C`** | §4.1 final, target tidak berubah |
| Q-2 | Rubrik penilaian | Diperoleh → `docs/rubrik.md` (lokal) | Prioritas mengikuti bobot; kelayakan 30% → bukti `SYN` masuk proposal |
| Q-3 | Ketentuan tugas akhir | `docs/brief/proyek-1.pdf` (lokal); tahap 1 = **usulan judul** | Ditambah §1.1 + deliverable D0 |
| Q-4 | Jalur tampilan dan kebutuhan konverter | **Diperbarui 2026-11-12:** VGA langsung menjadi jalur utama. Monitor uji perlu dipinjam dan monitor demo belum ditentukan | Konverter bukan kebutuhan jalur utama; R-2 sekarang memantau dukungan 1080p monitor, lihat Q-13 |
| Q-6 | Batas waktu | **Maksimum 2 bulan**, target lebih cepat, kualitas utama | Roadmap §5.2 penuh, gate per fase |
| Q-7 | Akses board | Basys 3 tersedia; JTAG pernah mendeteksi target. Penggantian SRAM diagnostik diizinkan; SPI flash dilarang | Pemrograman tidak membuktikan BOARD. Hasil tombol/keyboard/gambar memerlukan tindakan/pengamatan pemilik atau jalur observasi yang benar-benar terverifikasi |
| Q-9 | Input cadangan `sw`/`btn` | Keputusan lama D-8 **digantikan D-13**: lima tombol menjadi jalur penuh | §4.3 dan US-13 diselaraskan; reset disetujui melalui D-14, pemetaan keyboard melalui D-15 |

### 7.2 Masih terbuka

| ID | Pertanyaan | Dampak bila tidak dijawab |
|---|---|---|
| Q-5 | USB hub / dukungan mouse bersamaan | Tidak menjadi syarat baseline; mouse tetap opsional dan belum terverifikasi |
| Q-8 | Bukti perilaku **PIC24 USB-HID**: satu pasangan PS/2 di-multiplex, atau ada pasangan kedua? | Menentukan hidup/matinya fitur mouse (D-9) |
| Q-10 | Tanggal pengumpulan D0 yang sebenarnya / status unggah | Metadata akademik belum diverifikasi; D0 telah disetujui dan pertanyaan ini tidak menghalangi P2 |
| Q-11 | Daftar judul kelompok lain (`s.ub.ac.id/8sw` → **403**, butuh login) | Risiko judul bentrok dengan kelompok lain |
| Q-12 | Format laporan akhir kuliah D2 (template, bab wajib) | Untuk laporan akhir berikutnya; ketentuan lima bagian/rubrik P2 sudah tersedia dan tidak menunggu pertanyaan ini |
| Q-13 | Model monitor pinjaman dan monitor demo, serta dukungan 1920×1080 nominal 60 Hz melalui VGA | Menghalangi klaim/uji BOARD video sampai diketahui dan diuji, tetapi tidak menghalangi perancangan P2 atau uji input terpisah |
