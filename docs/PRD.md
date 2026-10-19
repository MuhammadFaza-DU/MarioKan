# PRD — MarioKan

**Versi:** 0.1 (draft)
**Tanggal:** 2026-10-19
**Pemilik:** Muhammad Faza
**Status:** menunggu review pemilik + 3 dokumen eksternal (lihat §7)

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
*clock-enable* 60 Hz, input keyboard/mouse lewat PS/2, fisika *fixed-point*,
dan FSM game lengkap (menu → main → mati/menang → game over).

Pendekatan kunci: **resolusi logika 384×216 di-upscale integer ×5** ke 1080p.
Ini membuat renderer hanya perlu menghitung 1 piksel logika per 5×5 piksel
layar, sehingga beban komputasi jatuh drastis tanpa mengorbankan ketajaman.

### Success Criteria (terukur)

| # | Kriteria | Cara ukur |
|---|---|---|
| SC-1 | Bitstream dihasilkan untuk `xc7a35tcpg236-1` | `write_bitstream` sukses, file `.bit` ada |
| SC-2 | **WNS ≥ 0** dan **WHS ≥ 0** pada clock pixel | `report_timing_summary` |
| SC-3 | **0 latch** terinferensi, 0 critical warning | laporan sintesis |
| SC-4 | Semua port top punya `PACKAGE_PIN` + `IOSTANDARD` | 0 warning `NSTD-1` / `UCIO-1` |
| SC-5 | Utilisasi di bawah kapasitas board | `report_utilization` (LUT ≤ 20.800, FF ≤ 41.600, BRAM ≤ 50, DSP ≤ 90) |
| SC-6 | Gambar tampil stabil 1080p60 di TV lewat konverter | uji papan, tidak ada tearing/blank |
| SC-7 | Game dapat dimainkan penuh: menu → level → menang | uji papan, skenario uji tertulis |
| SC-8 | Semua aturan menang/kalah terpicu sesuai §4.6 | testbench + uji papan |

### 1.1 Konteks akademik & deliverable

Proyek ini adalah tugas akhir mata kuliah **Sistem Digital Lanjut**, dikerjakan
bertahap. Tahap yang sedang berjalan: **Proyek 1 — Usulan Judul**
(sumber: `docs/brief/proyek-1.pdf`, rubrik: `docs/rubrik.md`).

| Deliverable | Isi | Status |
|---|---|---|
| **D0 — Proposal judul** | Judul, tujuan & fungsi, cara kerja (input/proses/output), rencana implementasi VHDL di Basys 3. PDF diunggah via BRONE | **belum ditulis — prioritas sekarang** |
| D1 — RTL + bitstream | Semua modul §4.4, `build.tcl`, XDC, bitstream | belum ada |
| D2 — Laporan kuliah | Dokumen akademik terpisah dari PRD | belum ada |
| D3 — Slide / video demo | Materi presentasi + rekaman board | belum ada |
| D4 — Dokumentasi teknis | `PORTING_NOTES.md`, diagram arsitektur, `checkpoint.md` | sebagian |

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
- AC: **bila mouse tidak terdeteksi, kursor disembunyikan dan game tetap 100% berfungsi dengan keyboard.**
- AC: bila jalur mouse **tidak terbukti ada** (§4.3), fitur ini batal dan **tidak dihitung** sebagai kekurangan.

**US-4 — Bermain**
Sebagai pemain, saya ingin berjalan, berlari, dan melompat dengan responsif.
- AC: jalan dengan `←`/`→` atau `A`/`D`; lari dengan `Shift`/`Z`.
- AC: lompat dengan `Space`/`↑`/`W`; **tinggi lompat bergantung lama tombol ditahan**.
- AC: gerakan tidak menembus tile padat (tabrakan X dan Y diselesaikan terpisah).

