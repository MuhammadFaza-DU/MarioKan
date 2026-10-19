# AGENTS.md — Aturan Project (VHDL / Basys3 / Vivado)

Dokumen ini **aturan tambahan** untuk project ini. `AGENTS.md` global
(`~/.config/opencode/AGENTS.md`) tetap berlaku penuh dan **berkedudukan lebih
tinggi**. Jika ada konflik: global menang, lalu aturan di file ini.

Root project: `D:\Progamming\Project dan SourceCode\VHDL\Project-Terakhir-SDL`

---

## 1. Batas Wilayah Kerja (WAJIB — instruksi eksplisit user)

- **DILARANG** membuat, mengubah, memindahkan, menghapus, atau meng-*generate*
  file/folder **di luar root project ini**.
- Yang termasuk "di luar": menulis ke `C:\Users\...`, menginstall tool/package
  global, mengubah config global OpenCode, mengubah env var / registry,
  menjalankan git di repo lain, mengubah file di folder kuliah lain.
- **Pengecualian** hanya bila (a) memang dibutuhkan untuk menyelesaikan task,
  DAN (b) user memberi izin eksplisit **lebih dulu**. Format permintaan izin:
  sebutkan aksi + path persis + alasan + dampak, lalu tunggu jawaban "ya".
- **Membaca** (read-only) di luar project **diizinkan** untuk diagnosa
  (mis. cek apakah Vivado/Python terpasang, baca dokumentasi resmi), selama
  tidak mengubah apa pun.
- File sementara / scratch → hanya di `./.tmp/` di dalam project (gitignored)
  atau temp dir yang sudah disetujui harness. Jangan taruh artefak build di luar.
- Install tool apa pun (Vivado, GHDL, package Python) = butuh izin user dulu.

## 2. Sumber Referensi

- Repo sumber (read-only): https://github.com/nicklesimba/FPGA-Mario
  Diakses via HTTP/raw (jangan clone ke luar project).
- Bila perlu salinan lokal untuk dibaca: hanya di `./reference/` dan
  **wajib** masuk `.gitignore`.
- Jangan pernah mengarang isi file repo. Tidak bisa diakses → tanya user.

## 3. Aturan Teknis Project

- RTL: **VHDL** (VHDL-2008 diizinkan, set di properti file). Constraint: **XDC**.
- Python/Tcl hanya untuk tooling (konversi sprite, build script) — **bukan**
  logika hardware.
- Komentar kode: Bahasa Indonesia (singkat). Identifier: English.
- Hanya `ieee.numeric_std`. Dilarang `std_logic_arith`, `std_logic_unsigned`,
  `std_logic_signed`.
- Tanpa derived clock di fabric (pakai clock-enable), tanpa latch, BRAM read
  sinkron, semua input asinkron lewat sinkronisasi 2-FF.
- Tanpa `real` / floating point di logika sintesis (pakai fixed-point).
- Target: Basys3 `XC7A35T-1CPG236C`. Jangan melampaui resource/kemampuan board.

## 4. Kejujuran Status (tidak bisa dinegosiasi)

- Bedakan tegas tiga tingkat bukti: **tersimulasi** / **tersintesis (WNS, utilisasi)**
  / **teruji di board**.
- Belum dites = katakan "belum dites" + cara mengetesnya. Jangan mengarang hasil.
- Jangan klaim "pasti jalan di hardware" tanpa bitstream + timing + uji board.

## 5. Artefak & Git

- `.gitignore` wajib memuat: `build/`, `*.bit`, `*.dcp`, `*.rpt`, `.Xil/`,
  `.tmp/`, `reference/`, `strix_runs/`, `*.log`.
- Jangan `git init` / commit / push / tag tanpa izin user.
- Bitstream final boleh disimpan (kecil) bila user mau; tanyakan dulu.
- Log Vivado (`vivado*.log`) muncul di cwd → jalankan build dari `.tmp/build/`,
  jangan dari root repo.

### 5.0 Checkpoint setiap pekerjaan besar (WAJIB ditawarkan)

Setiap kali menyelesaikan pekerjaan besar (fase selesai, fitur jadi, dokumen
besar selesai, bug besar teratasi), **selalu tawarkan** tiga langkah ini —
jangan menunggu diminta:

```powershell
git add -A
git commit -m "<pesan jelas>"
git tag -a stable-YYYY-MM-DD-vN -m "<ringkasan titik stabil>"
git push
git push origin stable-YYYY-MM-DD-vN
```

- Ambil tanggal: `Get-Date -Format "yyyy-MM-dd"`.
- Nomor `N`: hitung dari tag yang sudah ada hari itu
  (`git tag -l "stable-<tanggal>-v*"`), mulai dari `v1`.
- Format tawaran ke user: sebutkan **apa yang akan di-commit**, **nama tag**,
  lalu tunggu izin. Jangan commit/tag/push diam-diam.
- Kalau working tree sudah bersih (tidak ada perubahan baru), tetap tawarkan
  tag-nya — tag boleh menunjuk commit yang sudah ada.
- Setelah dieksekusi, verifikasi: `git tag -l` dan `git ls-remote --tags origin`.
- Riwayat checkpoint juga dicatat di `docs/checkpoint.md`.

## 5.1 Struktur dokumen (wajib rapi)

Semua dokumen masuk `docs/`, tidak ada file dokumen berserakan di root.

```
docs/
  PRD.md            -- spesifikasi operasional (sumber kebenaran requirement)
  checkpoint.md     -- progres & riwayat kerja (satu-satunya sumber progres)
  PORTING_NOTES.md  -- pemetaan modul lama -> baru, keputusan, batasan
  diagram/          -- diagram hasil generate
```

Dokumen **lokal saja** (di-`.gitignore`, TIDAK pernah di-commit karena repo
ini publik): `docs/brief/`, `docs/rubrik.md`, `docs/proposal/`.

Aturan:
- Dokumen baru dari luar (PDF/screenshot/tugas) → simpan di `docs/brief/`
  dengan nama deskriptif huruf kecil (`proyek-1.pdf`). Tetap lokal.
- Jangan menaruh dokumen di root kecuali `README.md`, `AGENTS.md`,
  `CONTRIBUTING.md`.
- Dokumen yang isinya penting tetapi sulit dicari (PDF/scan) → buat
  transkripsi terstruktur sebagai `.md` di `docs/` (juga lokal).
- Setiap dokumen baru yang **di-commit** wajib dirujuk dari `README.md` atau
  `docs/PRD.md`.
- **Jangan pernah** meng-commit dokumen akademik (rubrik, brief dosen,
  proposal) ke repo ini.

## 6. Sumber Kebenaran Requirement

- `docs/brief/ide-awal.md` = brief awal (referensi teknis, **bukan** requirement). Lokal.
- `docs/brief/proyek-1.pdf` = ketentuan tugas dari dosen. Lokal.
- `docs/rubrik.md` = transkripsi rubrik + ketentuan proposal. Lokal.
- `docs/PRD.md` = spesifikasi operasional setelah disetujui user. Bila PRD dan
  brief berbeda, **PRD menang**, tetapi perbedaan itu harus tercatat di
  bagian "Deviasi dari brief" pada PRD.
- Requirement baru dari dosen/user → update PRD dulu, baru kode.

## 7. Pelaporan

- Di akhir setiap sesi kerja: sebutkan skill yang dipakai, keputusan kunci,
  apa yang terverifikasi, dan apa yang belum.
