# Lessons

## L-001: Singkatan kendali tidak dijelaskan dan persetujuan diminta terlalu dini

- **Salah:** Agent mengusulkan kontrol menggunakan singkatan U/D/L/R/C tanpa terlebih dahulu menjelaskan tombol fisik Basys 3, perbedaannya dari tombol keyboard, dan statusnya sebagai usulan. Agent lalu meminta persetujuan target final ketika pemilik masih membutuhkan penjelasan.
- **Bukti:** Pada diskusi P2 tanggal 2026-11-12, pemilik menanyakan arti L/R dan C, apakah kendali tersebut milik keyboard atau papan FPGA, serta menolak permintaan persetujuan final karena belum memahami rancangan.
- **Dampak:** Penjelasan membingungkan, diskusi berulang tanpa keputusan yang benar-benar dipahami, dan persetujuan berisiko disalahartikan sebagai persetujuan atas rincian yang belum jelas.
- **Aturan baru:** Jelaskan nama fisik, letak relatif, dan identifier setiap tombol sebelum memakai singkatan. Selalu pisahkan kolom kendali papan FPGA dari kolom keyboard. Bedakan fakta perangkat, fungsi desain yang sedang termuat, usulan pemetaan, pemahaman pemilik, persetujuan desain, dan izin pemrograman perangkat. Bahas satu konsep yang belum dipahami terlebih dahulu; jangan meminta persetujuan keseluruhan sebelum pertanyaan pemilik terjawab. Persetujuan pemeriksaan atau diagnostik tidak berarti persetujuan pemetaan atau dokumen final.
- **Verifikasi:** Penjelasan korektif menggunakan diagram posisi lima tombol dan tabel dua jalur kendali dengan nama lengkap, tersimpan di `docs/INPUT_GUIDE.md`. Konfirmasi awal hanya menyatakan penjelasan jelas. Kemudian, setelah contoh tekan/tahan dan tiga tombol bersamaan dijelaskan, pemilik memilih "Cocok, setuju skema ini": hanya pemetaan papan beserta perilaku yang dijelaskan menjadi disetujui; reset dan pemetaan keyboard tetap terpisah. Sebelum menyusun keluaran P2, periksa konsistensi nama kendali dan sumber konfirmasi setiap keputusan.

## L-002: API fetch biner pada Code Mode diasumsikan seperti browser standar

- **Salah:** Audit PNG mencoba memanggil `response.arrayBuffer()` melalui fetch Code Mode tanpa menguji dukungan metode itu terlebih dahulu, lalu menjalankannya pada satu batch aset.
- **Bukti:** Semua 30 hasil inspeksi awal mengembalikan `TypeError: z.arrayBuffer is not a function`; tidak ada dimensi gambar yang berhasil diperiksa melalui jalur tersebut.
- **Dampak:** Satu batch akses jaringan tidak menghasilkan pengukuran yang dibutuhkan. Nilai payload nol pada hasil gagal tidak boleh dipakai sebagai ukuran aset.
- **Aturan baru:** Uji satu respons biner sebelum fan-out. Jangan menganggap seluruh API browser tersedia pada runtime terkurung. Untuk audit lokal, gunakan jalur biner yang telah diuji dan pisahkan commit SHA dari tree SHA serta payload teoritis dari pemakaian hasil sintesis.
- **Verifikasi:** Audit pengganti memakai Python standar dan Pillow membaca seluruh 30 PNG pada commit sumber yang dipin, menyimpan dimensi/warna dan perhitungan di `.tmp/asset-audit.json`. Pembacaan 30/30 berhasil; payload teoritis 4-bit berjumlah 15.385 byte. Tidak diklaim sebagai konversi aset atau hasil SYN/BOARD.

## L-003: Discovery bercabang tanpa rencana kerja yang disepakati