**US-5 — Musuh**
Sebagai pemain, saya ingin Goomba berjalan dan bisa diinjak.
- AC: Goomba berjalan, berbalik di dinding dan di tepi platform.
- AC: diinjak dari atas → animasi *squished* → hilang + skor + suara.
- AC: disentuh dari samping/bawah saat *small* → mati; saat *big/fire* → menyusut + invincible ±2 detik (berkedip).

**US-6 — Power-up & item**
Sebagai pemain, saya ingin memukul blok `?` dan mengambil jamur/bunga.
- AC: blok `?` dipukul dari bawah → mengeluarkan koin **atau** jamur (animasi naik) → berubah jadi blok kosong.
- AC: jamur bergerak, disentuh → Mario *big* (sprite 16×32) + skor + suara.
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
- AC: urutan mati: musik berhenti → animasi `mario_dead` → nyawa −1 → respawn **atau** GAME OVER bila nyawa 0.
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
- AC: kontributor tidak dapat merusak RTL tanpa review (aturan tertulis + CODEOWNERS).

### 2.3 Non-Goals (v1)

- Multi-level / world map.
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
| Display | TV **HDMI-only** + konverter VGA→HDMI (**sudah dimiliki**) | dikonfirmasi |
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
(deviasi **−0,042%** dari 148,5 MHz, jauh di bawah toleransi 0,5%).
Status: **`SYN`** — period terukur 6,737 ns, WNS +4,041 ns, 0 DRC error.

**Resolusi logika: 384×216**, di-upscale integer **×5** → 1920×1080 tepat.

- Grid tile 8×8 → **48×27 tile**.
- Strip HUD 24 px (3 baris tile) di atas + area bermain 192 px (24 baris tile) = 216 px.
- Upscale memakai **dua counter sub-piksel 0..4** (x dan y), **bukan pembagi**.
- **Tanpa framebuffer.** Arsitektur *racing the beam*: tilemap di BRAM, sprite
  ROM di BRAM, prioritas layer dihitung per piksel logika.
- `hsync`, `vsync`, `de`, dan RGB **diregister bersamaan** agar sejajar.
- Pipeline jalur piksel minimal 4 tahap (koordinat → alamat ROM → data → palette → output).
- Modul timing **parameterized lewat generic**, tetapi **grid logika 384×216
  dikunci untuk v1**. Penting: turun ke 720p **bukan** sekadar ganti angka —
  integer scale 720p memaksa grid logika lain (320×180 → 22,5 baris tile;
  256×144 → 8 metatile tinggi), yang berarti level, HUD, tinggi pipa/tangga,
  dan penempatan aset **harus disusun ulang**. Karena itu 720p berstatus
  **kontingensi terdokumentasi**, bukan janji "cukup ganti parameter".
  Mitigasi utama kegagalan timing adalah **pipeline**, bukan penurunan resolusi.

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

**Keyboard (wajib, jalur utama)**
- `ps2_rx`: sinkronisasi 2-FF, deteksi falling edge, frame 11 bit
  (start, 8 data LSB-first, parity ganjil, stop), cek parity, timeout.
- `kbd_decoder`: scancode **set 2**, tangani prefix `E0` (extended) dan `F0`
  (break). Keluaran = **status tombol ditahan** (bukan event sesaat).
- Pemetaan:

| Fungsi | Tombol |
|---|---|
| Kiri / Kanan | `←` `→` atau `A` `D` |
| Lompat | `Space` / `↑` / `W` |
| Lari / tembak | `Left Shift` / `Z` |
| Menu naik/turun | `↑` `↓` |
| Pilih | `Enter` |
| Pause | `P` / `Esc` |

**Jalur input cadangan (disetujui pemilik, 2026-10-19)**

- `sw[15:13]` = kiri / kanan / lompat; `sw[12]` = aksi (lari/tembak).
- `btnU` = lompat (duplikat, untuk kemudahan demo).
- Fungsi: **demo/debug fallback** bila jalur PS/2 gagal saat presentasi.
  **Tidak menggantikan** keyboard; keyboard tetap jalur utama dan wajib berfungsi.
