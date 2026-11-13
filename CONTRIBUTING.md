# Panduan Kontribusi — MarioKan

## Pembagian peran (disepakati)

| Peran | Boleh mengubah |
|---|---|
| **Pemilik RTL** (Muhammad Faza) | semua: `src/`, `constraints/`, `sim/`, `tools/`, `docs/` |
| **Kontributor** (teman) | `docs/`, `sim/` (testbench), laporan uji papan. **Tidak** mengubah `src/` atau `constraints/` |

Alasan pembatasan ini: requirement mengikuti PRD; rincian antarmuka yang masih
usulan harus dikunci sebelum RTL terkait. Perubahan RTL dari banyak orang
tanpa kontrak yang ketat berisiko konflik dan regresi timing.

Kalau kamu ingin mengusulkan perubahan RTL: buka **issue** dengan usulan +
alasan, jangan langsung PR.

## Alur kerja

1. `git switch -c docs/<topik>` atau `test/<topik>` (jangan bekerja di `main`).
2. Commit kecil dengan pesan jelas: `docs: tambah prosedur uji VGA`.
3. Buka Pull Request ke `main`. Sertakan: apa yang diubah, kenapa, dan bukti.
4. Pemilik repo me-review. Merge hanya setelah CI/cek manual lolos.

> **Status penegakan:** repo sudah **publik**, dikonfirmasi ulang lewat API
> GitHub pada 2026-11-12 (`private:false`, `visibility:public`). HTTP 403 yang
> pernah dicatat berasal dari saat repo masih private; jangan dianggap status
> sekarang. Branch protection/ruleset/CODEOWNERS aktif **belum diverifikasi**.
> Sampai ada bukti pengaturan aktual, alur review dan larangan push langsung
> merupakan konvensi kerja, bukan jaminan pembatasan teknis.

## Peran collaborator

| Akses | Hak |
|---|---|
| `push` | Commit, buat branch, buka Pull Request |
| `admin` | Ubah setting, hapus repo — **hanya pemilik** |

Undang collaborator (dijalankan pemilik):

```powershell
gh api --method PUT repos/MuhammadFaza-DU/MarioKan/collaborators/<USERNAME> -f permission=push
```

## Aturan bukti (tidak bisa dinegosiasi)

Setiap klaim harus menyebut tingkat buktinya:

- `SIM` — sudah dijalankan di simulasi (sebutkan testbench-nya)
- `SYN` — sudah lewat sintesis + timing (lampirkan WNS/WHS)
- `BOARD` — sudah dilihat di papan fisik (sebutkan apa yang terlihat)

**Dilarang** menulis "sudah jalan" tanpa salah satu label di atas.
Kalau belum dites: tulis "belum dites" + cara mengetesnya.

## Konvensi dokumen

- README utama: Inggris untuk pembaca publik; catatan kerja: Indonesia,
  istilah teknis tetap Inggris. Catatan English yang sudah ada dipertahankan.
- Komentar kode: Indonesia singkat. Identifier: English.
- Tabel status memakai label `SIM` / `SYN` / `BOARD`.

## Yang tidak boleh di-commit

- Artefak build (`build/`, `*.bit`, `*.dcp`, `*.rpt`, `.Xil/`)
- Salinan repo sumber di `reference/`
- Dokumen akademik di `docs/brief/`, `docs/proposal/`, `docs/rubrik.md` dan generator akademik lokal
- Diagnostik sementara di `.tmp/` serta kandidat diagram yang ditolak/diabaikan pada `.gitignore`
- Data pribadi / kredensial

Sudah diatur di `.gitignore`. Kalau kamu menemukan file yang lolos, laporkan.

Checkpoint memakai daftar file publik eksplisit dan pemeriksaan index, bukan
`git add -A` tanpa audit. Commit/tag tidak otomatis memberi izin push.
Jalankan `python -B tools/check_project_notes.py` sebelum checkpoint untuk
memeriksa catatan aktif dan batas lokal-only. Status kerja hanya di
`CHECKPOINTS.md`; laporan lama dibaca sebagai riwayat, bukan status terkini.