- **Salah:** Pembahasan P2 berpindah antara kendali, mekanik game, konverter, diagnostik papan, dan kesiapan aset tanpa satu rencana kerja bertahap yang ditinjau pemilik.
- **Bukti:** Pada 2026-11-12 pemilik meminta pembuatan plan karena pembahasan sebelumnya dinilai tidak jelas dan bergerak ke berbagai topik.
- **Dampak:** Batas antara penulisan P2 dan pembangunan game/diagnostik menjadi sulit diikuti; sudah ada catatan riset tetapi belum ada dokumen P2.
- **Aturan baru:** Sepakati target, urutan tahap, keluaran, dan gerbangnya sebelum melanjutkan. Satu tahap satu fokus; parkir topik sampingan. Gunakan kembali bukti yang sudah ada dan nyatakan setiap perluasan scope. Persetujuan rencana kerja bukan persetujuan otomatis atas keputusan desain yang belum dibahas.
- **Verifikasi:** Rencana dibuat di `docs/proposal/proyek-2/RENCANA_KERJA.md`, memisahkan enam tahap kebutuhan, arsitektur, pemeriksaan pendukung, draf, DOCX, dan QA. Eksekusi lanjutan menunggu tinjauan pemilik; keberhasilan penerapan alur belum boleh diklaim sebelum dijalankan.

## L-004: Pemeriksaan dokumen terlalu literal dan kegagalannya tidak bernama

- **Salah:** Pemeriksaan rencana menggabungkan banyak kondisi dalam assert tanpa label, termasuk mensyaratkan frasa `bukan persetujuan` yang tidak diwajibkan. Dokumen sudah menjelaskan batas persetujuan menggunakan kalimat berbeda.
- **Bukti:** Pemeriksaan awal menghasilkan AssertionError tanpa nama kondisi. Pemeriksaan diagnostik menunjukkan seluruh kondisi lain lulus; satu kegagalan adalah pencarian frasa tersebut, sedangkan status dokumen berbunyi bahwa persetujuan rencana kerja tidak otomatis menyetujui pemetaan/reset/isi P2.
- **Dampak:** False alarm dan satu langkah diagnosis tambahan, bukan kekurangan isi rencana yang telah dibuktikan.
- **Aturan baru:** Setiap pemeriksaan harus memiliki nama dan melaporkan kondisi yang gagal. Pin pemeriksaan ke requirement atau pernyataan yang sengaja ditetapkan, bukan sinonim yang dipaksakan setelah dokumen ditulis. Jangan mengubah isi yang benar hanya untuk menyenangkan pemeriksaan yang keliru.
- **Verifikasi:** Checker `.tmp/p2-qa/check_work_plan.py` memeriksa pernyataan batas persetujuan yang benar dan melaporkan PASS/FAIL per kondisi; hasilnya harus diperiksa sebelum klaim rencana terverifikasi.
  Pada akhir P2, dua kondisi status awal menjadi usang setelah pemilik meminta eksekusi; checker diselaraskan ke penerimaan isi yang tetap menunggu review, bukan memaksa rencana kembali berstatus belum dikerjakan. Gate PDF awal juga gagal membaca WHS yang pindah baris; whitespace text-layer kini dinormalisasi sebelum pemeriksaan frasa. Kegagalan itu tidak dijadikan alasan mengubah isi dokumen yang benar.

## L-005: Ekstraksi gambar global menghasilkan gambar dari sesi yang tidak sesuai

- **Salah:** Helper ekstraksi gambar dipanggil dengan default database dan tanpa filter sesi. Berkas yang dihasilkan bukan foto Basys 3 yang baru dikirim pada percakapan ini.
- **Bukti:** Hasil dibuka dengan tool read dan terlihat berupa screenshot lama yang tidak cocok dengan foto papan. Hasil itu tidak dipakai sebagai bukti hardware atau sumber instruksi.
- **Dampak:** Satu berkas scratch yang tidak relevan dibuat di `.tmp/evidence/`; berkas yang baru dibuat tersebut kemudian dihapus dan ketidakberadaannya diverifikasi. Tidak ada file asli pengguna yang dihapus.
- **Aturan baru:** Jangan menganggap gambar terbaru pada database global sebagai lampiran sesi aktif. Verifikasi gambar hasil ekstraksi sebelum OCR, dokumentasi, atau pengambilan keputusan. Jika sesi/backend belum teridentifikasi, gunakan foto yang benar-benar terlihat pada pesan pengguna untuk analisis visual dan jangan mengklaim sudah mengarsipkannya ke file lokal. Jangan menyisir gambar sesi lain untuk mencoba-coba.
- **Verifikasi:** File ekstraksi yang salah telah dihapus. Pengamatan konektor memakai foto Basys 3 yang ada pada pesan pengguna, bukan hasil helper; belum ada salinan lokal foto yang benar yang diklaim tersimpan. Konfirmasi jalur adaptor/layar masih diminta terpisah.