- Biaya ± belasan LUT. Wajib didokumentasikan di `README` dan `PORTING_NOTES.md`
  sebagai fitur *non-spec* (lihat deviasi D-8).

**Mouse (opsional, graceful degradation — status: belum tervalidasi)**
- `ps2_tx`: kirim `0xFF` (reset) → tunggu `0xFA 0xAA 0x00` → `0xF4` (enable reporting).
- Parser paket 3 byte (tombol, ΔX, ΔY; bit tanda & overflow), akumulasi posisi, clamp.
- Kursor 8×8/16×16, hover + klik kiri pada tombol menu.
- **Bila tidak ada paket mouse valid dalam N detik → kursor disembunyikan, game tetap penuh via keyboard.**

**Batasan protokol yang harus diakui (temuan builder check, 2026-10-19):**
Basys3 hanya punya **satu** pasangan PS/2 (`PS2Clk` C17 / `PS2Data` B17). PS/2
**tidak addressable** — tidak ada ID perangkat di dalam frame. Paket mouse
3-byte punya framing 11-bit dan parity ganjil yang **identik** dengan tiga
scancode keyboard, sehingga `ps2_rx` tidak bisa membedakan perangkat hanya
dari framing. Selain itu `ps2_tx` harus memakai jalur open-drain yang sama
dengan keyboard yang sedang aktif bicara → arbitrase arah harus dirancang.

**Konsekuensi keputusan:**
- **Keyboard adalah satu-satunya jalur input yang wajib dan dijamin** untuk v1.
- **Mouse berstatus fitur opsional `4b`**, dikerjakan **hanya jika** terbukti
  ada jalur perangkat mouse yang bisa dibedakan (mis. PIC24 mengekspos
  pasangan PS/2 kedua, atau bukti firmware meneruskan trafik mouse).
- Bila tidak terbukti: `ps2_tx`, `mouse_decoder`, dan kursor **dibatalkan dari
  scope**, menu tetap 100% berfungsi via keyboard. Ini **bukan** kegagalan
  fitur — ini keputusan berbasis bukti.
- **Bukti yang dibutuhkan:** dokumen/pengujian yang menunjukkan apakah PIC24
  Basys3 mengekspos dua pasangan PS/2 atau melakukan multiplexing. Sampai itu
  ada, mouse tidak dijanjikan.

### 4.4 Arsitektur modul

```
clk 100MHz ──► clk_gen (MMCME2_BASE) ──► clk_pix 148,4375 MHz + locked
btnC ──► reset_sync (tunggu locked)

PS2 kbd ──► ps2_rx ──► kbd_decoder ──┐
PS2 mouse ─► ps2_rx/tx ─► mouse_decoder ─┤─► input_mux ──► game_ctrl (FSM utama)
                                         │
        ┌────────────────────────────────┼──────────────────────────────┐
        ▼                ▼               ▼                              ▼
   player_phys     goomba_ctrl      items (mushroom,          hud_text / timer
   (fisika Mario)  (musuh)          fireflower, coin,         (skor, nyawa, waktu)
        └────────────┬───────────────┘
                     ▼
              level_rom / tilemap (BRAM) ──► collision (tile + AABB)

vga_timing (1080p) ──► pixel_xy ──► scaler ──► renderer ──► RGB444 ──► VGA
                                                   ▲
                                    tile/sprite ROM + palette + font
```

**Hierarki file yang diharapkan** (nama boleh disesuaikan, pemisahan dipertahankan):

```
src/
  top_basys3.vhd        -- hanya wiring + pin
  clk_gen.vhd           -- MMCME2_BASE (UNISIM)
  reset_sync.vhd
  vga_timing.vhd        -- generic (1080p/720p/480p)
  scaler.vhd            -- koordinat layar -> koordinat logika (counter, tanpa divider)
  renderer.vhd          -- prioritas layer, palette lookup, output RGB444
  palette_pkg.vhd, tile_rom.vhd, level_rom.vhd, sprite_rom_*.vhd, font_rom.vhd
  ps2_rx.vhd, ps2_tx.vhd, kbd_decoder.vhd, mouse_decoder.vhd, input_mux.vhd
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
docs/PRD.md, docs/PORTING_NOTES.md, docs/checkpoint.md
```

