# Audit aset dan kelayakan awal MarioKan

**Tanggal audit:** 2026-11-12.
**Status:** inventaris sumber dan perhitungan awal, bukan implementasi aset target
atau bukti game lengkap lulus SIM/SYN/BOARD.

## 1. Yang tersedia dan yang belum siap

Audit membaca langsung 30 PNG pada folder
`ECE385-HelperTools-master/PNG To Hex/On-Chip Memory/sprite_originals/`
di repo `nicklesimba/FPGA-Mario`, commit
`077d8a510f398e90e20650698b9795cc2d5f797e`.
Tree sumber: `d971da4a66c4db72d678df9da9829ba0f84e8fb1`.

Semua PNG tersebut berhasil dibuka dengan Pillow untuk memeriksa dimensi,
mode warna, transparansi, dan jumlah warna. Hasil rinci tersimpan di
`.tmp/asset-audit.json`. PNG dibaca dalam memori, tidak dipasang sebagai aset
final project.

Sumber mencakup pose Mario kecil/besar, kematian Mario, Goomba, koin,
bola api, jamur, blok tanda tanya, bata, tanah, dan logo. Tidak semua berkas
dalam folder itu diperlukan untuk MarioKan; keberadaan 30 berkas tidak berarti
semua kebutuhan aset game sudah terpenuhi.

Di project target, folder `assets/`, ROM sprite VHDL pada `src/`, dan alat
`tools/sprites2vhdl.py` **belum tersedia** pada saat audit. Sprite Fire Mario,
bunga api, lingkungan, font/HUD, dan elemen akhir level belum menjadi aset
target yang siap dipakai. Tidak adanya nama PNG tertentu di folder yang
diaudit juga tidak membuktikan gambarnya tidak direpresentasikan di tempat
lain pada repo acuan.

## 2. Sumber tidak boleh dipakai tanpa penyesuaian

Contoh hasil pengukuran PNG asli:

Normalisasi Mario kecil ke 16 x 16 merupakan ukuran rancangan yang perlu
ditinjau visualnya; ukuran Mario besar 16 x 32 sudah disebut dalam PRD.
Keduanya belum menjadi hasil konversi yang telah diuji.

| Berkas sumber | Ukuran sumber | Temuan |
|---|---|---|
| `mario_still_right.png` | 26 x 32 piksel | Berbeda dari usulan normalisasi Mario kecil 16 x 16 |
| `mario_big_still_right.png` | 21 x 42 piksel | Bukan ukuran target Mario besar 16 x 32 |
| `mario_big_walk_right_2.png` | 21 x 46 piksel | Tinggi kanvas antar-frame belum seragam |
| `mush.png` | 16 x 16 piksel | Dimensi sesuai satu metatile target |
| `qblock_blink_1.png` | 15 x 15 piksel | Kanvas harus dinormalisasi dengan frame lain |
| `tile_brick.png` | 20 x 19 piksel | Memiliki 70 warna sumber, melebihi satu palet target |
| `tile_ground.png` | 20 x 20 piksel | Memiliki 170 warna sumber dan tidak mempunyai alpha |
| `mario_logo.png` | 176 x 88 piksel | Memerlukan anggaran memori dan tata letak menu tersendiri |

Karena itu, konversi harus mencakup crop/padding yang ditinjau, penyeragaman
kanvas dan titik pijak animasi, penyesuaian ke grid target, serta kuantisasi
warna. Hindari resampling halus yang mengaburkan pixel art. Area tabrakan
harus didefinisikan terpisah dari padding gambar.

Contoh wrapper lama yang telah dibaca (`ram_mario_still_right.sv`,
`ram_mario_big_still_right.sv`, `ram_logo.sv`) memakai pemilihan warna
kombinasional dan path `$readmemh` absolut milik pengembang lama. Wrapper itu
tidak boleh disalin menjadi implementasi target. Target tetap VHDL, palet
RGB444, dan pembacaan BRAM sinkron.

## 3. Anggaran memori awal

Dengan asumsi setiap piksel sumber selesai dikonversi menjadi indeks 4-bit,
jumlah payload seluruh 30 PNG pada dimensi aslinya adalah **15.385 byte**.
Ini **bukan ukuran file PNG terkompresi**, bukan hasil konversi yang sudah
dibuat, dan bukan pemakaian BRAM hasil sintesis.

Artix-7 target menyediakan 50 blok BRAM36. Kapasitas mentahnya:

```text
50 x 36.864 bit = 1.843.200 bit = 225 KiB
```

Kapasitas efektif bergantung pada konfigurasi lebar/kedalaman, packing,
pembulatan alokasi, dan kebutuhan port. Selain gambar, anggaran harus
menyertakan tilemap, font, metadata, dan kebutuhan lain.