## L-006: Pemeriksaan aksesori disalahpahami sebagai kebutuhan merakit rangkaian

- **Salah:** Pertanyaan tentang rangkaian yang terhubung ke header belum mendahulukan penegasan bahwa konektor hitam adalah bagian bawaan papan dan tidak ada kebutuhan merakit rangkaian tambahan untuk game inti.
- **Bukti:** Pemilik menunjuk port hitam lalu mempertanyakan mengapa harus membuat rangkaian tambahan dan apakah FPGA dapat dipakai langsung.
- **Dampak:** Pemeriksaan keamanan menambah kebingungan tentang kebutuhan perangkat proyek.
- **Aturan baru:** Saat membahas perangkat, bedakan konektor bawaan, periferal yang dicolokkan, dan rangkaian yang harus dirakit. Jelaskan tujuan pemeriksaan sebelum meminta pemilik mengidentifikasi aksesori. Jangan menyamakan keberadaan port kosong dengan keberadaan modul tambahan.
- **Verifikasi:** `docs/INPUT_GUIDE.md` bagian 5 menjelaskan bahwa game inti memakai fasilitas bawaan Basys 3; keyboard/monitor adalah periferal, dan pemeriksaan sambungan bukan keharusan menambah rangkaian. Penjelasan ini harus dibawa ke naskah P2 dan diperiksa saat review.

## L-007: Regenerasi diagram pada Windows menghasilkan CRLF

- **Salah:** Generator diagram dijalankan setelah koreksi label tanpa memastikan kontrak LF pada keluaran. Generator lama memakai open teks dengan newline default Windows.
- **Bukti:** Git memperingatkan CRLF pada SVG yang diregenerasi. Tes yang menjalankan generator sungguhan di scratch project gagal karena keluaran memuat CRLF, bertentangan dengan `.gitattributes`.
- **Dampak:** Artefak hasil regenerasi tidak mengikuti konvensi line ending meskipun XML-nya valid.
- **Aturan baru:** Generator teks menetapkan newline LF secara eksplisit. Uji berkas hasil generator, bukan hanya sintaks Python atau teks sumber; jangan menganggap normalisasi Git menggantikan keluaran yang benar.
- **Verifikasi:** Tes regresi `tools/tests/test_architecture_diagram.py` menunjukkan kegagalan sebelum perbaikan dan lulus setelah newline dibuat eksplisit. `python -B -m unittest discover -s tools/tests -v` lulus 1 tes; py_compile lulus; SVG diregenerasi, valid XML, dan tidak mengandung CRLF. Ini verifikasi tooling, bukan SIM/SYN/BOARD game.

## L-008: Patch besar memakai konteks yang tidak cocok dengan file

- **Salah:** Satu patch pencatatan kendali mengubah beberapa file sekaligus dan mencari teks `di usulkan`, padahal file panduan menulis `diusulkan`.
- **Bukti:** Tool patch menolak dengan `Failed to find expected lines` pada `docs/INPUT_GUIDE.md`. Pembacaan ulang menunjukkan PRD, AGENTS, dan panduan masih memuat keputusan lama; patch gagal tidak dihitung sebagai perubahan berhasil.
- **Dampak:** Pencatatan persetujuan kendali tertunda; tidak ada bukti perubahan parsial yang diteruskan sebagai hasil selesai.
- **Aturan baru:** Baca konteks persis sebelum patch, pecah perubahan lintas dokumen menjadi kelompok kecil, dan periksa state nyata setelah tool gagal. Jangan mengklaim file berubah hanya karena tercantum dalam patch yang dikirim.
- **Verifikasi:** Konteks seluruh file terdampak dibaca ulang dan patch pengganti diterima. Pemeriksaan ulang diff mengonfirmasi pemetaan papan disetujui dan reset/keyboard tetap terpisah. Tes tooling diagram lulus 1 tes, py_compile dan pemeriksaan struktur rencana lulus, SVG hasil regenerasi valid XML/LF, serta git diff --check lulus. Ini pemeriksaan dokumen/tooling, bukan uji game.

