# Catatan Serah-Terima — Rencana Rename Folder Induk

**Tanggal:** 2026-10-22
**Status:** **SELESAI DIEKSEKUSI 2026-10-22.** Folder sudah bernama `Project-SourceCode`.
**Tujuan:** `D:\Progamming\Project dan SourceCode` → `D:\Progamming\Project-SourceCode`

> **Hasil eksekusi (2026-10-22):** rename berhasil, isi identik (236.764 file /
> 12.642.011.776 byte, delta 0). 32 file referensi diperbaiki (54 kemunculan):
> 21 fungsional + 11 dokumentasi. File bukti historis & cache sengaja TIDAK
> diubah (lihat 3.3). Penyebab kegagalan sesi sebelumnya terkonfirmasi: handle
> terbuka pada rantai folder (root, `VHDL`, `Project-Terakhir-SDL`) yang hilang
> setelah proses pemegangnya berhenti.

> Dokumen ini ditulis oleh sesi yang **menghentikan** pekerjaan sebelum eksekusi,
> atas permintaan pemilik. Isinya: fakta yang sudah diverifikasi, jebakan yang
> sudah ditemukan, dan apa yang **tidak** boleh diulang. Semua klaim di bawah
> berasal dari pengujian nyata, bukan asumsi.

---

## 1. Alasan rename

Path mengandung **spasi** (`Project dan SourceCode`). Vivado memecah argumen Tcl
di spasi sehingga muncul:

```
ERROR: [Common 17-69] Command failed: File 'D:/Progamming/Project' is a directory
```

Workaround `[list $path]` sudah dipakai di `tools/build.tcl` dan **terbukti
berfungsi**, tetapi rapuh untuk kontributor yang menulis script baru.

---

## 2. PENGHALANG UTAMA (harus diselesaikan lebih dulu)

### Kunci cwd — ini yang menggagalkan semua percobaan

```
WindowsTerminal PID 9028   cwd = D:\...\Project-Terakhir-SDL
  └─ powershell PID 12656  (cwd sama)
      └─ opencode PID 23772 (session)
```

Windows mengunci **seluruh rantai folder di atas** cwd sebuah proses. Selama
terminal itu terbuka, rename folder induk **mustahil** — bukan masalah izin.

**Bukti pengujian (semua sudah dicoba):**

| Uji | Hasil |
|---|---|
| Rename folder baru di `D:\Progamming` | BERHASIL |
| Rename `MATLAB` (tidak dipakai proses) | BERHASIL |
| Rename file di dalam project | BERHASIL |
| Rename `VHDL` (di rantai cwd session) | **GAGAL** "Access denied" |
| Rename folder project | **GAGAL** "being used by another process" |
| `session_move` ke `D:\Progamming` | tetap gagal (shell terminal masih memegang) |
| `Start-Process` detached + tunggu | tetap gagal selama terminal terbuka |

**Kesimpulan:** tidak ada trik dari dalam session. Yang harus terjadi:
**tutup jendela terminal** yang cwd-nya di folder itu. Setelah itu rename bisa
dilakukan langsung — tidak perlu script penunggu.

**Jangan buang waktu** mencoba: `session_move`, `Start-Process -WindowStyle
Hidden`, `robocopy /MOVE`, TakeOwnership, atau `handle.exe` (tidak terpasang).
Semuanya sudah dipertimbangkan/diuji.

---

## 3. Peta dampak — 72 referensi di seluruh pohon

### 3.1 WAJIB diperbaiki (fungsional, rusak diam-diam bila dilewat)

| File | Isi |
|---|---|
| `Aplikasi\Tazk\graphify-out\.graphify_root` | path root graphify |
| `Lomba\HoloDev 9.0\graphify-out\.graphify_root` | idem |
| `MATLAB\Workshop-MATLAB-Agentic\graphify-out\.graphify_root` | idem |
| `WEBB\gamein\graphify-out\.graphify_root` | idem |
| `WEBB\muhammad-faza-portfolio\graphify-out\.graphify_root` | idem |
| `WEBB\StackCrate\graphify-out\.graphify_root` | idem |
| `Tes model\simulink-fundamentals\winshot.ps1` | `$Out = "D:\...\matlab.png"` |
| `Tes model\simulink-fundamentals\view.ps1` | `$Shot = "D:\...\real.png"` |
| `Tes model\simulink-fundamentals\scroll.ps1` | idem |
| `Tes model\simulink-fundamentals\keynav.ps1` | idem |
| `Tes model\simulink-fundamentals\drag.ps1` | idem |
| `Tes model\simulink-fundamentals\uia.ps1` | default `$Out` |
| `Tes model\simulink-fundamentals\t_add_enabled_triggered.m` | `logfile = 'D:\...'` |
| `BEBAS CAMPURAN\Game Action Koki\measure_boss.py` | 5 path absolut |
| `BEBAS CAMPURAN\Game Action Koki\measure_bg.py` | 11 path absolut |
| `Tes model\ds\oc\verification\ui-responsive-test.js` | path screenshot |
| `WEBB\Web-Subtitle-Otomatis\.git\config` | **URL submodule absolut** (2 baris) |
| `AGENTS.md` (root induk) | judul + definisi root |
| `Tes model\seb-modif\AGENTS.md` | 5 rujukan ke root |
| `VHDL\Project-Terakhir-SDL\AGENTS.md` | baris "Root project:" |

