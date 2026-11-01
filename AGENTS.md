# AGENTS.md — Aturan Project (MarioKan · VHDL / Basys 3 / Vivado)

> **Delta di atas aturan global.** `~/.config/opencode/AGENTS.md` tetap berlaku
> penuh dan berkedudukan **lebih tinggi** dari file ini. Bila ada konflik:
> **instruksi user > aturan global > file ini > skill**.
>
> Root project: `D:\Progamming\Project-SourceCode\VHDL\Project-Terakhir-SDL`

---

## 1. Prinsip kerja (selalu aktif)

Prinsip umum sudah diatur global (§1). Bagian ini menegaskan yang **paling
kritis untuk project ini** — jangan dilewati.

- **Kejujuran status 3 tingkat bukti.** Setiap klaim wajib berlabel:
  **`SIM`** (lulus simulasi, sebut testbench) / **`SYN`** (lulus sintesis +
  timing, lampirkan WNS/WHS) / **`BOARD`** (terbukti di papan fisik, sebut yang
  terlihat). Belum dites → tulis **"belum dites"** + cara mengetesnya.
  **Dilarang** menulis "sudah jalan" tanpa label.
- **Jangan klaim "pasti jalan di hardware"** tanpa bitstream + WNS/WHS + uji board.
- **Verifikasi sebelum menyimpulkan.** Keputusan penting (timing layak/tidak,
  modul benar/tidak) butuh **≥2 bukti saling mendukung** dari sumber berbeda
  (mis. laporan Vivado + simulasi). Satu bukti = indikasi sementara.
- **Jangan mengarang isi repo/PDF/dokumen** yang tidak terbaca → tanya user.
- **Berpikir kritis & cek dampak sebelum mengubah.** Jangan merusak RTL/timing
  yang sudah lulus. Perubahan luas tanpa memahami struktur dulu = dilarang.
- **Cek state dulu** (baca file/config yang ada) sebelum menambah/menghapus.
- **Skala proses ke ukuran task.** Typo/label → langsung. Bug → isolasi &
  reproduksi dulu. Fitur besar → rencana dulu. Jangan over/under-engineer.
- **Izin untuk aksi berisiko:** commit/push/tag, hapus, flash board, install
  tool → konfirmasi user lebih dulu.
- **Selesaikan sampai lulus.** Build/simulasi gagal → tampilkan error asli,
  cari akar, perbaiki, ulangi. Kalau tetap gagal → laporkan "masih gagal di X".
- **Perbarui `CHECKPOINTS.md`** setiap perubahan bermakna (§8).

## 2. Otoritas & perubahan keputusan

- Urutan kekuatan: **instruksi user > aturan global > file ini > skill**.
- Keputusan bertanda **final** (§3) hanya boleh berubah lewat **konfirmasi
  eksplisit user** — bukan inisiatif agent.
- Jangan menanyakan ulang keputusan yang sudah final (§3).
- Bila instruksi user bertentangan dengan aturan global: ikuti user, **lalu
  laporkan konfliknya**. Jangan diam-diam memilih salah satu.

## 3. Keputusan project (final)

| Topik | Keputusan |
|---|---|
| Target board | Basys 3, Artix-7 `XC7A35T-1CPG236C`; VGA 4-4-4 (12-bit); tanpa codec audio & tanpa SDRAM |
| Bahasa / constraint | VHDL-2008 (per file) + XDC; hanya `ieee.numeric_std` |
| Video | 1920×1080@60; clock pixel **148,4375 MHz** (MMCM `11.875/1/8`); grid logika **384×216** ×5 integer |
| Arsitektur | Tanpa framebuffer (racing-the-beam), tanpa soft CPU, tanpa derived clock (pakai CE), BRAM read sinkron |
| Fixed-point | Posisi **Q13.8** (21-bit, ±4095,996 px); kecepatan **Q8.8** |
| Palet | **4 bank × 16 × 12-bit**, 2-bit bank-select per sprite (D-7) |
| Input | Keyboard PS/2 **wajib**; mouse = fitur opsional `4b` (D-9); fallback `sw[15:12]` + `btnU` (D-8) |
| Audio | **Ditunda** ke pengembangan lanjutan (D-1) |
| Respawn | Tilemap **tidak** reset; score/coins tetap; time/posisi/enemy reset; nyawa −1 (awal 3) |
| Peran kontributor | Hanya `docs/` + `sim/`; **tidak** menyentuh `src/` / `constraints/` (D-5) |
| Pelacakan progres | `CHECKPOINTS.md`, bukan knowledge graph (D-4) |