## L-009: Probe Python dengan XML inline rusak oleh quoting PowerShell

- **Salah:** Probe render memakai Python -c dengan string SVG berisi quote berlapis pada PowerShell.
- **Bukti:** Interpreter mengembalikan SyntaxError: unterminated string literal, sebelum renderer SVG dijalankan.
- **Dampak:** Probe pertama tidak membuktikan ada/tidaknya dukungan render; tidak ada diagram yang dihasilkan.
- **Aturan baru:** Untuk kode yang mengandung XML/JSON dan banyak quote, tulis skrip scratch di .tmp melalui patch, lalu jalankan berkasnya. Jangan menafsirkan kerusakan quoting sebagai kegagalan library render.
- **Verifikasi:** Probe pengganti .tmp/diagram-design/render_probe.py berhasil: halaman 841,89 x 595,28 pt, teks probe terbaca kembali, raster 1170 x 827 px. Implementasi berikutnya memakai import pymupdf agar tidak memakai alias fitz yang deprecated.

## L-010: Tes halaman diagram tidak menangkap teks keluar kotak

- **Salah:** Generator kandidat mengizinkan deskripsi dua baris tambahan di kotak setinggi 60 unit; baseline terakhir mencapai y+63. Tes awal memeriksa batas halaman, belum batas kotak modul dan benturan label.
- **Bukti:** Render PNG memperlihatkan teks melewati bingkai. Tes tambahan gagal untuk label monitor dan menemukan sembilan pasangan label bertumpuk, walaupun empat tes awal lulus.
- **Dampak:** Draf belum layak dimasukkan ke laporan. Draf tersebut tidak menggantikan diagram umum dan belum diserahkan sebagai hasil final.
- **Aturan baru:** Periksa teks terhadap kotaknya dan periksa benturan label pada render ukuran cetak, bukan hanya validitas SVG atau keberadaan teks. Jangan mengecilkan font untuk memaksa kepadatan; ringkas label atau ubah pengelompokan.
- **Verifikasi:** Kandidat diperbaiki dengan deskripsi satu baris dan pemisahan area label; lima tes v2 lulus setelah sebelumnya menunjukkan kegagalan. Pengembangan kandidat kemudian dihentikan mengikuti revisi pemilik ke diagram umum melalui draw.io. Pengujian tooling bukan bukti SIM/SYN/BOARD game.

## L-011: Kontrak event draf belum menjelaskan pemilik guard secara eksplisit

- **Salah:** Draf fungsi/antarmuka menempatkan syarat tembakan di uraian Input Processing tanpa langsung menyebut pemilik pemeriksaan bentuk/slot. Draf juga menjamin pengurangan nyawa sekali tetapi belum menjelaskan penolakan pemicu mati berbentuk level selama DYING.
- **Bukti:** Review read-only DeepSeek pada 2026-11-12 mengangkat I-1/I-2. Pemeriksaan sendiri menemukan data bentuk sebenarnya sudah ada pada actor_state dan slot dimiliki Items, tetapi kontrak pengendali belum eksplisit; guard FSM yang tersirat belum cukup sebagai uraian implementasi. Dua pemeriksaan kehadiran kontrak gagal sebelum klarifikasi.
- **Dampak:** Builder dapat memilih pemilik gating berbeda atau memakai ulang timeout/jurang sebagai pemicu urutan mati. Ini risiko rancangan, bukan bug hardware yang sudah direproduksi, karena RTL belum ada.
- **Aturan baru:** Untuk setiap event/status, jelaskan produsen, pemilik syarat kelayakan, konsumen, kapan dikonsumsi/dibuang dan kapan boleh dipicu kembali. Bedakan press, request, penerimaan alokasi slot dan status level. Jangan menerima seluruh penilaian reviewer tanpa memeriksa record/state yang sebenarnya sudah tersedia.
- **Verifikasi:** RANCANGAN_TEKNIS M02/M03/M06 dan §6 diperjelas: controller membaca player_state.form lalu memberi fire_req, Items memutuskan alokasi tanpa antrean tersembunyi; guard PLAYING + death_latched membatasi satu urutan mati, lives_zero hanya memilih hasilnya. Guard dokumen berubah gagal→lulus dan skenario SIM yang kelak harus dibuat dicatat pada §7. Checker ini hanya memeriksa kelengkapan kontrak tertulis, belum membuktikan perilaku SIM/SYN/BOARD.

