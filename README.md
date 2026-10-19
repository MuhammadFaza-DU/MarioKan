# MarioKan

Game platformer bergaya *Super Mario Bros.* yang berjalan sepenuhnya di FPGA
**Digilent Basys3** (`XC7A35T-1CPG236C`), ditulis dalam **VHDL**, dibangun dengan
**Vivado 2026.1**, output **VGA 1920×1080 @ 60 Hz**, input **keyboard/mouse PS/2**.

Proyek tugas akhir. Repo ini memuat kode RTL, constraint, tooling, simulasi,
dan seluruh dokumentasi teknis.

---

## Status (jujur, per titik terakhir)

Tingkat bukti yang dipakai di repo ini — **tiga tingkat, jangan dicampur**:

| Tingkat | Arti |
|---|---|
| `SIM` | Hanya terbukti lewat testbench / simulasi |
| `SYN` | Terbukti lewat sintesis + implementasi + timing (WNS/WHS) |
| `BOARD` | Terbukti berjalan di papan fisik |

| Item | Status | Bukti |
|---|---|---|
| Toolchain Vivado 2026.1 + device `xc7a35tcpg236-1` | `SYN` | `vivado -version` v2026.1; 30 varian `xc7a35t*` terpasang |
| MMCM 100 MHz → 148,4375 MHz (1080p) | `SYN` | `CLKFBOUT_MULT_F=11.875 / DIVCLK_DIVIDE=1 / CLKOUT0_DIVIDE_F=8` → `clk_pix period=6.737 ns`; **WNS +4.041 ns**, 0 DRC error, bitstream 2,19 MB terbentuk |
| Seluruh RTL game (video, input, gameplay, audio) | — | **belum ada** |
| Uji di papan fisik | — | **belum ada** |

> Bitstream uji di atas adalah desain *probe* (counter + MMCM), bukan game.
> Ia hanya membuktikan jalur toolchain dan kelayakan clock, **bukan** bahwa
> game sudah berjalan.

## Struktur repo

```
docs/
  PRD.md            spesifikasi operasional (sumber kebenaran requirement)
  rubrik.md         rubrik & ketentuan tugas dari dosen
  checkpoint.md     progres & riwayat kerja
  brief/            dokumen mentah: proyek-1.pdf, ide-awal.md
src/                RTL VHDL (menyusul)
constraints/        XDC Basys3
sim/                testbench VHDL
tools/              skrip Python/Tcl (konversi sprite, build batch)
```

## Build

```powershell
# dari root repo
D:\AMDDesignTools\2026.1\Vivado\bin\vivado.bat -mode batch -source tools/build.tcl
```

> **Catatan path:** path repo saat ini mengandung spasi
> (`Project dan SourceCode`). Vivado memecah argumen di spasi, jadi **setiap
> perintah Tcl yang menerima path wajib dibungkus `[list ...]`**:
> ```tcl
> read_vhdl -vhdl2008 [list $f]
> ```
> Ini sudah diverifikasi. Rencana jangka panjang: pindahkan repo ke path
> tanpa spasi.

## Kontribusi

Lihat [`CONTRIBUTING.md`](CONTRIBUTING.md). Progres & riwayat kerja ada di
[`docs/checkpoint.md`](docs/checkpoint.md).

## Atribusi & hak cipta

Logika perilaku game diacu dari repo akademik
[nicklesimba/FPGA-Mario](https://github.com/nicklesimba/FPGA-Mario)
(Nikhil Simha, Pranith Bottu). Karakter dan sprite adalah milik Nintendo;
penggunaan murni untuk keperluan akademik/non-komersial.
