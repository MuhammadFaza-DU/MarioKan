# Panduan input MarioKan

**Diperbarui:** 2026-11-12.

Dokumen ini membedakan perangkat kendali, cara penyambungan, dan status fungsi
tombol. Setelah memahami contoh penekanan, pemilik **menyetujui pemetaan lima
tombol papan beserta perilaku tekan/tahannya pada 2026-11-12**. Reset melalui
saklar nomor 0 dan pemetaan keyboard kemudian disetujui terpisah pada tanggal
yang sama. Persetujuan desain ini
bukan bukti bahwa game sudah diimplementasikan atau diuji.

## 1. Dua perangkat kendali yang berbeda

### Lima tombol pada papan FPGA Basys 3

Papan memiliki lima tombol tekan yang tersusun seperti tanda tambah:

```text
                    Tombol ATAS
                       btnU

Tombol KIRI       Tombol TENGAH       Tombol KANAN
   btnL               btnC               btnR

                    Tombol BAWAH
                       btnD
```

| Nama lengkap | Identifier VHDL | Arti huruf |
|---|---|---|
| Tombol atas pada papan | `btnU` | Up, atas |
| Tombol bawah pada papan | `btnD` | Down, bawah |
| Tombol kiri pada papan | `btnL` | Left, kiri |
| Tombol kanan pada papan | `btnR` | Right, kanan |
| Tombol tengah pada papan | `btnC` | Center, tengah |

Huruf pada identifier tersebut menjelaskan posisi tombol di papan. Huruf itu
**bukan perintah untuk menekan huruf U, D, L, R, atau C pada keyboard**.
Dalam penjelasan untuk pemakai, tulis nama lengkapnya, bukan hanya singkatan.

Diagram posisi mengacu pada orientasi normal papan, bukan setiap orientasi
foto. Jika papan/foto diputar, identifikasi tombol melalui label PCB
`BTNU`, `BTND`, `BTNL`, `BTNR`, dan `BTNC`. Jangan menentukan fungsi atau nama
tombol hanya karena letaknya berada di atas/kiri pada foto yang diputar.

### Keyboard USB eksternal

Keyboard eksternal disambungkan ke **port USB HID pada Basys 3**, bukan
dianggap terbaca melalui kabel programmer laptop. Pengendali PIC24 pada papan
menjadi perantara: sisi FPGA menerima clock dan data PS/2, lalu decoder VHDL
menerjemahkannya menjadi status tombol.

```text
Keyboard USB eksternal
    -> port USB HID pada Basys 3
    -> pengendali PIC24 pada papan
    -> jalur PS/2
    -> penerima dan decoder di FPGA
```

`PS2Clk` dan `PS2Data` adalah nama sinyal antarmuka FPGA. Penggunaan nama
PS/2 tidak berarti keyboard harus memiliki konektor PS/2 bulat; perangkat
yang direncanakan adalah keyboard USB yang ditangani pengendali pada papan.
Kompatibilitas keyboard nyata tetap perlu diuji.

### Kabel programmer laptop bukan jalur keyboard

Kabel laptop ke konektor pemrograman/daya papan digunakan untuk komunikasi
pemrograman/debug yang didukung antarmukanya. **Keyboard laptop tidak otomatis
diteruskan menjadi input game FPGA melalui kabel tersebut.** Dukungan kendali
dari keyboard laptop akan memerlukan protokol dan implementasi tambahan;
hal itu belum ditetapkan sebagai jalur kendali MarioKan.

Port untuk keyboard, konektor pemrograman, dan konektor keluaran VGA mempunyai
fungsi berbeda. Jangan menyebut semuanya sebagai satu jalur USB.

## 2. Fungsi kendali P2 dan status keputusan

**Kolom tombol papan dan keyboard: disetujui melalui pembahasan terpisah.**
Kedua jalur wajib diimplementasikan untuk
kendali penuh, sehingga pemain boleh memakai salah satunya.

| Keadaan dan tindakan | Tombol pada papan FPGA | Tombol pada keyboard eksternal |
|---|---|---|
| Menu: pindahkan pilihan ke atas | Tombol atas (`btnU`) | Panah atas |
| Menu: pindahkan pilihan ke bawah | Tombol bawah (`btnD`) | Panah bawah |
| Menu: konfirmasi pilihan atau mulai | Tombol tengah (`btnC`) | `Enter` |
| Bermain: bergerak ke kiri | Tombol kiri (`btnL`) | Panah kiri atau huruf `A` |
| Bermain: bergerak ke kanan | Tombol kanan (`btnR`) | Panah kanan atau huruf `D` |
| Bermain: lompat | Tombol atas (`btnU`) | `Space`, panah atas, atau huruf `W` |
| Bermain: lari atau tembak saat memiliki kemampuan api | Tombol bawah (`btnD`) | `Shift` kiri atau huruf `Z` |
| Bermain: pause atau lanjut | Tombol tengah (`btnC`) | Huruf `P` atau `Esc` |