## L-012: Penjelasan serial menggantikan eksekusi rencana (pengulangan L-003)

- **Salah:** Sesudah draf 12 modul dibuat dan direview, agent memperlakukan "oke, lanjut" sebagai permintaan tutorial tiga modul per balasan, alih-alih melanjutkan naskah dan DOCX yang menjadi tujuan pekerjaan.
- **Bukti:** Balasan terakhir menjelaskan ulang Player/Enemy/Items dari draf dan menjanjikan tiga modul berikutnya, tanpa perubahan file. Pemilik kemudian menegur "kapan P2 nya selesai" dan mempertanyakan rencana. Pemeriksaan folder P2 hanya menemukan empat dokumen perencanaan/rancangan/review, belum ada NASKAH_P2 atau DOCX.
- **Dampak:** Percakapan bertambah tanpa keluaran akhir; rencana sudah tersedia tetapi tidak dijalankan. Ini pengulangan L-003, bukan sekadar kekurangan penjelasan.
- **Aturan baru:** "Lanjut" pada pekerjaan aktif berarti lanjutkan keluaran berikutnya dalam rencana, bukan kembali ke mode mengajar kecuali diminta. Sajikan draf utuh untuk review; hanya keputusan penghambat yang memerlukan jeda. Gunakan batch keluaran dan jalankan guard file wajib + tes/QA sebelum menyebut P2 selesai. Diagnostik kecil tidak boleh diam-diam dihapus untuk mempercepat laporan.
- **Verifikasi:** Next di CHECKPOINTS dan RENCANA_KERJA diarahkan ke tiga batch keluaran; guard keberadaan enam keluaran benar-benar menolak saat naskah/DOCX/tes/review belum ada. Sesudah koreksi, NASKAH_P2 dan MATRIKS_KOMPATIBILITAS dibuat dan checker sumber/tautannya lulus. Ini bukti keluaran berikutnya mulai dikerjakan, bukan klaim P2 selesai; generator/DOCX/review akhir/QA dan diagnostik masih pending.

## L-013: Hunk tanpa perubahan menambahkan konteks patch yang keliru (pengulangan L-008)

- **Salah:** Patch checkpoint disertai bagian RENCANA_KERJA tanpa perubahan nyata, memakai konteks yang tidak mencakup awal kalimat pada baris aslinya.
- **Bukti:** Tool menolak dengan "Failed to find expected lines" pada frasa Milestone. Pembacaan ulang CHECKPOINTS mengonfirmasi tidak ada perubahan parsial yang boleh diklaim berhasil.
- **Dampak:** Pencatatan tertunda; sumber naskah/matriks yang sudah dibuat tidak rusak.
- **Aturan baru:** Saat koreksi state, kirim patch satu file dan hanya hunk yang mengubah isi. Baca baris nyata sebelum patch; pertahankan guard verifikasi konteks otomatis milik patch dan git diff --check. Jangan memasukkan hunk no-op sebagai pengingat pekerjaan berikutnya.
- **Verifikasi:** Patch pengganti per file diterima; Next dan kemajuan rencana mencatat berkas yang benar-benar sudah ada. Ini pengulangan L-008, bukan masalah pada naskah atau alat ekspor.

## L-014: Ekspor Word berhasil tetapi penutupan COM memakai argumen yang salah

