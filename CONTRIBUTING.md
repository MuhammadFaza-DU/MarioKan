# Panduan Kontribusi — MarioKan

## Pembagian peran (disepakati)

| Peran | Boleh mengubah |
|---|---|
| **Pemilik RTL** (Muhammad Faza) | semua: `src/`, `constraints/`, `sim/`, `tools/`, `docs/` |
| **Kontributor** (teman) | `docs/`, `sim/` (testbench), laporan uji papan. **Tidak** mengubah `src/` atau `constraints/` |

Alasan pembatasan ini: interface antar-modul RTL dikunci oleh PRD. Perubahan
RTL dari banyak orang tanpa kontrak interface yang ketat = konflik dan regresi
timing yang sulit dilacak.

Kalau kamu ingin mengusulkan perubahan RTL: buka **issue** dengan usulan +
alasan, jangan langsung PR.

## Alur kerja

1. `git switch -c docs/<topik>` atau `test/<topik>` (jangan bekerja di `main`).
2. Commit kecil dengan pesan jelas: `docs: tambah prosedur uji VGA`.
3. Buka Pull Request ke `main`. Sertakan: apa yang diubah, kenapa, dan bukti.
4. Pemilik repo me-review. Merge hanya setelah CI/cek manual lolos.

> **Catatan jujur soal penegakan aturan:** repo ini **private** pada akun GitHub
> Free, sehingga **branch protection dan rulesets tidak dapat diaktifkan**
> (GitHub mengembalikan HTTP 403). Artinya aturan "jangan push langsung ke
> `main`" di atas adalah **konvensi, bukan paksaan teknis**. Semua collaborator
> secara teknis masih bisa push langsung ke `main`.
>
> Mohon dipatuhi secara sukarela. Bila ingin dipaksakan, pilihannya: (a) upgrade
> akun ke GitHub Pro, atau (b) jadikan repo publik setelah tugas selesai.
> Pemilik repo akan memeriksa riwayat `main` bila terjadi masalah.

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

- Bahasa: Indonesia, istilah teknis tetap Inggris.
- Komentar kode: Indonesia singkat. Identifier: English.
- Tabel status memakai label `SIM` / `SYN` / `BOARD`.

## Yang tidak boleh di-commit

- Artefak build (`build/`, `*.bit`, `*.dcp`, `*.rpt`, `.Xil/`)
- Salinan repo sumber di `reference/`
- Data pribadi / kredensial

Sudah diatur di `.gitignore`. Kalau kamu menemukan file yang lolos, laporkan.