Alasan & detail tiap deviasi: `docs/PRD.md` §6. **Jangan ubah tabel ini tanpa
konfirmasi user.**

## 4. Batas lingkup & isolasi (WAJIB — instruksi eksplisit user)

- **DILARANG** membuat, mengubah, memindahkan, menghapus, atau meng-*generate*
  file/folder **di luar root project ini**.
- Termasuk "di luar": menulis ke `C:\Users\...`, install tool/package global,
  mengubah config global OpenCode, mengubah env var/registry, menjalankan git
  di repo lain, mengubah file di folder kuliah lain.
- **Pengecualian** hanya bila (a) memang dibutuhkan untuk menyelesaikan task
  DAN (b) user memberi izin eksplisit **lebih dulu**. Format permintaan izin:
  sebutkan aksi + path persis + alasan + dampak, lalu tunggu jawaban "ya".
- **Membaca** (read-only) di luar project **diizinkan** untuk diagnosa
  (mis. cek Vivado/Python terpasang, baca dokumentasi resmi), selama tidak
  mengubah apa pun.
- File sementara / scratch → hanya di `./.tmp/` di dalam project (gitignored)
  atau temp dir harness yang sudah disetujui. Jangan taruh artefak build di luar.
- Install tool apa pun (Vivado, GHDL, package Python) = butuh izin user dulu.
- Jangan menyalin/menimpa file dari project lain.
- **Sumber referensi eksternal (read-only):** repo `nicklesimba/FPGA-Mario`
  diakses via HTTP/raw (jangan clone ke luar project). Salinan lokal untuk
  dibaca hanya di `./reference/` dan **wajib** masuk `.gitignore`. Tidak bisa
  diakses → tanya user, jangan mengarang.

## 5. Konvensi teknis

- **Stack:** VHDL-2008 + XDC; toolchain Vivado **2026.1**; Python 3.12/Pillow
  hanya untuk tooling (konversi sprite); Tcl untuk build script — **bukan**
  logika hardware.
- **Penamaan:** identifier English, komentar kode Indonesia (singkat).
- **Struktur:** `src/` (top `top_basys3` + modul), `constraints/basys3.xdc`,
  `sim/tb_*.vhd`, `tools/`, `docs/`, `build/` (gitignored).
- **RTL:** tanpa latch; tanpa derived clock (pakai CE); semua input asinkron
  lewat sinkronisasi 2-FF; tanpa `real`/floating point di sintesis; BRAM read
  sinkron; tanpa pembagian/modulo non-pangkat-2 di jalur piksel; register
  `hsync`/`vsync`/`de`/RGB bersamaan; `inout` hanya di top (PS/2 open-drain).
- **Dokumen:** semua di `docs/`; root hanya `README.md`, `AGENTS.md`,
  `CONTRIBUTING.md`, `CHECKPOINTS.md`. Dokumen akademik (`docs/brief/`,
  `docs/rubrik.md`, `docs/proposal/`, `tools/make_proposal.py`) **lokal-only**,
  **jangan pernah** di-commit (repo publik).
- **Artefak & `.gitignore`** wajib memuat: `build/`, `*.bit`, `*.dcp`, `*.rpt`,
  `.Xil/`, `.tmp/`, `reference/`, `strix_runs/`, `*.log` (+ dokumen akademik).
  Bitstream final boleh disimpan (kecil) bila user mau — tanyakan dulu.