- **Salah:** Skrip QA memakai `$word.Quit(0)`, padahal binding COM Word pada PowerShell meminta argumen opsional itu melalui referensi.
- **Bukti:** PDF 17 halaman terbentuk dan dapat dibuka, tetapi skrip exit 1 dengan `NonRefArgumentToRefParameterMsg`; satu WINWORD tersembunyi masih hidup tanpa dokumen.
- **Dampak:** Proses QA belum bersih walaupun ekspor PDF berhasil. Keberadaan PDF tidak cukup sebagai bukti seluruh skrip sukses.
- **Aturan baru:** Gunakan `[object]$saveMode=0` lalu `Quit([ref]$saveMode)` dalam finally. Sebelum menutup instance tertinggal, pastikan tidak terlihat dan tidak mempunyai dokumen; jangan membunuh seluruh proses Word.
- **Verifikasi:** Instance tersembunyi dengan Documents=0 ditutup melalui COM; ekspor ulang exit 0 dan menghasilkan PDF 16 halaman. Status ekspor dan cleanup dilaporkan terpisah.

## L-015: Lebar ID dan pemenggalan tabel DOCX belum aman pada render pertama

- **Salah:** Kolom ID lampiran hanya 1 cm tanpa noWrap, dan paragraf header/baris pertama tidak dijaga bersama kelanjutannya.
- **Bukti:** Render Word pertama memperlihatkan ID terbelah dan pemenggalan kurang baik; dua tes tambahan gagal untuk lebar 1,000125 cm dan keep_with_next=False.
- **Dampak:** Kehadiran semua ID dalam XML tidak menjamin keterbacaan dokumen cetak.
- **Aturan baru:** Uji berkas hasil untuk ID minimum 1,3 cm + noWrap, header berulang, cantSplit dan header/baris pertama keep_with_next. Tetap render setiap halaman karena tes struktur tidak dapat menilai seluruh tata letak.
- **Verifikasi:** Kolom menjadi 1,4 cm, tes regresi berubah gagal→lulus; ekspor ulang 16 halaman dan batas teks 0 pelanggaran. Seluruh contact sheet diperiksa, dengan pemeriksaan resolusi penuh tambahan pada diagram dan tabel padat.
  Catatan handshake yang ditambahkan langsung di bawah gambar sempat menghasilkan halaman terasing. Catatan dipindah ke §1.1 dan spasi badan diseragamkan. Gate final otomatis menolak halaman non-gambar <500 karakter, teks keluar batas aman, ID hilang dan PDF basi; render akhir 16 halaman lulus.

## L-016: Drop berkas browser tidak membuktikan diagram sudah diimpor

- **Salah:** Jalur impor awal memakai browser.files.drop tanpa terlebih dahulu membuktikan transport berkas didukung pada editor tersebut.
- **Bukti:** Tool mengembalikan UnknownVizError dan snapshot berikutnya tetap menunjukkan Shapes 0 / Connectors 0.
- **Dampak:** Tidak ada diagram yang boleh diklaim telah dirender melalui percobaan itu.
- **Aturan baru:** Setelah kegagalan transport, periksa state editor. Gunakan protokol load/export resmi draw.io untuk master yang sama, bukan menggambar ulang atau memakai kandidat yang ditolak.
- **Verifikasi:** Bridge lokal menerima event init/load/export dari embed.diagrams.net; SVG dan PNG asli draw.io tersimpan beserta manifest hash. SHA256 master tetap C1C43F130D9BE6F1334D74D47CC885BD6FA61BA92BA441FE6C4574AFC1ACF18B; PNG 3456×2283 tertanam byte-identik dalam DOCX.

## L-017: Menggunakan foreach dalam XDC membuat pin diagnostik tidak diterapkan