**Audio** (`audio_synth.vhd`, `sfx_rom.vhd`, `bgm_rom.vhd`, `pwm_dac.vhd`)
didesain tetapi **tidak masuk v1** — lihat §6.

### 4.5 Aturan RTL (wajib)

- Bahasa: **VHDL** (VHDL-2008 diizinkan, diset per file). Constraint: **XDC**.
- Hanya `ieee.numeric_std`. **Dilarang** `std_logic_arith`, `std_logic_unsigned`, `std_logic_signed`.
- **Satu clock pixel** dari MMCM. Tidak ada derived clock dari counter — pakai **clock-enable**.
- Tick game 60 Hz diturunkan dari awal blanking vertikal (`frame_start`).
- Semua input asinkron lewat **sinkronisasi 2-FF**; tombol/PS/2 diberi debounce/glitch filter.
- Reset **sinkron**, aktif setelah `locked`.
- Tanpa latch, tanpa loop kombinasional. `Inferred latch` = **bug**, harus nol.
- Pembacaan BRAM **sinkron**; latensi pipeline dihitung dan sync disejajarkan.
- Tanpa `real`/floating point di logika sintesis → **fixed-point**, didefinisikan di `game_pkg.vhd`:
  - **Posisi dunia (`world_x`, `world_y`, `camera_x`) = Q12.8** (20-bit `signed`).
    Level terlebar 212 metatile × 16 px = **3392 px**, sementara Q8.8 hanya
    menjangkau ±127,996 → **Q8.8 tidak cukup untuk posisi**.
  - **Kecepatan (`vel_x`, `vel_y`) = Q8.8** (16-bit `signed`) — cukup untuk
    rentang kecepatan realistis dengan presisi sub-piksel.
  - Konversi ke koordinat layar: ambil bit integer dari Q12.8 (geser 8, tanpa divider).
- Pembagian/modulo konstanta non-pangkat-2 **dilarang** di jalur piksel.
- `inout` hanya di top untuk `PS2Clk`/`PS2Data` dengan buffer open-drain.

### 4.6 Aturan game (eksplisit, harus diimplementasikan persis)

**FSM utama:**
```
BOOT → MENU → (HOW_TO_PLAY) → PLAYING ⇄ PAUSED
                                  ├─(mati)──► DYING → (nyawa>0 ? PLAYING : GAME_OVER)
                                  └─(tiang bendera)──► LEVEL_CLEAR
GAME_OVER / LEVEL_CLEAR ──(Enter/klik)──► MENU
```

**Kalah** — Mario kehilangan satu kesempatan bila salah satu terjadi:
1. Menyentuh Goomba dari **samping/bawah** saat **small**.
   Saat **big/fire**: menyusut ke small + invincibility ±2 detik (berkedip), **tidak mati**.
2. **Jatuh ke jurang** (Y melewati batas bawah layar).
3. **Waktu habis** (timer HUD mencapai 0).

Urutan mati: musik berhenti → animasi `mario_dead` → nyawa −1 →
respawn di awal level (bila nyawa > 0) → GAME OVER bila 0. **Nyawa awal 3.**

**Semantik respawn (dikunci — menentukan arsitektur tilemap):**

| State | Saat mati → respawn |
|---|---|
| Tilemap (blok `?` yang sudah terpakai, bata pecah) | **TIDAK di-reset** (perilaku SMB). Satu tilemap mutable, **tanpa** ROM salinan dan **tanpa** FSM reload. |
| `SCORE`, `COINS` | **Dipertahankan** |
| `TIME` | **Di-reset** ke nilai awal level |
| Posisi Mario, kamera | **Di-reset** ke awal level |
| Musuh & item aktif | **Di-reset** (semua kembali ke posisi awal) |
| Nyawa | −1 |