### 3.2 Dokumentasi (kosmetik, tapi menyesatkan bila dibiarkan)

`MATLAB\Tes 1\PETUNJUK.md` · `Tes model\simulink-fundamentals\CARAPAKAI.md` ·
`Tes model\seb-modif\README.md` ·
`Lomba\HoloDev 9.0\docs\superpowers\plans\2026-09-05-auralyze-landing-redesign.md` ·
`WEBB\StackCrate\docs\superpowers\plans\` (3 file) ·
`WEBB\gamein\docs\superpowers\plans\2026-10-17-preflight-data-foundation.md` ·
`Tes model\ds\gpt 6.1 sol\PROMPT_USED.md` · `BENCHMARK.md`

### 3.3 JANGAN DIUBAH — bukti historis & cache

| File | Alasan |
|---|---|
| `WEBB\gamein\research\reports\phase-0-verification-evidence.json` | merekam command yang **benar-benar dijalankan** pada tanggal itu. Mengubahnya = memalsukan bukti |
| `WEBB\gamein\research\reports\phase-0-data-report.md` | laporan historis |
| `Tes model\ds\sekai\verify\detect-round1.json` | hasil verifikasi |
| `*\\.impeccable\hook.cache.json` | cache, akan regenerate sendiri |
| `WEBB\muhammad-faza-portfolio\graphify-out\graph.html` | file generated |

### 3.4 AMAN — tidak perlu disentuh

- **48 file** `*.csproj` + `*.sln` di `Tes model\seb-modif\` → **terverifikasi
  memakai path relatif**, tidak terpengaruh.
- `pyvenv.cfg` → **tidak ada satu pun** venv di pohon ini.
- `*.xpr` → tidak ada project Vivado berbasis file.
- `node_modules`, `build`, `dist`, `.dart_tool`, dll → regenerable.

---

## 4. Prosedur yang disarankan

1. **Tutup semua terminal/session** yang cwd-nya di dalam folder itu (cek:
   `Get-CimInstance Win32_Process | ? { $_.CommandLine -like "*Project dan SourceCode*" }`).
2. Rename:
   ```powershell
   Rename-Item -LiteralPath "D:\Progamming\Project dan SourceCode" -NewName "Project-SourceCode"
   ```
3. Verifikasi:
   ```powershell
   Test-Path "D:\Progamming\Project-SourceCode"      # harus True
   Test-Path "D:\Progamming\Project dan SourceCode"  # harus False
   ```
4. Perbaiki file di §3.1 dan §3.2 (ganti string `Project dan SourceCode` →
   `Project-SourceCode`). **Lewati** §3.3.
5. Verifikasi akhir — scan ulang seluruh pohon, harus **0** sisa:
   ```powershell
   Get-ChildItem "D:\Progamming\Project-SourceCode" -Recurse -File -Force |
     Where-Object { $_.Length -lt 2MB -and $_.Extension -match '^\.(md|ps1|py|m|js|json|tcl|yml|txt|csproj|sln|vhd|xdc)$' } |
     Select-String -Pattern 'Project dan SourceCode' -SimpleMatch
   ```
6. Cek git repo MarioKan masih sehat:
   ```powershell
   git -C "D:\Progamming\Project-SourceCode\VHDL\Project-Terakhir-SDL" status --short
   ```

---

## 5. Jebakan teknis yang sudah ditemukan (jangan diulang)

1. **Regex skip-dir berakhir backslash tunggal** → PowerShell melempar
   `Illegal \ at end of pattern` untuk setiap file dan scan jadi sangat lambat.
   Perbaikan: tutup dengan `(\\|$)`.
2. **Karakter non-ASCII (em-dash) di script .ps1** bisa ter-*double-encode*
   menjadi mojibake (`C3 A2 E2 82 AC`) dan merusak parsing. Pakai ASCII murni.
3. **`Get-ChildItem -Recurse` atas 236.757 file** butuh waktu lama; batasi
   dengan filter ekstensi sebelum membaca isi file.
4. **File bisa biner meski berekstensi teks** → cek byte NUL sebelum decode.
5. **UTF-16** (`pyvenv.cfg`, sebagian `.ini`) tidak terbaca sebagai UTF-8 —
   deteksi BOM dan lewati.
6. **`reset --hard` dari `git filter-branch`** menghapus file tracked di disk.
   (Relevan untuk operasi git, bukan rename ini.)
7. **Backup dulu, baru edit.** Tanpa backup, kesalahan replace tidak bisa
   dibatalkan.

---

## 6. Status akhir sesi ini

| Item | Kondisi |
|---|---|
| Perubahan filesystem | **NOL** |
| Nama folder | `Project dan SourceCode` (tidak berubah) |
| Jumlah file | **236.757** (identik dengan sebelum mulai) |
| Script yang dibuat | sudah **dihapus** (2 file + 2 log di `%TEMP%`) |
| Proses tersisa | **tidak ada** |
| Repo MarioKan | tidak tersentuh |