Contoh perbedaan yang mudah tertukar: **tombol bawah pada papan (`btnD`)**
dipakai untuk aksi, tetapi **huruf `D` pada keyboard** untuk bergerak ke kanan.

Fungsi tombol dapat berbeda menurut keadaan game. Pada pemetaan papan ini,
tombol tengah mengonfirmasi menu saat berada di menu, tetapi mengaktifkan
pause saat sedang bermain. Perilaku itu ditentukan oleh logika VHDL, bukan
fungsi bawaan tombol fisik.

### Contoh penekanan tombol papan yang disetujui

| Tindakan | Cara menekan tombol fisik Basys 3 |
|---|---|
| Berjalan ke kanan | Tahan tombol kanan |
| Melompat ke kanan | Tahan kanan, lalu tekan atas |
| Berlari ke kanan | Tahan kanan dan bawah bersamaan |
| Berlari sambil melompat | Tetap tahan kanan dan bawah, lalu tekan atas; tiga tombol bersamaan |
| Menembak | Saat Fire Mario, tekan bawah sekali; arah tembakan mengikuti arah hadap, dengan batas jumlah bola aktif |
| Pause / lanjut | Tekan lalu lepas tengah; tekan lagi untuk melanjutkan |

- Lompat: satu penekanan memulai satu lompatan. Menahan atas lebih lama
  menghasilkan lompatan lebih tinggi; melepas lebih cepat menghasilkan
  lompatan lebih pendek. Tidak melompat berulang otomatis saat atas terus ditahan.
- Aksi: menahan bawah bersama arah membuat Mario berlari. Saat Fire Mario,
  tepi penekanan bawah meminta satu tembakan; tahan tidak menembak terus.
  Lepas lalu tekan kembali untuk meminta tembakan berikutnya.
- Menu/pause: satu penekanan hanya menghasilkan satu aksi. Menahan tengah
  ketika memilih START tidak boleh langsung membuat permainan pause;
  pemain harus melepasnya lalu menekan lagi.

Pemilik menyetujui skema ini setelah contoh tiga tombol bersamaan dijelaskan.
Kenyamanan dan fungsi nyata tetap perlu diuji pada papan, bukan dianggap
terbukti hanya karena pemetaannya telah disetujui.

### Contoh keyboard yang disetujui

Keyboard yang dimaksud adalah perangkat eksternal di port USB HID Basys 3,
bukan keyboard laptop. Pilihan tombol alternatif pada tabel berarti cukup
memakai salah satunya.

- Berlari sambil melompat ke kanan: tahan `D` + `Shift` kiri, lalu tekan `Space`.
- Tahan tombol lompat lebih lama untuk lompatan lebih tinggi; tidak memulai
  lompatan baru otomatis saat terus ditahan.
- Saat Fire Mario, satu penekanan `Shift` kiri atau `Z` meminta satu tembakan
  jika batas bola aktif mengizinkan. Tahan bersama arah untuk lari, bukan
  menembak terus-menerus. Lepas lalu tekan lagi untuk tembakan berikutnya.
- Menu/pause satu aksi per penekanan, bukan berulang karena keyboard
  mengirim ulang kode tombol yang masih ditahan.
- Reset tetap memakai saklar nomor 0, sama seperti pemain tombol papan.

## 3. Reset melalui saklar nomor 0 (disetujui)

`sw[0]` berarti saklar geser bernomor 0 pada papan. Saklar bertahan pada posisi
yang dipilih. Tombol tekan berbeda: setelah dilepas, tombol kembali ke keadaan
tidak ditekan.

**Keputusan pemilik 2026-11-12:**

1. `sw[0] = 1`: batalkan sesi dan tahan game dalam keadaan reset.
2. Kembalikan `sw[0] = 0`: masuk menu utama, tidak langsung bermain.
3. Pilih START: permainan baru dari awal, dengan tiga nyawa, skor/koin nol,
   waktu awal, dan blok/peta seperti awal.

High score yang sudah tersimpan tetap dipertahankan oleh reset saklar selama
papan menyala. Penyimpanannya tidak persisten: tidak dijanjikan bertahan
setelah daya mati atau FPGA diprogram ulang. Reset ini tidak menghapus
program FPGA dan tidak menulis SPI flash.

Saklar berlaku untuk pemain keyboard maupun pemain lima tombol papan.
Tombol tengah tetap konfirmasi menu atau pause/lanjut; tidak ditambah fungsi
reset tekan lama.