> Konsekuensi yang diterima: pemain yang menghabiskan semua blok power-up lalu
> mati bisa lanjut sebagai *small* tanpa akses bunga api. Ini sama dengan
> perilaku SMB asli dan **bukan** bug. Bila kelak ingin reset penuh, itu
> menambah satu ROM level + FSM reload — perubahan arsitektur, bukan tweak.
> **Keputusan builder (2026-10-19).**

**Menang:** menyentuh **tiang bendera** di akhir level → animasi meluncur turun →
bonus skor berdasar ketinggian sentuh + bonus sisa waktu → `LEVEL_CLEAR`
(jingle) → tampil `COURSE CLEAR` + skor → kembali ke menu, high score diperbarui.

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

**Level:** satu level, ≈100–212 metatile lebar, 12 metatile tinggi.
Wajib memuat: **≥ 2 jurang, ≥ 4 Goomba, ≥ 3 blok `?` (koin/jamur/bunga),
pipa, tangga akhir, tiang bendera.** Format level harus mudah diubah
(teks → ROM VHDL lewat skrip).

### 4.7 Aset

- Sumber kebenaran sprite = **PNG asli** di repo acuan
  (`ECE385-HelperTools-master/.../sprite_originals/`, 24 file) — **tersedia, terverifikasi**.
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
- Input asinkron (PS/2, tombol, saklar): `set_false_path` ke register sinkronisasi.
- Semua port top **wajib** punya `PACKAGE_PIN` + `IOSTANDARD`.
- `tools/build.tcl`: `read_vhdl` → `read_xdc` → `synth_design -top top_basys3
  -part xc7a35tcpg236-1` → `opt/place/route` → `report_timing_summary`,
  `report_utilization`, `report_clock_utilization`, `report_drc` → `write_bitstream`.
- **Karena path repo mengandung spasi:** setiap argumen path di Tcl **wajib**
  dibungkus `[list ...]` (sudah diverifikasi).

### 4.9 Verifikasi

| Testbench | Isi | Status |
|---|---|---|
| `tb_vga_timing` | total 2200×1125, lebar sync, posisi `de` | belum ada |
| `tb_ps2` | frame scancode set 2 (make/break/`E0`), parity salah ditolak | belum ada |
| `tb_player` | tinggi lompat variabel, gravitasi, tabrakan lantai/dinding | belum ada |
| `tb_game_ctrl` | semua transisi FSM: mati (Goomba/jurang/waktu), menang | belum ada |
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
| R-1 | Timing closure gagal di 148,4375 MHz untuk renderer penuh (speed grade `-1`) | Tinggi | Pipeline jalur piksel ≥4 tahap; register semua output; jaga logika kombinasional tetap dangkal. **Mitigasi utama = pipeline.** Turun ke 720p **bukan** mitigasi murah: ia memaksa grid logika, level, dan HUD disusun ulang (lihat §4.2) → hanya dipakai sebagai kontingensi terakhir dengan rework terdokumentasi |
| R-2 | Konverter VGA→HDMI menolak clock 148,4375 MHz, atau hanya menerima input ≤720p (banyak konverter murah begini) | Tinggi | **Uji di fase 2** dengan pola uji warna, sebelum aset/level dibuat. Butuh model konverter (Q-4). Bila input 1080p tidak didukung → keputusan resolusi harus diambil **sebelum fase 3** |
| R-3 | Jalur PS/2 ke PIC24 belum pernah diuji; keyboard+mouse pada satu pasangan PS/2 tidak bisa dibedakan dari framing | Tinggi | Keyboard-first (wajib). Mouse = fitur `4b` opsional yang hanya dikerjakan bila ada bukti perangkat terpisah. Bila PS/2 gagal total → lihat R-9 |
| R-9 | Jalur PS/2 tidak berfungsi saat demo (risiko satu titik kegagalan pada acara ternilai) | Tinggi | Siapkan **jalur input cadangan** `sw[15:12]` sebagai D-pad + `btnU` sebagai lompat, didokumentasikan sebagai *debug/demo fallback* (bukan bagian spek). Biaya ± belasan LUT |
| R-4 | BRAM/Logic tidak cukup setelah semua fitur masuk | Sedang | Ukur utilisasi tiap fase; sprite indeks 4-bit; tilemap padat; siapkan degradasi (kurangi frame animasi) |
| R-5 | Scope "lengkap sesuai brief" tidak selesai dalam 1–2 bulan | Tinggi | Fase berurutan dengan gate; fitur non-kritis dipangkas lebih dulu, dicatat sebagai deviasi |
| R-6 | Path mengandung spasi memecah Tcl | Rendah | `[list $path]` di semua script; rencana pindah path |
| R-7 | Audio tidak bisa dibuktikan (hardware belum ada) | Sedang | Ditunda resmi sebagai deviasi D-1; desain disiapkan untuk fase lanjutan |
| R-8 | Mesin build 16 GB RAM; Vivado 1080p bisa lambat | Rendah | Build batch, hindari GUI untuk iterasi |
| R-10 | Uji papan bergantung siklus "build → flash → lapor" manual; setiap gate `BOARD` butuh round trip | Sedang | Rancang **observabilitas on-board sejak fase 2**: pola uji warna, layar status (mode video, hasil input terdeteksi), kode LED/7-seg. Setiap flash harus memberi informasi diagnostik maksimal |