- **Salah:** Pin tombol dan LED disingkat menjadi loop Tcl di XDC yang dibaca melalui read_xdc.
- **Bukti:** Vivado memberi empat Critical Warning Designutils 20-1307, lalu Place 30-58: 21 port belum ditempatkan; laporan placement hanya memuat empat pin yang ditulis langsung. Ringkasan synth internal menyebut 0 critical warning tetapi total synth_design mencatat 4.
- **Dampak:** Placement gagal dan tidak ada bitstream yang layak dimuat. Ini kesalahan constraint, bukan bukti Basys 3 kekurangan pin.
- **Aturan baru:** Tulis constraint pin XDC secara eksplisit; control flow Tcl hanya di skrip build. Gate pin sebelum opt/place dan baca total pesan seluruh build, bukan hanya ringkasan mesin synth.
- **Verifikasi:** Dua tes regresi gagal untuk 21 pin yang hilang dan command foreach, lalu lulus setelah 25 pin ditulis langsung dan dicocokkan dengan Master XDC Digilent. Build ulang lulus SYN: WNS +2,068 ns, WHS +0,128 ns, 99 LUT/216 FF, 0 latch/BRAM/DSP/DRC/critical warning; CDC 8 safe/0 unsafe. Gate artefak memeriksa silang log/timing/utilisasi/CDC dan menyimpan hash. Bitstream belum diprogram; BOARD tetap belum dites.

## L-018: Nama font style DOCX tidak menjamin font yang dirender Word

- **Salah:** Generator menetapkan font.name Times New Roman tetapi membiarkan atribut font theme dari template Heading bawaan.
- **Bukti:** XML Heading1 masih mempunyai asciiTheme/hAnsiTheme=majorHAnsi; PDF Word merender judul Diagram blok sistem sebagai Calibri-Bold. Tes baru menolak atribut theme dan gagal pada Heading 1.
- **Dampak:** Tes font.name awal lulus walaupun heading berbeda dari arah tampilan P1.
- **Aturan baru:** Hapus atribut theme pada style laporan dan tetapkan keluarga font eksplisit untuk ascii/hAnsi/eastAsia/cs. Periksa font span pada PDF hasil ekspor, bukan hanya properti python-docx.
- **Verifikasi:** Tes regresi berubah gagal→lulus; suite generator akhir 15 tes lulus. Font lima heading wajib dan tiga heading lampiran pada PDF Word benar-benar TimesNewRomanPS-BoldMT; gate final memeriksa delapan span tersebut.

## L-019: Hunk no-op terulang saat sinkronisasi status publik (L-008/L-013)

- **Salah:** Patch PRD/README kembali disertai hunk penutup yang tidak mengubah isi, setelah konteks hunk-hunk lain.
- **Bukti:** Tool menolak konteks Asset readiness; pembacaan ulang PRD dan README memastikan keduanya belum berubah. Ini pengulangan, bukan perubahan yang berhasil.
- **Dampak:** Satu upaya pembaruan status terbuang; tidak ada file rusak atau perubahan parsial yang diklaim selesai.
- **Aturan baru:** Patch status satu file per operasi, hanya hunk dengan perubahan dan urutan sesuai sumber. Untuk Update File multi-hunk, simpan draf di .tmp lalu jalankan tools/check_patch.py sebelum tool patch. Jangan bypass penolakan konteks dengan skrip penulisan ulang.
- **Verifikasi:** Kesalahan ini terulang pada audit checkpoint (hunk penutup Renderered yang tidak diperlukan); native guard menolak tanpa menulis. Ditambahkan preflight check_patch.py dengan empat tes gagal sebelum implementasi lalu lulus: no-op, urutan mundur, konteks salah dan perubahan valid. Preflight dipakai pada pembaruan ledger ini. Ini alat yang harus dipanggil, bukan interceptor global yang otomatis mengawasi semua tool call.

## L-020: Reviewer yang diminta memakai skill mengabaikan pemuatan skill