- **Commit:** Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`,
  `refactor:`). **Tag:** `stable-YYYY-MM-DD-vN`.
- **Perintah verifikasi:** build Vivado (`tools/build.tcl`) → cek WNS ≥ 0,
  WHS ≥ 0, 0 latch, 0 critical warning, 0 DRC, utilisasi di bawah batas;
  simulasi `sim/tb_*.vhd`; `python -m py_compile <file>` untuk tooling Python.

## 6. Baca context dulu (urutan wajib)

1. `CHECKPOINTS.md` — posisi kerja terkini (selalu pertama).
2. `docs/PRD.md` — sumber kebenaran requirement.
3. `README.md` — ringkas arsitektur & status bukti.
4. `docs/PORTING_NOTES.md` (bila ada) / `docs/diagram/arsitektur.svg`.
5. `docs/brief/ide-awal.md` + `docs/rubrik.md` (lokal, referensi — **bukan** requirement).

**Sumber kebenaran requirement:** `docs/PRD.md` menang atas brief; perbedaan
wajib tercatat di PRD §6. Requirement baru dari dosen/user → update PRD dulu,
baru kode.

## 7. Definition of Done

Gerbang sebelum boleh bilang "selesai" (mengacu PRD §1 SC-1…SC-8 & §4.9):

- [ ] Build Vivado: synth/impl sukses; **WNS ≥ 0**, **WHS ≥ 0** di clock pixel;
      **0 latch**, 0 critical warning, 0 DRC error.
- [ ] Semua port top punya `PACKAGE_PIN` + `IOSTANDARD` (0 `NSTD-1`/`UCIO-1`).
- [ ] Utilisasi di bawah kapasitas: LUT ≤ 20.800, FF ≤ 41.600, BRAM ≤ 50, DSP ≤ 90.
- [ ] Testbench relevan (`SIM`) lulus untuk perilaku baru.
- [ ] Klaim menyebut label `SIM`/`SYN`/`BOARD`; belum dites ditulis "belum dites"
      + cara mengetesnya.
- [ ] Ringkasan tertulis: apa berubah, apa **belum** terverifikasi, risikonya.
- [ ] `CHECKPOINTS.md` diperbarui; tawarkan checkpoint bila di titik stabil.

**Pelaporan akhir sesi:** sebutkan skill yang dipakai, keputusan kunci, apa yang
terverifikasi, dan apa yang belum.

## 8. Checkpoint & state

- Checkpoint di **setiap titik stabil** (fase selesai, fitur jadi, bug besar
  teratasi). Catat di `CHECKPOINTS.md`; bila git → commit + tag
  `stable-YYYY-MM-DD-vN`.
- **Selalu tawarkan**, jangan diam-diam: sebutkan apa yang akan di-commit +
  nama tag, lalu tunggu izin.
- **Hanya sesi utama (PM/controller) yang menulis `CHECKPOINTS.md`.** Subagent
  dilarang mengeditnya langsung — lapor satu baris, sesi utama yang menggabungkan.
- Log hanya perubahan **bermakna** (perubahan perilaku/fitur, bug fix, file
  penting dibuat/dihapus, keputusan diambil/diubah). Bukan whitespace, typo
  komentar, atau eksperimen yang dibuang sebelum commit.
- **Jangan** commit/push tanpa izin eksplisit user.
- Prosedur (setelah izin):

```powershell
git add -A
git commit -m "<pesan jelas>"
git tag -a stable-YYYY-MM-DD-vN -m "<ringkasan titik stabil>"
git push
git push origin stable-YYYY-MM-DD-vN
```

- Tanggal: `Get-Date -Format "yyyy-MM-dd"`; nomor `N` dihitung dari tag hari itu
  (`git tag -l "stable-<tanggal>-v*"`). Verifikasi: `git tag -l` dan
  `git ls-remote --tags origin`.
- Log Vivado (`vivado*.log`) muncul di cwd → jalankan build dari `.tmp/build/`,
  jangan dari root repo.