### 5.2 Roadmap (fase berurutan, tidak boleh loncat)

| Fase | Isi | Gate (bukti) |
|---|---|---|
| **0. Proposal judul (D0)** | Judul, tujuan & fungsi, cara kerja, rencana implementasi + bukti kelayakan (`SYN`) | PDF terunggah via BRONE |
| **1. Analisis** | Ringkasan perilaku modul repo acuan (fisika, goomba, item), daftar asumsi | Dokumen ringkasan disetujui |
| **2. Fondasi video** | `clk_gen`, `reset_sync`, `vga_timing`, `scaler`, pola uji warna, XDC, `build.tcl` | `SYN` WNS≥0 + **`BOARD`** gambar tampil di TV |
| **3. Aset** | `sprites2vhdl.py`, palet, ROM sprite/tile/font/level | `SIM` render statis benar |
| **4. Input** | `ps2_rx`, `kbd_decoder`, `ps2_tx`, `mouse_decoder` | `SIM` + `BOARD` status tombol tampil di LED |
| **5. Gameplay inti** | `player` (fisika, tabrakan), kamera, animasi | `SIM` + `BOARD` Mario bisa bergerak |
| **6. Entitas** | Goomba, blok `?`, jamur, bunga api, fireball, koin, skor | `SIM` + `BOARD` interaksi benar |
| **7. Game FSM** | menu, pause, mati, game over, menang, HUD, timer, nyawa | `SIM` + `BOARD` alur lengkap |
| **8. Audio** | *(ditunda — §6 D-1)* | — |
| **9. Integrasi** | timing closure, utilisasi, dokumentasi, daftar uji board | `SYN` + `BOARD` + DoD |

---

## 6. Deviasi dari brief (`Ide-awal.md`)