Sebagai pembanding, satu framebuffer 1920 x 1080 dengan RGB444 memerlukan:

```text
1920 x 1080 x 12 bit = 24.883.200 bit = 3.110.400 byte
```

Itulah alasan desain tidak menyimpan satu layar penuh. Renderer menggunakan
ulang gambar kecil untuk tile dan sprite saat piksel layar dipindai.
Perhitungan payload aset memberi **indikasi awal kapasitas memori memadai**,
tetapi tidak membuktikan utilisasi atau timing renderer lengkap.

Keputusan lingkup level 2026-11-12: satu level lengkap wajib dan hingga empat
peta tambahan opsional setelah dasar tersebut lulus. Peta tambahan memakai
mekanik/aset bersama, bukan lima salinan logika game. Sebagai ilustrasi saja,
asumsi satu byte per metatile pada peta 212 x 12 menghasilkan 2.544 byte per
peta atau 12.720 byte untuk lima peta. Ini bukan format tilemap yang sudah
diimplementasikan dan belum menghitung metadata, penyimpanan mutable,
pembulatan alokasi BRAM, atau kebutuhan port. Koordinat dan cara pemuatan
level tambahan perlu dirancang tersendiri bila fitur opsional diaktifkan;
jangan menganggap lima panjang level boleh digabungkan ke rentang Q13.8
tanpa pemeriksaan.

## 4. Alur penyiapan aset yang direncanakan

1. Pilih aset sumber dan catat asal/lisensinya; buang berkas yang tidak dipakai
   dari manifest target, bukan menghapus sumber acuan.
2. Tutup daftar kebutuhan yang belum tersedia; pratinjau aset baru atau adaptasi
   visual sebelum dianggap final.
3. Normalisasi kanvas, skala, titik pijak, transparansi, dan urutan animasi.
4. Petakan aset ke **empat bank palet**, masing-masing 16 entri RGB444 dengan
   indeks 0 untuk transparansi. Palet harus konsisten lintas aset/frame dalam
   bank yang sama, bukan palet baru bebas untuk setiap PNG.
5. Hasilkan data indeks, metadata sprite, dan ROM VHDL sinkron. Gambar menghadap
   kiri dapat memakai pencerminan alamat agar tidak menggandakan data gambar.
6. Uji ulang hasil konversi melalui rekonstruksi gambar dan pemeriksaan indeks,
   dimensi, bank palet, serta transparansi.
7. Uji pipeline renderer: indeks warna, bank, transparansi, dan sinyal video
   harus tetap sejajar melewati latensi ROM/palet.

## 5. Apa yang sudah dan belum dibuktikan pada FPGA

- **SYN arsip probe, bukan game:** laporan final `.tmp/probe/rpt_timing.txt`
  menunjukkan clock piksel sekitar 148,438 MHz, WNS +4,043 ns, WHS +0,254 ns.
  Laporan utilisasi probe menunjukkan 1 LUT, 28 register, 0 latch, dan 0 BRAM.
  Hasil tersebut tidak mengukur renderer, aset, atau gameplay lengkap.
- **SIM/SYN diagnostik input terpisah:** `tb_input_probe` lulus; SYN
  `input_probe_top` WNS +2,068 ns / WHS +0,128 ns, 99 LUT/216 FF, 0 BRAM.
  Tidak memuat ROM sprite/VGA dan belum diprogram; hasil ini tidak memperluas
  bukti utilisasi memori atau kesiapan aset target.
- **Deteksi perangkat saja:** Windows/FTDI dan Vivado/JTAG mendeteksi target
  `xc7a35t_0`; DONE=1. Isi desain yang sedang termuat tidak diidentifikasi,
  sehingga ini bukan uji fungsional BOARD untuk game.
- **SIM aset/renderer: belum dites.** Memerlukan ROM target dan testbench untuk
  memeriksa alamat, latensi, transparansi, layering, dan hasil piksel.
- **SYN game lengkap: belum dites.** Perlu synth, place, route, laporan utilisasi,
  WNS/WHS, DRC, dan pemeriksaan cakupan constraint pada desain terintegrasi.
- **BOARD gambar/game: belum dites.** Perlu bitstream yang sesuai, pemeriksaan
  monitor yang menerima 1080p melalui VGA langsung. Konverter bukan jalur
  utama yang dipilih; jika kelak dipakai, arah/kemampuannya perlu diuji terpisah.

Kesimpulan dibatasi: terdapat sumber gambar dan indikasi awal kelayakan memori,
tetapi aset target belum siap dan game lengkap belum terbukti pada FPGA.