Reset sesi berbeda dari pause dan respawn. Pause melanjutkan keadaan yang
sama; respawn setelah mati mengurangi nyawa tetapi mempertahankan skor/koin
dan perubahan blok. Permainan baru setelah reset justru memulihkan peta awal.
Draf mekanisme pemulihan peta sudah ditulis pada rancangan teknis P2;
parameter/implementasi dan pengujiannya belum dikunci atau dibuat.

**Belum dites SIM/SYN/BOARD.** Jangan menganggap saklar sudah melakukan ini
pada program yang sedang termuat. Uji kelak dengan menahan 1, melepas ke 0,
memastikan menu tidak langsung mulai, lalu memeriksa sesi baru dan high score.

## 4. Batas bukti dan pekerjaan berikutnya

- Pemeriksaan perangkat tanggal 2026-11-12: Windows mendeteksi antarmuka FTDI,
  dan Vivado mendeteksi `xc7a35t_0` melalui JTAG. Status konfigurasi DONE=1.
  Desain yang sedang termuat belum diidentifikasi. Bukti tersimpan di
  `.tmp/build/hardware-inspection.txt` dan `.tmp/build/hardware-inspection.log`.
- Pemeriksaan tersebut **bukan uji fungsional BOARD** untuk tombol, keyboard,
  game, VGA, atau konverter. Tidak ada bitstream yang dimuat atau perangkat
  yang direset pada pemeriksaan tersebut.
- **SIM pemetaan input: belum dites.** Setelah rancangan disetujui dan RTL ada,
  uji debounce, tekan/tahan/lepas, navigasi menu, pause, dan tombol bersamaan.
- **SIM diagnostik mentah:** `tb_input_probe` lulus untuk debounce/hold/kombinasi
  tombol, byte/prefix PS/2, parity/stop/timeout, pemulihan dan reset diagnostik.
  Ini bukan decoder pemetaan penuh, START/pause atau reset sesi game.
- **SYN diagnostik input:** `input_probe_top` 148,4375 MHz, WNS +2,068 ns /
  WHS +0,128 ns, 99 LUT/216 FF, 0 latch/DRC/critical warning. Berkas dan
  panduan LED di `.tmp/diagnostics/`; bitstream belum diprogram.
- **BOARD pemetaan/input: belum dites.** Diagnostik siap untuk langkah uji
  mentah, tetapi tetap memerlukan pemuatan SRAM dan penekanan/pengamatan nyata.
  Pengujian gameplay kedua jalur memerlukan RTL game berikutnya; JTAG saja
  tidak mencukupi.
- Pemetaan lima tombol papan, reset saklar, dan pemetaan keyboard disetujui
  setelah penjelasan terpisah. Izin diagnostik SRAM tidak menggantikan
  persetujuan desain atau bukti pengujian fungsional.
- Pemilik menyatakan keyboard USB eksternal sudah terpasang dan program SRAM
  yang sedang berjalan boleh diganti untuk diagnostik. Foto papan pada
  2026-11-12 memperlihatkan kabel pada konektor PROG dan USB HID, serta
  konektor VGA yang tampak belum terpasang kabel pada saat foto diambil.
  Ujung kabel keyboard dan perangkat konverter/layar tidak terlihat pada foto
  tersebut; kompatibilitas keduanya belum dibuktikan oleh foto itu.

## 5. Konektor bawaan bukan rangkaian tambahan

Papan Basys 3 sudah menyediakan FPGA, tombol, saklar, LED, seven-segment,
USB HID, dan keluaran VGA. Rancangan game inti tidak mensyaratkan merakit
PCB atau rangkaian tambahan.

Header hitam di tepi papan merupakan konektor bawaan, bukan aksesori tambahan.
Pertanyaan pemeriksaan sambungan hanya menanyakan apakah ada kabel/modul
eksternal yang ditancapkan ke header; bukan keharusan menambah rangkaian.
Keyboard eksternal dan monitor adalah periferal yang disambungkan ke port
yang sesuai. Audio tetap ditunda.

Pemilik memilih VGA langsung sebagai jalur layar utama dan menegaskan
**1080p saja** pada 2026-11-12. Monitor untuk pengujian masih harus dipinjam;
monitor demo akhir belum ditentukan. Konverter tidak diperlukan pada jalur
VGA langsung, tetapi dukungan 1080p monitor tetap belum diverifikasi.

Rujukan perangkat: [Basys-3-Master.xdc resmi Digilent](https://github.com/Digilent/digilent-xdc/blob/master/Basys-3-Master.xdc).
Requirement dan perubahan keputusan tetap dikelola di [PRD](PRD.md), dengan
progres di [CHECKPOINTS.md](../CHECKPOINTS.md).