| ID | Brief | Keputusan | Alasan | Disetujui |
|---|---|---|---|---|
| **D-1** | Audio wajib: 3 kanal synth, SFX, BGM, PWM ke Pmod | **Ditunda** ke pengembangan lanjutan; desain tetap didokumentasikan | Hardware audio belum tersedia; tidak bisa dibuktikan bersuara | Pemilik, 2026-10-19 |
| **D-2** | `Ide-awal.md` = sumber requirement | **Digantikan** PRD ini; `Ide-awal.md` hanya referensi teknis | Dokumen awal tidak berbasis brief tugas akhir | Pemilik, 2026-10-19 |
| **D-3** | 1080p wajib | **Dipertahankan** 1080p, dengan fallback 720p lewat generic | 1080p terbukti layak (`SYN` WNS +4,041 ns pada probe) | Pemilik, 2026-10-19 |
| **D-4** | — (tidak dibahas) | Progres dilacak di `docs/checkpoint.md`, bukan knowledge graph | Proyek tidak berjangka panjang/masif | Pemilik, 2026-10-19 |
| **D-5** | — (tidak dibahas) | Kontributor hanya menyentuh `docs/` + `sim/` | Interface RTL harus dikunci agar tidak regresi | Pemilik, 2026-10-19 |
| **D-6** | Peringatan mouse+keyboard | **Diperkuat**: keyboard adalah jalur utama, mouse opsional | Hanya 1 port USB-HID; hub belum tersedia | PRD |
| **D-7** | Brief menyebut "satu ROM palet 16 entri" | **4 bank palet × 16 entri** (2 bit bank-select per sprite) | 15 warna terpakai terlalu sempit untuk 17 jenis aset; kegagalan baru terlihat di fase aset | Builder, 2026-10-19 |
| **D-8** | Input hanya keyboard + mouse | Tambah **jalur cadangan** `sw[15:12]` + `btnU` sebagai demo fallback | Mitigasi risiko satu titik kegagalan PS/2 pada demo ternilai | Builder, 2026-10-19 |
| **D-9** | Mouse "wajib untuk menu" | Mouse **de-scoped ke fitur opsional 4b** | Satu pasangan PS/2 tidak addressable; mouse & keyboard tidak bisa dibedakan dari framing | Builder, 2026-10-19 |
| **D-10** | Brief menyebut fixed-point "mis. Q8.8" | **Q12.8 untuk posisi**, Q8.8 untuk kecepatan | Q8.8 saturasi di ±127,996; level butuh sampai 3392 px | Builder, 2026-10-19 |

---

## 7. Keputusan pemilik & pertanyaan terbuka

### 7.1 Sudah dijawab (2026-10-19)

| ID | Pertanyaan | Jawaban | Dampak ke PRD |
|---|---|---|---|
| Q-1 | Spesifikasi alat | **Basys 3, Xilinx Artix-7 `XC7A35T-1CPG236C`** | §4.1 final, target tidak berubah |
| Q-2 | Rubrik penilaian | Diperoleh → `docs/rubrik.md` | Prioritas mengikuti bobot; kelayakan 30% → bukti `SYN` masuk proposal |
| Q-3 | Ketentuan tugas akhir | `docs/brief/proyek-1.pdf`; tahap 1 = **usulan judul** | Ditambah §1.1 + deliverable D0 |
| Q-4 | Konverter VGA→HDMI | Belum bisa dicek; **diuji di fase 2** dengan pola uji | R-2 tetap terbuka, tidak memblokir fase 0–1 |
| Q-5 | USB hub | Belum diketahui | Mouse tetap fitur `4b` opsional |
| Q-6 | Batas waktu | **Maksimum 2 bulan**, target lebih cepat, kualitas utama | Roadmap §5.2 penuh, gate per fase |
| Q-7 | Akses board | **Basys3 bisa dicolok ke mesin ini** | Agent bisa flash & membaca hasil sendiri → bukti `BOARD` dapat dihasilkan langsung |
| Q-9 | Input cadangan `sw`/`btn` | **Disetujui** | Masuk §4.3 + deviasi D-8 |

### 7.2 Masih terbuka

| ID | Pertanyaan | Dampak bila tidak dijawab |
|---|---|---|
| Q-8 | Bukti perilaku **PIC24 USB-HID**: satu pasangan PS/2 di-multiplex, atau ada pasangan kedua? | Menentukan hidup/matinya fitur mouse (D-9) |
| Q-10 | Tanggal pengumpulan **D0 (proposal)** yang sebenarnya | Menentukan urgensi penulisan proposal |
| Q-11 | Daftar judul kelompok lain (`s.ub.ac.id/8sw` → **403**, butuh login) | Risiko judul bentrok dengan kelompok lain |
| Q-12 | Format laporan kuliah (template, bab wajib) | Menentukan isi deliverable D2 |