- **Salah:** Subagent review akhir menganggap review dokumentasi read-only tidak mempunyai skill relevan dan tidak memanggil tool skill, walaupun prompt meminta skill plan/pelaporannya.
- **Bukti:** Laporan sesi ses_e3011541dffeS2a4tMUUm8idlJ mengakui tidak memuat skill; reviewer juga tidak menjalankan tes atau QA render akhir.
- **Dampak:** Temuan dapat diuji silang, tetapi laporan tidak boleh disebut review yang memenuhi seluruh proses skill atau menggantikan verifikasi sesi utama.
- **Aturan baru:** Nilai temuan berdasarkan sumber dan bukti, bukan gelar model/verdict. Saat memberi tugas review berikutnya, sebutkan ID skill wajib secara eksplisit; jangan membiarkan reviewer memutuskan bahwa read-only mengecualikan pemuatan skill.
- **Verifikasi:** Sesi utama memakai requesting-code-review/receiving-code-review, memeriksa seluruh temuan, menjalankan 15 tes generator dan QA sendiri. Kekurangan proses reviewer dicatat di REVIEW.md; tidak diklaim sudah diperbaiki retroaktif atau disembunyikan melalui review kedua.

## L-021: Ekstraksi PDF dicetak ke stdout PowerShell dengan encoding non-UTF8

- **Salah:** Probe Python mencetak baris PDF berisi panah Unicode memakai encoding stdout cp1252.
- **Bukti:** UnicodeEncodeError muncul ketika mencetak daftar awal halaman; PDF tetap valid dan tidak diubah.
- **Dampak:** Satu keluaran diagnostik terhenti, bukan kegagalan DOCX atau ekspor Word.
- **Aturan baru:** Probe teks Unicode memakai `python -X utf8` atau skrip yang mengatur encoding eksplisit; jangan mengubah isi dokumen hanya agar terminal lama dapat mencetaknya.
- **Verifikasi:** Perintah ulang -X utf8 menampilkan 18 halaman iterasi beserta sumber halaman terasing, lalu revisi/QA final menghasilkan 16 halaman tanpa halaman terasing.

## L-022: Hunk patch disusun tidak mengikuti urutan file sumber

- **Salah:** Patch PRD memasang perubahan US-12 sebelum kembali mengubah US-5 pada file yang sama.
- **Bukti:** Tool melaporkan konteks US-5 tidak ditemukan, padahal pembacaan ulang membuktikan teksnya masih sama. Urutan hunk maju-lalu-mundur adalah perbedaan yang dihilangkan pada patch pengganti.
- **Dampak:** Pembaruan ditolak; tidak ada perubahan parsial yang diteruskan sebagai berhasil. Bukan alasan mengubah isi requirement atau memakai penulisan ulang seluruh file.
- **Aturan baru:** Urutkan hunk sesuai posisi sumber dan pecah patch yang panjang. Gunakan preflight multi-hunk serta tetap periksa state setelah kegagalan.
- **Verifikasi:** Patch terurut diterima. Tes test_rejects_backwards_hunks menolak urutan mundur, sementara test_accepts_real_changes_in_source_order menerima perubahan sah. Suite preflight empat tes lulus; checker catatan aktif juga lulus setelah status diperbarui.

## L-023: Pemeriksaan publikasi bergantung pada pasangan data dan blacklist parsial

- **Salah:** Tes publikasi awal membandingkan PNG hanya dengan hash dalam manifest yang bisa diedit bersamanya. Pemeriksaan tautan memakai blacklist direktori dan tidak mencakup `docs/rubrik.md` yang di-ignore.
- **Bukti:** Review 2026-11-13 menemukan kedua celah; reproduksi di memori pada sesi utama menerima PNG+manifest yang diubah bersama dan tautan rubrik lokal. Kedua input negatif tidak ditolak sebelum perbaikan.
- **Dampak:** Suite bisa hijau walaupun ekspor bukan byte yang disetujui atau README menautkan file yang tidak tersedia pada checkout publik. Tidak ada file akademik yang diunggah atau master diagram yang diubah.
- **Aturan baru:** Identitas artefak yang disetujui dipin ke hash independen. Tautan lokal diperiksa terhadap batas root, keberadaan file dan `git check-ignore --no-index`, bukan blacklist parsial saja. Uji hasil checker dengan input negatif sebelum mengandalkannya untuk publikasi.
- **Verifikasi:** Reproduksi yang sama berubah gagal→lulus: kedua mutasi ditolak. Suite 15 tes tooling lokal tetap lulus; snapshot publik diuji terpisah sebelum commit. Ini verifikasi dokumentasi/tooling, bukan SIM/SYN/BOARD baru.
