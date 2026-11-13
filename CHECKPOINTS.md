# CHECKPOINTS — MarioKan

> Satu-satunya sumber progres project. Bentuk mengikuti skill `setup-early-project`
> (Current State → Change Log → Stable tags), lalu riwayat detail diarsipkan di
> bagian bawah. Hanya **sesi utama (PM/controller)** yang menulis file ini.

## Current State (2026-11-13)

**Verifikasi pembaruan publik:** 15 tes tooling lokal lulus (10 tes publik,
termasuk 5 tes README/ekspor baru; 5 tes kandidat v2 tetap lokal). Checker
catatan aktif dan diff --check lulus. Hash master draw.io tidak berubah;
PNG publik byte-identik dengan ekspor resmi sebelumnya. Hasil DOCX 16 halaman,
15 tes generator dan diagnostik pada checkpoint 2026-11-12 tetap bukti historis,
bukan pengujian ulang atau SIM/SYN/BOARD game baru. `tools/check_patch.py`
memeriksa hunk no-op/konteks/urutan; bukan interceptor otomatis semua tool call.

- **Acuan tetap:** D0 proposal final disetujui berdasarkan konfirmasi pemilik 2026-11-12, dicatat pada `stable-2026-11-12-v1`; tanggal persetujuan sebenarnya/status unggah belum diverifikasi. Keputusan input/reset/level/1080p/D-16 tetap berlaku. Repo publik (API GitHub dikonfirmasi ulang 2026-11-12), akademik lokal-only. Setup ingatan 2026-11-01 tetap menjadi riwayat, bukan checkpoint terbaru.
- **Dokumen lokal-only siap ditinjau:** `docs/proposal/proyek-2/Perancangan_Arsitektur_MarioKan_P2.docx`, **16 halaman**, sampul P1, diagram draw.io, lima bagian serta lampiran 24 koneksi/22 skenario/19 aspek. Review/perbaikan/QA selesai; 15 tes generator + 6 tes tooling lokal lulus. Gate PDF: 0 overflow/halaman terasing, 65 ID utuh. `REVIEW.md` memuat keputusan/batas; isi/usulan belum disetujui pemilik. Master dan P1 byte-identik; rubrik di `docs/brief/proyek-2.pdf`. DOCX tidak diregenerasi saat checkpoint agar tidak menimpa kemungkinan suntingan pemilik.
- **In progress:** Audit sistem terdokumentasi; diagnostik **input-only**, bukan game, tersedia di `.tmp/diagnostics/`. **SIM** `tb_input_probe` lulus untuk input mentah/receiver; **SYN** `input_probe_top` 148,4375 MHz: WNS **+2,068 ns**, WHS **+0,128 ns**, 99 LUT/216 FF, 0 latch/BRAM/DSP/DRC/critical warning, 25 pin cocok Master XDC dan CDC 8 safe/0 unsafe. Bitstream belum dimuat; **BOARD input/video/game belum dites**. SIM tidak mencakup decoder kendali penuh/game. Target/input/reset/1080p tetap keputusan final sebelumnya; kontrak teknis baru tetap usulan. Izin mengganti SRAM untuk diagnostik sudah ada, SPI flash tetap dilarang; monitor masih harus dipinjam.
- **Belum selesai / blocker nyata:** RTL game/fondasi video belum dibuat; analisis platform/antarmuka sebagian sudah tertulis, bukan lagi "belum mulai seluruhnya". Tinjauan pemilik dan penguncian parameter masih diperlukan. BOARD input memerlukan pemuatan SRAM/tindakan fisik; BOARD video memerlukan monitor. Mouse opsional Q-8 dan metadata D0 Q-10 tidak menghalangi P2 atau jalur input wajib.
- **Publikasi yang diizinkan pemilik (2026-11-13):** rapikan lalu push README Inggris untuk pembaca kuliah/portofolio/kontributor, gambar PNG ekspor draw.io resmi dan sumber editable. Lima tes publikasi memeriksa tautan/anchor/batas ignore, status bukti dan hash sumber/PNG independen; dua celah tes hasil review direproduksi lalu diperbaiki (L-023). Checkpoint baru `stable-2026-11-13-v1`, beserta dua commit dan tag 2026-11-12 yang belum terkirim, disetujui untuk push setelah audit. Status remote wajib dibuktikan dengan refs Git dan pemeriksaan konten GitHub; izin ini bukan izin flash/submit/scan berbiaya.
- **Pendamping checkpoint sebelumnya:** `.tmp/checkpoints/stable-2026-11-12-v2-local.zip` dan manifest hash tetap lokal. Kandidat v2/generator/tesnya di-ignore, tidak dihapus; akademik/diagnostik tidak masuk Git. Tag Git tidak mencakup materi ter-ignore; pulihkan dari tag lalu arsip pendamping untuk state lokal. Arsip ini tidak ikut push dan bukan backup off-device.
- **Next:** Pemilik meninjau DOCX dan membuat PDF final/pengumpulan sendiri. Jelaskan dampak penggantian SRAM, lalu muat bitstream diagnostik ketika siap mengamati tombol/byte keyboard bersama; SPI flash tetap dilarang. VGA/ROM menunggu monitor. Kunci parameter sebelum RTL, jangan kembali ke tutorial per modul. Rencana rilis/deploy belum dijawab; tidak menjalankan scan otomatis.

## Change Log (newest first)

> Log di bawah merekam status **pada saat kejadian**. Frasa lama "belum commit",
> "belum DOCX" atau "menunggu ekspor" bukan status aktif setelah checkpoint
> berikutnya; gunakan Current State dan daftar Stable tags sebagai acuan.

- 2026-11-13 - **README/diagram publik, persiapan checkpoint dan push disetujui:** pemilik memilih rapikan lalu push, gambar+sumber, README Inggris dan seluruh jenis pembaca. Ditambahkan PNG resmi byte-identik 3456×2283, manifest sumber/hash dan lima tes publikasi; master draw.io tidak diubah. README menjelaskan tahap rancangan, kontrol yang disetujui, batas bukti probe, navigasi dokumen dan build game yang belum tersedia; CONTRIBUTING mencatat pengecualian bahasa README. Review read-only tidak menemukan Critical/Important; dua temuan Minor pada kekuatan tes diverifikasi dengan input negatif, diperbaiki dan dicatat L-023. Suite 15 tes tooling lokal dan guard catatan lulus; tidak meregenerasi DOCX atau menjalankan SIM/SYN/BOARD baru. Izin mencakup checkpoint baru dan push commit/tag publik yang tertunda, bukan materi akademik/diagnostik, flash, deploy atau submit. Pemeriksaan refs dan tampilan GitHub dilakukan sesudah push, tidak diasumsikan berhasil dari izin. Skill: brainstorming/software-engineering, antislop/copywriting, TDD/debugging, review/penerimaan review, verification-before-completion; browser terpisah untuk QA publik, graph/setup tetap dilewati sesuai D-4.
- 2026-11-12 - **Checkpoint/sinkronisasi atas permintaan pemilik:** audit catatan aktif publik dan lokal menemukan status private pada CONTRIBUTING, status discovery PRD, janji agent mengamati papan sendiri, klaim toleransi monitor universal, catatan ekspor/DOCX lama dan checkbox rencana usang. Diselaraskan tanpa mengganti keputusan final atau menulis ulang riwayat. API GitHub read-only mengonfirmasi visibility public. Audio/klik ditandai opsional sesuai keputusan lama; reset boot dan batas false path diperjelas, diagnostik terpisah dari game pada seluruh catatan aktif. Ditambah `tools/check_project_notes.py`, dijalankan sebelum perbaikan dan menolak pola usang/batas kandidat, lalu wajib lulus sebelum commit. Kandidat v2 dipertahankan lokal dengan ignore spesifik; source legacy yang sudah dilacak tetap diberi label legacy. Commit/tag lokal disetujui, push tidak. Pendamping arsip lokal diverifikasi melalui hash setiap anggota dan disimpan terpisah dari Git; akademik/bitstream/log tidak masuk index. Tidak ada regenerasi DOCX, uji/flash papan, instalasi, setup global atau deploy pada tindak lanjut ini. Verifikasi memakai skill verification-before-completion dan prinsip TDD pada guard, bukan mengklaim SIM/SYN baru.
- 2026-11-12 - **DOCX P2 + review/QA, diagnostik input SIM/SYN:** ekspor resmi master melalui protokol draw.io load/export berhasil (PNG 3456×2283, SVG dan manifest hash), master/P1 tidak diubah. Tes generator ditulis lebih dahulu; DOCX dibentuk memakai identitas tujuh anggota/dosen dan logo dari P1. Word COM mengekspor PDF sementara; masalah penutupan COM, kolom ID, pemenggalan tabel, font theme dan halaman catatan terasing ditemukan/diperbaiki, lalu render final **16 halaman** diperiksa. Lima heading utama + tiga heading lampiran benar-benar Times New Roman pada PDF; 0 teks keluar batas, semua A01–A24/U01–U22/K01–K19 utuh. Review read-only `sekaigateway/ds/deepseek-v4.1-flash-1017#max` diperiksa sendiri: risiko rubrik root ditangani dengan pemindahan terverifikasi+gitignore; cakupan usulan dan balasan handshake ditambahkan tanpa mengubah diagram. Minor legacy/sampul/orientasi referensi ditunda, alasan di REVIEW.md. Reviewer mengaku tidak memuat skill; kekurangan ini dicatat, tidak diklaim memenuhi seluruh proses. Ditambahkan PORTING_NOTES berbasis sepuluh sumber terpin dengan hash cocok. **SIM** tb_input_probe lulus; **SYN** diagnostik input-only lulus pada part target (WNS +2,068 / WHS +0,128 ns, 99 LUT/216 FF, 0 latch/BRAM/DSP/DRC/critical warning). Build awal gagal karena foreach XDC, diperbaiki dengan constraint eksplisit dan dua tes pin gagal→lulus. Gate artefak memeriksa silang laporan/log/CDC. **Belum memuat SRAM; BOARD belum dites; tidak menyentuh SPI flash/src/constraints produksi.** Suite akhir 15 tes generator+6 tooling lama lulus, checker sumber/guard enam keluaran/py_compile/diff --check lulus. Pelajaran L-014…L-021 dan pembaruan L-004/L-015 dicatat. Skill utama: executing-plans, hardware-integration, software-engineering, TDD, systematic-debugging, review/penerimaan review, verification-before-completion dan Anti-Slop/copywriting during; browser/ego-browser untuk ekspor. Graph/setup dilewati sesuai D-4; tidak install/deploy/commit/tag/push/submit. Semua akademik lokal-only, index kosong; pemilik tetap harus meninjau isi/usulan dan menjalankan PDF/pengumpulan sendiri.
- 2026-11-12 - **Keluaran setelah koreksi alur:** dibuat lokal-only NASKAH_P2.md (lima komponen rubrik, IPO 12 blok, alur sistem, rencana VHDL dan 22 skenario SIM/SYN/BOARD) serta MATRIKS_KOMPATIBILITAS.md (19 aspek dengan bukti/risiko, uji awal dan gate). Laporan probe timing/utilisasi/DRC lama dibaca ulang dan pin Master XDC resmi Digilent dibaca melalui URL raw; tidak menjalankan SYN baru. Naskah menandai gambar DOCX belum diekspor, lampiran rinci harus disisipkan, parameter usulan dan seluruh uji fungsional belum dilakukan. Checker sumber memeriksa lima bagian, 12 IPO sesuai master, 22 skenario unik dengan stimulus/hasil/metode, 19 aspek dan tautan; lulus, py_compile dan diff --check lulus; kedua dokumen gitignored. Ini kemajuan naskah, **bukan DOCX/P2 selesai**. Guard final sebelumnya benar-benar menolak karena enam keluaran belum ada; sesudah penulisan masih belum ada generator/tes generator/DOCX/REVIEW akhir. Diagnostik tetap pending. Tidak ada perubahan diagram/RTL/flash/commit/tag/deploy.
- 2026-11-12 - **Koreksi eksekusi setelah teguran pemilik:** dua balasan sebelumnya mengubah "lanjut" menjadi penjelasan serial modul, padahal draf 12 modul sudah selesai ditulis. Pemilik menanyakan kapan P2 selesai dan mempertanyakan rencana. Ini pengulangan kesalahan alur L-003, dicatat L-012. Rencana diselaraskan menjadi tiga batch keluaran (isi/audit/naskah → draf DOCX → review/QA), tanpa membatalkan diagnostik kecil yang telah diminta atau menunggu game lengkap. Ditambahkan guard otomatis yang menolak klaim selesai bila enam keluaran utama belum ada. Pada saat pemeriksaan, folder P2 baru berisi RENCANA_KERJA, RANCANGAN_TEKNIS, CATATAN_DIAGRAM dan REVIEW_MODUL; naskah/DOCX belum dibuat. Tidak ada RTL/flash/commit/tag/deploy atau klaim SIM/SYN/BOARD baru. Skill diagnosing-superpowers dimuat untuk konteks keluhan, tetapi tidak menjalankan audit sesi global/subagent/export karena tujuan pemilik adalah melanjutkan P2, bukan laporan bug Superpowers; proses dilanjutkan dengan executing-plans/hardware-integration/Anti-Slop yang sudah dimuat.
- 2026-11-12 - **Draf fungsi dan antarmuka P2:** atas arahan "Yokk mulai", dibuat lokal-only `RANCANGAN_TEKNIS.md`: 12 blok dengan input/proses/output, pemilik state, laju/latensi, tipe tetap/parametrik dan pemetaan 24 koneksi diagram. Clock/boot reset, reset sesi, held/press, akses BRAM, usulan reload peta dan commit metadata saat blanking dijelaskan; parameter/urutan simultan/jadwal ROM tetap terbuka, bukan keputusan final pemilik. Reviewer yang dipilih (`sekaigateway/ds/deepseek-v4.1-flash-1017#max`) melakukan satu review read-only, tanpa Critical. Sesi utama menguji silang I-1/I-2: data bentuk/slot sudah tersedia tetapi pemilik gating perlu diperjelas; pemicu mati diberi guard PLAYING + death_latched, bukan edge timeout saja. Hasil/keputusan/batas review di REVIEW_MODUL.md; pelajaran L-011 dicatat. Checker dokumen 44 kondisi lulus setelah dua guard kontrak gagal→lulus; suite tooling lama 6 tes, py_compile dan diff --check lulus, bukan SIM game. Hash master draw.io dan PDF P1 tetap, naskah/review gitignored; tidak ada perubahan src/constraints, bitstream, BOARD, commit/tag atau deploy. Skill hardware-integration, brainstorming, executing-plans, antislop/copywriting, review/penerimaan review dan verification-before-completion dipakai; TDD dimuat untuk urutan guard dokumen, bukan klaim TDD RTL; graph/setup dilewati sesuai D-4. **SIM/SYN/BOARD rancangan ini belum dites**, cara pengujian direncanakan pada §7 draf. Persetujuan rincian tetap menunggu tinjauan pemilik.
- 2026-11-12 - **Diagram umum disetujui:** pemilik mengirim screenshot diagram terbuka di draw.io dan menyatakan "nice, gunakan ini". Sumber utama ditetapkan `docs/diagram/arsitektur.drawio` (12 blok fungsi/24 koneksi); README tidak lagi menampilkan SVG lama sebagai diagram aktif. PRD §4.4/D-16, AGENTS, rencana P2 dan CATATAN_DIAGRAM diselaraskan. Diagram native tidak diubah sesudah persetujuan ini. Screenshot adalah bukti review visual pemilik, bukan klaim agent membuka/mengekspor editor; ekspor gambar asli draw.io dan QA cetak/DOCX masih belum dilakukan. SVG/kandidat detail disimpan sebagai legacy, tidak dihapus atau diadopsi kembali. Ini persetujuan diagram umum, bukan seluruh RTL/P2. Pemeriksaan ulang XML/koneksi sumber lulus; tidak ada uji SIM/SYN/BOARD baru atau commit/tag. Skill hardware-integration, brainstorming, antislop/copywriting dan verification-before-completion yang sudah dimuat dipakai; graph dilewati sesuai D-4.
- 2026-11-12 - Pemilik mengirim screenshot draw.io sebagai acuan visual, lalu menegaskan **hitam-putih saja, jelas, Player/Enemy/Items terpisah, label fungsi/data singkat English**. Dibuat draf native `docs/diagram/arsitektur.drawio` dengan 12 blok fungsi, 6 perangkat I/O dan 24 koneksi, tanpa gambar/SVG tertanam, tanpa pastel/rounded/shadow. Catatan cakupan dan arti panah dua arah disimpan lokal-only di `CATATAN_DIAGRAM.md`; satu blok fungsi dapat mencakup beberapa entity VHDL, bukan klaim netlist aktual. Verifikasi sumber: XML parse, ID/endpoint/parent, jalur keyboard/tombol ke VGA, gaya monokrom, orientasi A4 landscape, batas halaman serta overlap kotak lulus melalui `.tmp/diagram-design/check_drawio.py`; suite tooling lama/kandidat 6 tes lulus dan diff --check lulus. **Belum diimpor/dirender di editor draw.io**, belum ada klaim posisi label/cetak lulus; review visual oleh pemilik sesuai pilihannya. SVG lama dan kandidat detail tidak ditimpa. Skill brainstorming, hardware-integration, antislop/copywriting dan verification-before-completion dipakai; knowledge graph dilewati sesuai D-4. Tidak ada SIM/SYN/BOARD baru atau commit/tag.
- 2026-11-12 - Klarifikasi revisi draw.io: pemilik tidak memilih jumlah blok tertentu; kelengkapan modul, koneksi, input dan output mengikuti rubrik P2. Pemilik akan mengirim screenshot dari mata kuliah lain sebagai acuan design system. Agent diminta membuat **file .drawio editable untuk direview pemilik di draw.io**, bukan harus menggambar melalui GUI. Tunggu screenshot sebelum menyusun diagram baru; isi fungsional tidak disalin dari contoh lintas mata kuliah. Tidak ada diagram draw.io yang sudah dibuat/diverifikasi, tidak ada perubahan diagram umum lama, dan tidak ada commit/tag baru.
- 2026-11-12 - **Steering pemilik:** diagram diminta lebih umum dan mudah dipahami, bukan terlalu detail; pengerjaan harus melalui draw.io, karena pendekatan SVG/image generator dinilai tampak AI. Pengembangan kandidat detail dihentikan untuk klarifikasi. `docs/diagram/arsitektur.svg` belum diganti. File kandidat `architecture-v2.json`, `arsitektur-draft.svg/.png`, generator v2 dan tesnya tetap disimpan, bukan hasil final atau keputusan modul yang disetujui. Konsep generatif `.tmp/diagram-design/visual-concept.png` memakai openai/gpt-image-2 dan mengandung angka teknis keliru, tidak diadopsi sebagai sumber koneksi/label. Sepuluh sumber acuan dipin dan disimpan read-only di `reference/fpga-mario-077d8a5/`; sumber dan catatan uji tooling dapat dipakai kembali. Belum ada reviewer, RTL, pemrograman board, atau uji SIM/SYN/BOARD baru. Editor/ekspor draw.io belum diverifikasi; belum commit/tag.
- 2026-11-12 - Pemilik memilih **"Setuju pemetaan ini"** setelah tabel dan contoh keyboard eksternal dijelaskan. Disetujui panah/A-D bergerak, Space/atas/W lompat, Shift kiri/Z lari/bola api, atas/bawah menu, Enter konfirmasi, P/Esc pause; tekan/tahan mengikuti papan, reset tetap sw[0], tanpa tembakan otomatis. PRD D-15/§4.3/rencana tes, panduan input, AGENTS, README dan rencana P2 diselaraskan. Persetujuan kontrol papan, reset, dan keyboard lengkap, bukan persetujuan seluruh rancangan P2. Tidak ada RTL atau uji SIM/SYN/BOARD baru; belum di-commit/tag.
  Verifikasi dokumen: pemeriksaan struktur rencana dan git diff --check lulus; pencarian status aktif tidak menemukan pemetaan keyboard yang masih ditandai terbuka, selain kolom riwayat keputusan. Skill yang digunakan tetap hardware-integration, brainstorming, antislop/copywriting (during), dan verification-before-completion; TDD tidak diperlukan untuk perubahan prose tanpa kode perilaku baru. Knowledge graph tetap dilewati sesuai D-4.
- 2026-11-12 - Pemilik memilih saklar nomor 0, memastikan urutan reset, lalu menyatakan **"okeeeyyy, aku setuju"** setelah penjelasan: `sw[0]=1` menahan reset sesi; kembali 0 menuju menu, tidak otomatis bermain; START berikutnya mengembalikan tiga nyawa, skor/koin nol, waktu/blok awal. High score tetap selama papan menyala, tanpa penyimpanan persisten. PRD §4.3/§4.6/D-14/rencana tes, INPUT_GUIDE, README, AGENTS dan rencana P2 diselaraskan. Respawn tetap mempertahankan tilemap/skor/koin; pemulihan peta hanya untuk permainan baru harus dirancang di tahap arsitektur. Reset bukan penulisan konfigurasi/flash. Pemetaan keyboard masih terbuka. Verifikasi dokumen: struktur enam tahap rencana lulus dan git diff --check lulus; status aktif reset diperiksa lintas dokumen, riwayat lama dipertahankan. Skill hardware-integration dan prinsip brainstorming/antislop/verification yang sudah dimuat dipakai; knowledge graph dilewati sesuai D-4. Tidak ada RTL atau SIM/SYN/BOARD baru; belum di-commit/tag.
- 2026-11-12 - Pemilik memilih **"Cocok, setuju skema ini"** setelah contoh lima tombol dijelaskan, termasuk tiga tombol untuk berlari sambil melompat. Disetujui: menu atas/bawah dan tengah konfirmasi; bermain kiri/kanan bergerak, atas lompat variabel satu kali per tekan, bawah lari/bola api satu tembakan per tekan, tengah pause/lanjut; tahan tengah saat START tidak langsung pause. PRD US-13/§4.3/SC-7/D-13, panduan input, AGENTS, README, rencana P2, dan label diagram diselaraskan. D-8 menjadi riwayat; dua jalur penuh wajib, bukan saklar cadangan. Reset dan pemetaan keyboard belum diputuskan. Patch awal gagal karena konteks tidak cocok, dicatat pada L-008, lalu diterapkan ulang dari state yang diperiksa. Verifikasi: suite tooling 1 tes lulus, py_compile lulus, struktur rencana lulus, SVG valid XML/LF dan memuat dua jalur penuh; diff --check lulus. Rencana tetap gitignored; hash PDF P1 tetap identik. Skill: brainstorming, hardware-integration, software-engineering, TDD, verification-before-completion, antislop/copywriting (during, pilihan sesi). Knowledge graph dilewati sesuai D-4. Tidak ada RTL atau SIM/SYN/BOARD baru; belum di-commit/tag.
- 2026-11-12 - Setelah membahas lima level, pemilik memilih variasi peta dengan mekanik sama dan kebijakan **satu level wajib, empat pengembangan opsional**. PRD §2.3/§4.6, roadmap opsional, D-12, README, audit aset, dan rencana P2 diselaraskan. Empat peta bukan syarat minimum, tidak dianggap sudah dibuat, dan tidak dibahas rinci sebelum satu level lengkap terbukti. Tidak ada RTL atau pengujian hardware baru; belum di-commit/tag.
- 2026-11-12 - Verifikasi tooling diagram: ditemukan keluaran CRLF pada Windows, direproduksi dengan tes regresi, lalu diperbaiki memakai newline LF eksplisit. Suite `python -B -m unittest discover -s tools/tests -v` lulus 1 tes, py_compile lulus, SVG hasil regenerasi valid XML/LF, dan pemeriksaan struktur rencana lulus. Hash kedua salinan PDF final P1 tetap `A98E3A0CB6A5FF99E06A2001539DEF1EE9CAB030BAACE32EC25A43BB71C18093`. Tidak ada SIM/SYN/BOARD game baru. Pelajaran dicatat pada L-007; belum di-commit/tag.
- 2026-11-12 - Pemilik memilih monitor VGA langsung sebagai jalur utama, mengklarifikasi monitor uji harus dipinjam dan monitor demo belum ditentukan, lalu menegaskan **tetap 1080p saja** setelah membahas beberapa mode. PRD SC-6, perangkat tampilan, R-2, roadmap, dan D-3/D-11/Q-13 diperbarui; tidak menambahkan mode kompatibilitas atau mengklaim monitor sudah cocok. Diagram publik/generator diselaraskan ke Q13.8 dan VGA langsung; laporan final probe dibedakan dari estimated timing lama. Panduan membedakan konektor bawaan dari aksesori, dicatat pada L-006. Tidak ada bitstream yang dimuat atau uji BOARD video baru. Entri ini belum di-commit/tag.
- 2026-11-12 - Pemilik mengirim foto Basys 3 menyala. Foto memperlihatkan kabel pada PROG dan USB HID; konektor VGA tampak belum berkabel saat foto diambil. Adaptor dan layar tidak terlihat, sehingga jalur video masih perlu dikonfirmasi. Panduan input ditambah catatan orientasi PCB agar nama tombol tidak tertukar saat foto diputar. Tidak ada pemrograman atau uji input/video baru. Helper arsip gambar menghasilkan gambar sesi yang salah; hasilnya tidak dipakai dan scratch yang dibuat dihapus, dicatat pada L-005. Entri ini belum di-commit/tag.
- 2026-11-12 - Pemilik mengklarifikasi sasaran: jangan membangun seluruh game sekarang, tetapi audit seluruh risiko kompatibilitas dan tentukan pengujian wajib tiap fase agar rancangan tidak diteruskan dengan asumsi kecocokan FPGA. Dipilih audit dan program uji kecil. Keyboard eksternal dinyatakan terpasang; program SRAM lama tidak perlu dipertahankan; foto video menyusul. Tahap 2-3 rencana kerja diperbarui untuk matriks kompatibilitas menyeluruh dan program uji awal; belum ada pemrograman SRAM/SPI flash. Ini bukan persetujuan pemetaan/reset atau dokumen final. Entri ini belum di-commit/tag.
- 2026-11-12 - Pemilik meminta plan karena diskusi P2 melebar. Dibuat rencana lokal-only `docs/proposal/proyek-2/RENCANA_KERJA.md` dengan enam tahap, keluaran, gerbang, cakupan rubrik, batas diagnostik, reviewer yang telah dipilih, serta larangan commit/submit otomatis. Rencana menunggu tinjauan pemilik; belum menjadi persetujuan pemetaan/game final. Pelajaran pengendalian scope dicatat di `docs/LESSONS.md` L-003. Entri ini belum di-commit/tag.
- 2026-11-12 - Audit kesiapan aset: membaca 30 PNG asli pada commit acuan `077d8a510f398e90e20650698b9795cc2d5f797e`; ukuran/frame/palet belum seragam. Payload teoritis indeks 4-bit seluruh PNG sumber 15.385 byte, bukan alokasi BRAM hasil sintesis. Aset target, alat konversi, dan renderer belum tersedia; kelayakan game lengkap belum terbukti. Temuan disimpan di `docs/ASSET_FEASIBILITY.md`, inventaris PRD diperbarui, dan README diberi tautan. Bukti rinci di `.tmp/asset-audit.json`; tidak ada SIM/SYN/BOARD fungsional baru. Kegagalan API biner audit awal dicatat di `docs/LESSONS.md` L-002. Entri ini belum di-commit/tag.
- 2026-11-12 - Pemilik menyatakan penjelasan perbedaan lima tombol papan, keyboard USB eksternal, kabel programmer, dan saklar nomor 0 sudah jelas serta meminta dokumentasi. Dibuat `docs/INPUT_GUIDE.md` dengan diagram posisi tombol dan tabel kendali terpisah; README diberi tautan. Status memahami penjelasan dipisahkan dari persetujuan pemetaan/reset, yang masih terbuka. Verifikasi koreksi L-001 diperbarui di `docs/LESSONS.md`. Entri ini belum di-commit/tag.
- 2026-11-12 - Discovery P2: catatan dosen meminta input dan alur game diperjelas, arah konverter video dibuktikan, serta perbedaan desain acuan Altera dan target Basys 3 diterangkan. Pemetaan/reset dan rancangan final belum disetujui. Pemeriksaan FTDI + JTAG mendeteksi `xc7a35t_0` dan DONE=1 tanpa pemrograman/reset; bukti di `.tmp/build/hardware-inspection.txt` dan log Vivado. Tidak ada SIM/SYN baru atau uji fungsional BOARD. Kesalahan komunikasi agent (singkatan kendali tidak dijelaskan dan permintaan persetujuan terlalu dini) dicatat di `docs/LESSONS.md` L-001. Entri ini belum di-commit/tag.
- 2026-11-12 - Pemilik mengonfirmasi **proposal Proyek 1 telah disetujui**; status menunggu persetujuan ditutup dan langkah berikutnya diarahkan ke dokumen Proyek 2. Sumber status: konfirmasi pemilik, bukan pemeriksaan BRONE; tanggal persetujuan sebenarnya dan status unggah tidak diverifikasi. Tidak ada perubahan RTL atau pengujian SIM/SYN/BOARD baru. Checkpoint yang disetujui pemilik: `stable-2026-11-12-v1`.
- 2026-11-01 — Setup ulang `AGENTS.md` (8 bagian, delta) + `CHECKPOINTS.md` (skill `setup-early-project`); log lama dipindah ke arsip — `tag stable-2026-11-01-v1`
- 2026-10-22 — Q12.8 → Q13.8 disinkronkan ke PRD + README; status D0 final — `c5936e3`
- 2026-10-22 — Catat hasil rename folder induk (`Project dan SourceCode` → `Project-SourceCode`) + perbarui path — `e976c8f`
- 2026-10-22 — Dokumen serah-terima rencana rename folder induk (handoff) — `7ed6f76`
- 2026-10-22 — Proposal final ditetapkan (rename + metadata PDF dibersihkan) — `f3836c7`…`bdc7780` (tag v1–v3)
- 2026-10-19 — `tools/make_proposal.py` dikeluarkan dari repo publik; README/checkpoint diperbarui — `c4d405f` (+`745aa0a`)
- 2026-10-19 — Audit lingkup kerja: git terisolasi, tidak ada file luar tersentuh — `11c4676`
- 2026-10-19 — Repo dijadikan PUBLIK + riwayat git dibersihkan (dokumen akademik lokal-only) — `9160df4` (+`623a117`)
- 2026-10-19 — README profesional + diagram SVG vektor + `tools/build.tcl` + aturan checkpoint wajib — `bb653d0`/`d575ef0`/`2b765f6`
- 2026-10-19 — Repo GitHub dibuat; catat batasan branch protection (403) + cara undang collaborator — `e8de132`/`4d93241`
- 2026-10-19 — Proposal Proyek 1 (DOCX + PDF) + generator + diagram blok — `651d736`
- 2026-10-19 — Struktur dokumen dirapikan + Proyek 1 (rubrik & ketentuan) diserap — `f0c0e65`
- 2026-10-19 — PRD v0.1 MarioKan ditulis — `6c79217`
- 2026-10-19 — Repo diinisialisasi + verifikasi toolchain (probe `SYN`, WNS +4,041 ns, `.bit` 2,19 MB) — `3e68197`

## Stable tags (if git)

- `stable-2026-11-13-v1` - README Inggris untuk semua pembaca, PNG resmi+sumber/provenance, tes publikasi dan catatan; checkpoint/push disetujui pemilik setelah verifikasi.
- `stable-2026-11-12-v2` - checkpoint dibuat lokal 2026-11-12: keputusan/catatan publik, master draw.io dan tooling; izin push tag diberikan 2026-11-13. Akademik/diagnostik/kandidat tetap pada arsip pendamping lokal yang tidak dipush.
- `stable-2026-11-12-v1` - persetujuan proposal Proyek 1 berdasarkan konfirmasi pemilik; langkah berikutnya dokumen Proyek 2. Hanya perubahan `CHECKPOINTS.md`.
- `stable-2026-10-22-v3` — proposal final (rename + metadata bersih) + Q13.8 sinkron di PRD & README (`bdc7780`)
- `stable-2026-10-22-v2` — rename folder induk `Project dan SourceCode` → `Project-SourceCode` (`4b44d40`)
- `stable-2026-10-22-v1` — handoff rename: audit lengkap, eksekusi dihentikan tanpa perubahan (`f3836c7`)
- `stable-2026-10-19-v4` — repo publik bersih, script proposal lokal-only, README sinkron (`70b324f`)
- `stable-2026-10-19-v3` — `make_proposal.py` dikeluarkan dari repo publik (`d307697`)
- `stable-2026-10-19-v2` — repo publik, riwayat bersih, proposal 7 anggota (`22cd75a`)
- `stable-2026-10-19-v1` — repo + README profesional + diagram SVG + build.tcl (`5bff195`)

---

## Riwayat detail (arsip)

> Konten di bawah dipindahkan **utuh** dari `docs/checkpoint.md` pada 2026-11-01.
> Format asli (entri bertanggal, terbaru dulu, dengan bukti `SIM`/`SYN`/`BOARD`)
> dipertahankan sebagai arsip. `docs/checkpoint.md` kini hanya penunjuk ke file ini.

#### (Arsip) Checkpoint - Progres & Riwayat Kerja

File ini adalah **satu-satunya sumber progres** proyek. Setiap sesi kerja
menambah entri. Tujuannya: siapa pun (manusia atau agent) bisa tahu posisi
proyek tanpa membaca ulang seluruh riwayat chat.

### Cara pakai

- Tambah entri **di paling atas** (terbaru dulu).
- Format: `## YYYY-MM-DD — <judul singkat>`
- Isi minimal: apa yang dikerjakan, **bukti** (SIM/SYN/BOARD), apa yang gagal,
  apa langkah berikutnya.
- Jangan hapus entri lama. Kalau ada koreksi, tulis koreksinya sebagai entri baru.
- Kalau sesuatu belum dites, tulis "belum dites" — jangan dihilangkan.

---

### 2026-10-22 (lanjutan 2) — Nama final proposal ditetapkan (rename)

**Keputusan pemilik**
Nama file proposal final = **`Proposal_P1_Muhammad Faza Difa'ulhaq.pdf`**
(format yang dipakai saat mengunggah ke BRONE, sama dengan nama saat pertama
dikirim). Nama-nama iterasi `rev` / `rev2` / `rev3` **tidak dipakai lagi**.

**Dikerjakan**
- `docs/proposal/Proposal-P1-MarioKan-rev3-2026-10-22.pdf` →
  `docs/proposal/Proposal_P1_Muhammad Faza Difa'ulhaq.pdf` (isi byte-identik,
  274.168 B, tidak ada perubahan dokumen).
- Entri checkpoint sebelumnya ditandai koreksinya (lihat catatan *Koreksi nama*
  di dua entri 2026-10-22 di bawah) agar penamaan tidak ambigu.

**Kondisi `docs/proposal/` sekarang (satu-satunya yang ada)**

```
docs/proposal/Proposal_P1_Muhammad Faza Difa'ulhaq.pdf   274.168 B  <- FINAL
docs/proposal/gambar/diagram-blok.png                    114.008 B  <- sumber Gambar 1
```

**Bukti**
- `Get-ChildItem docs\proposal -Recurse -File` → hanya 2 file di atas.
- Ukuran 274.168 B sama persis dengan `rev3` sebelum rename → rename murni,
  tidak ada kerusakan/regenerasi.
- Root repo tetap 5 file publik; `git status` bersih (folder `docs/proposal/`
  gitignored).

**Berikutnya**
- ~~Sinkronkan Q13.8 ke `docs/PRD.md` §4.5 dan `README.md`~~
  → **SUDAH DIKERJAKAN** 2026-10-22 (lanjutan 4, lihat entri paling atas).

---

### 2026-10-22 (lanjutan 4) — Q12.8 → Q13.8 disinkronkan ke PRD + README

**Latar**
Proposal final sudah memakai **Q13.8**, tetapi `docs/PRD.md` §4.5 dan
`README.md` masih menulis **Q12.8** — klaim yang **salah aritmetika**:
20-bit signed Q12.8 hanya menjangkau ±2.047,996, sedangkan level terlebar
212 metatile × 16 px = 3.392 px. Ini inkonsistensi terakhir yang tersisa
setelah proposal dibereskan.

**Dikerjakan**
- `docs/PRD.md` §4.5 (baris 361–368):
  - `Q12.8 (20-bit signed)` → **`Q13.8 (21-bit signed: 1 sign + 12 integer + 8 fraksi)`**
  - ditambah jangkauan eksplisit **±4.095,996** + headroom **703,996 px**
  - ditambah catatan bahwa Q12.8 **tidak cukup** (bukan hanya Q8.8)
  - baris konversi koordinat layar: `Q12.8` → `Q13.8`
- `docs/PRD.md` §6 tabel deviasi **D-10**: keputusan diubah ke Q13.8 +
  kolom alasan mencatat riwayat koreksinya (Q12.8 sempat dipakai, dikoreksi
  2026-10-22).
- `README.md` (baris 32–35): `Q12.8` → **`Q13.8`**, ditambah penjelasan singkat
  21-bit signed, ±4095.996 px, dan mengapa Q12.8 gagal.

**Bukti aritmetika (dihitung, bukan dikira)**
```
Q13.8  21-bit signed : min -4096.000000  max 4095.996094  ->  +-4095.996
Q12.8  20-bit signed : min -2048.000000  max 2047.996094  ->  +-2047.996
Q8.8   16-bit signed : min  -128.000000  max  127.996094  ->   +-127.996
level terlebar : 212 x 16 = 3392 px
Q13.8 headroom : 703.996094 px   -> cukup
Q12.8 cukup    : False
```

**Sisa penyebutan `Q12.8` (sengaja, bukan inkonsistensi)**
- `docs/checkpoint.md` — entri-entri historis di bawah, memang mencatat
  temuan saat itu.
- `docs/PRD.md` baris 364 & 522 — disebut sebagai **pembanding** ("Q12.8 tidak
  cukup") dan sebagai **riwayat koreksi** di D-10. Bukan klaim aktif.

**Berikutnya**
- Tidak ada pekerjaan dokumen yang tertunda. Berikutnya = mulai RTL fase 1
  (analisis modul repo acuan) setelah judul disetujui dosen.

---

### 2026-10-22 (lanjutan 3) — Metadata PDF dibersihkan

**Latar**
Metadata internal PDF final masih menyimpan nama kerja lama:
`title = "Proposal-Proyek-1-MarioKan_Rev - Google Dokumen"`. Kalau dosen membuka
*Properties* di PDF reader, yang muncul nama draf, bukan judul proposal.

**Dikerjakan** (`PyMuPDF`, script di `.tmp/` — scratch, tidak di-commit)
- `title` → `Proposal Proyek Akhir - MarioKan: Implementasi Game Platformer
  Bergaya Super Mario Bros Berbasis FPGA Basys 3 dengan Bahasa VHDL`
- `author` → 7 nama anggota (dipisah `;`)
- `subject` → `Proposal Proyek 1 - Mata Kuliah Sistem Digital Lanjut`
- `keywords` → `FPGA; Basys 3; Artix-7 XC7A35T; VHDL; game platformer; 1920x1080; MarioKan`
- `creator` / `producer` / `creationDate` **dibiarkan apa adanya** (jujur:
  Chrome + Skia/PDF m155 = memang ekspor Google Docs). Tidak dipalsukan.

**Jebakan yang ditemukan (penting untuk siapa pun yang mengedit PDF ini)**
1. `saveIncr()` → metadata tampil baru, **tetapi objek lama tetap ada di byte
   file**; `strings`/grep masih menemukan `MarioKan_Rev`. Tidak cukup.
2. `save(..., clean=True)` → **MERUSAK RENDERING**. Terukur: 2,5%–10,6% piksel
   berbeda per halaman pada dpi 110; spasi antar kata hilang sehingga teks
   terbaca `DENGANBAHASAVHDLkarena`. **Jangan dipakai.**
3. `save(..., garbage=4, deflate=True)` **tanpa `clean`** → satu-satunya opsi
   yang benar: piksel **identik 12/12 halaman**, teks identik, string lama
   **hilang total**, ukuran 274.168 → 273.904 B.

**Bukti (semua terverifikasi, bukan asumsi)**
- `piksel identik = True` untuk 12 halaman @ dpi 110 (perbandingan
  `pixmap.samples` per halaman terhadap file sebelum diedit).
- `teks identik = True` (ekstraksi text-layer per halaman).
- Pencarian byte: `MarioKan_Rev` / `Google Dokumen` / `Proposal-Proyek-1-MarioKan`
  → **semuanya False**.
- Metadata akhir: title/author/subject/keywords sesuai di atas.
- Isi dokumen tetap: `seg[6:0], an[3:0]`, `W7/U7/U2/W4`, `U16 (led[0]) … L1`,
  `Q13.8` ada, `Q12.8` tidak ada, `Disusun Oleh` ada, `Disusuh` tidak ada,
  12 halaman, 2.026 kata.
- Render halaman 7 + OCR: tabel pin terbaca benar (baris seven-segment cocok).

**Cadangan**
- `.tmp/backup_before_metadata.pdf` (274.168 B) = PDF asli **sebelum** metadata
  diedit. **SUDAH DIHAPUS** 2026-10-22 atas instruksi pemilik, setelah PDF final
  dinyatakan aman (12/12 halaman ter-render, byte lama nihil).
  Kalau perlu versi asli lagi: ekspor ulang dari Google Docs, lalu jalankan
  ulang prosedur metadata (lihat jebakan di atas — **jangan pakai `clean=True`**).

**Berikutnya**
- ~~Sama seperti entri sebelumnya (sinkron Q13.8 ke PRD + README)~~
  → **SUDAH DIKERJAKAN** 2026-10-22 (lanjutan 4).

---

### 2026-10-22 — Review proposal revisi pemilik vs rubrik + relokasi file

> **Koreksi nama (2026-10-22, lanjutan 2):** file hasil relokasi di entri ini
> sempat bernama `Proposal-P1-MarioKan-rev-2026-10-22.pdf`, lalu **dihapus**.
> Nama final yang berlaku sekarang: `Proposal_P1_Muhammad Faza Difa'ulhaq.pdf`.

**Dikerjakan**
- Membaca proposal revisi pemilik (ekspor Google Docs, 12 halaman, 2.012 kata,
  berjudul internal `Proposal-Proyek-1-MarioKan_Rev`) dan membandingkannya
  dengan `docs/rubrik.md`, `docs/PRD.md`, `README.md`, serta versi lama
  (`docs/proposal/Proposal-Proyek-1-MarioKan.pdf`, 10 halaman, 2.487 kata).
  > **Catatan (2026-10-22):** file pembanding ini **sudah dihapus**; angka
  > 10 hal / 2.487 kata dipertahankan sebagai riwayat pengukuran.
- Memindahkan PDF dari **root repo** ke `docs/proposal/` sebagai
  `Proposal-P1-MarioKan-rev-2026-10-22.pdf`. Root sebelumnya memuat dokumen
  akademik yang **belum di-ignore** → satu `git add -A` bisa membocorkannya ke
  repo publik.

**Bukti**
- `git status --untracked-files=all` → **bersih** setelah relokasi.
- Root kini hanya 5 file publik: `.gitattributes`, `.gitignore`, `AGENTS.md`,
  `CONTRIBUTING.md`, `README.md`.
- Tabel pin proposal dicek baris per baris terhadap
  `Basys-3-Master.xdc` resmi Digilent (diunduh, disimpan di `.tmp/`):
  clk/VGA/Hsync/Vsync/PS2/sw/btn/JA **cocok**; baris **LED** dan
  **seven-segment** salah urutan.

**Temuan (diserahkan ke pemilik untuk diperbaiki sendiri)**
- Typo hal. 1 `Disusuh` → `Disusun`.
- `led[15:0] U16 … L1` seharusnya `led[0]=U16 … led[15]=L1`;
  `seg[6:0], an[3:0] W7 … U2` seharusnya `seg[0]=W7…seg[6]=U7`,
  `an[0]=U2…an[3]=W4`.
- Klaim "Q12.8 (20 bit bertanda) menjangkau 3.392 px" **salah aritmetika**:
  20-bit signed Q12.8 maks ±2.047,996. Perlu Q13.8 (21-bit) atau x unsigned.
  Klaim sama ada di PRD §4.5 dan README → **belum diperbaiki**, menunggu
  keputusan pemilik.
- Caption Gambar 1 menumpuk tepi bawah gambar (bbox gambar berakhir y=625,0 pt,
  caption mulai y=620,1 pt → overlap ±4,9 pt).
- Label diagram efektif ≈4,6 pt saat dicetak (gambar 2046×1060 px di 15,09 cm).
- Tabel pecah halaman tanpa header berulang; satu header yatim (hal. 9).
- Cover kehilangan "Mata Kuliah: Sistem Digital Lanjut" + "S1".
- Judul §3 "Gambaran Kerja" ≠ istilah rubrik "Gambaran cara kerja".
- Tidak ada sitasi dalam teks meski daftar pustaka 10 entri; tidak ada
  pernyataan orisinalitas/atribusi aset.

**Status penilaian (pendapat, bukan nilai dosen)**
Keempat komponen rubrik (20/25/25/30) menurut penilaian reviewer berada di
**Level 5**; kekurangan ada di detail teknis & format, bukan substansi.

**Berikutnya**
- Pemilik memperbaiki sendiri di Google Docs → menyerahkan versi benar.
- ~~Menunggu keputusan: Q13.8 vs unsigned 20-bit~~ → **sudah diputuskan Q13.8**
  (dipakai di proposal final).
- ~~Sinkronkan ke `docs/PRD.md` §4.5 dan `README.md`~~
  → **SUDAH DIKERJAKAN** 2026-10-22 (lanjutan 4).

---

### 2026-10-22 (lanjutan) — Proposal FINAL ditetapkan + file lama dihapus

> **Koreksi nama (2026-10-22, lanjutan 2):** entri ini memakai label iterasi
> `rev`/`rev2`/`rev3` sebagai penanda kerja, **bukan** nama file final. Nama file
> final sekarang: `docs/proposal/Proposal_P1_Muhammad Faza Difa'ulhaq.pdf`
> (= isi `rev3`). Label iterasi di bawah dipertahankan sebagai riwayat.

**Latar**
Pemilik menyerahkan tiga iterasi perbaikan di hari yang sama. Iterasi ketiga
(`rev3`, 12 hal, 2.026 kata, dibuat 07:18 UTC) dinyatakan **final**.

**Riwayat iterasi (semua terverifikasi dari text-layer PDF)**

| Iterasi | Dibuat | Yang berubah |
|---|---|---|
| `rev` | 06:37 UTC | versi pertama dari pemilik (2.012 kata) |
| `rev2` | 07:05 UTC | `Disusuh`→`Disusun`, LED `U16 (led[0]) … L1 (led[15])`, Q12.8→**Q13.8** (hal. 5 & 9), tabel 4.1 jadi 1 halaman (font 10 pt) — **tapi kolom seg/an tertukar** |
| `rev3` | 07:18 UTC | kolom seven-segment dibetulkan: Sinyal `seg[6:0], an[3:0]`, Pin `W7 … U7 (seg), U2 … W4 (an)` |

**Dikerjakan**
- `docs/proposal/` dibersihkan atas instruksi pemilik. **Dihapus (4 file):**
  `Proposal-P1-MarioKan-rev-2026-10-22.pdf`,
  `Proposal-P1-MarioKan-rev2-2026-10-22.pdf`,
  `Proposal-Proyek-1-MarioKan.docx`, `Proposal-Proyek-1-MarioKan.pdf`
  (dua terakhir = deliverable lama 2026-10-19, 10 hal).
- **Tersisa saat itu:** `Proposal-P1-MarioKan-rev3-2026-10-22.pdf` (274.168 B)
  + `gambar/diagram-blok.png`. → **Sudah di-rename** jadi
  `Proposal_P1_Muhammad Faza Difa'ulhaq.pdf` (lihat entri lanjutan 2 di atas).

**Bukti**
- Tabel pin §4.1 `rev3` dicek ulang ke `Basys-3-Master.xdc`: baris
  seven-segment **cocok penuh** (`seg[0]=W7`…`seg[6]=U7`, `an[0]=U2`…`an[3]=W4`).
  Seluruh tabel pin kini **0 error**.
- `git status` bersih; root repo tetap 5 file publik.

**Cacat yang MASIH ADA di versi final (diketahui, diterima pemilik)**

> Berlaku untuk file final `Proposal_P1_Muhammad Faza Difa'ulhaq.pdf`.
> Semua terverifikasi ulang dari PDF final, bukan dari ingatan.

- Caption Gambar 1 masih menumpuk gambar (overlap **4,9 pt**).
- Daftar pustaka keluar margin kiri **1,27 cm** (entri di x=72 pt, body x=108 pt).
- Header tabel belum berulang (hal. 4, 8, 10, 11) + header yatim hal. 9.
- Kata `Seven-segmen` / `t` terpotong di kolom Perangkat.
- `±4.095,99` (eksaknya 4.095,996); `XC7A35TCpg236-1` (gaya beda).
- Judul §3 `Gambaran Kerja` ≠ istilah rubrik; cover tanpa `Mata Kuliah`/`S1`.
- Audio masih di kolom "Termasuk dalam proyek".
- **0 sitasi dalam teks** meski daftar pustaka 10 entri.

**Sudah benar di versi final (jangan diperbaiki lagi)**
- `Disusun Oleh` (bukan `Disusuh`).
- Tabel pin §4.1: `led[15:0]` → `U16 (led[0]) … L1 (led[15])`.
- Tabel pin §4.1: `seg[6:0], an[3:0]` → `W7 … U7 (seg), U2 … W4 (an)`.
- Fixed-point **Q13.8** (hal. 5 §3.2 dan hal. 9 §4.3.4) — bukan Q12.8 lagi.

**Berikutnya**
- ~~Sinkronkan Q13.8 ke `docs/PRD.md` §4.5 dan `README.md`~~
  → **SUDAH DIKERJAKAN** 2026-10-22 (lanjutan 4).
- Deliverable lama DOCX/PDF terhapus; bisa diregenerasi dari
  `tools/make_proposal.py` (34 KB, ada di disk, gitignored) bila diperlukan.

---

### 2026-10-19 (lanjutan 6) — `tools/make_proposal.py` dikeluarkan dari repo publik

**Latar**
Script generator proposal memuat teks proposal lengkap + daftar nama/NIM
anggota. Meski terlihat seperti tooling, isinya praktis membocorkan dokumen
akademik dalam bentuk kode. Pemilik memutuskan mengeluarkannya.

**Dikerjakan**
- `tools/make_proposal.py` di-`git rm --cached` dan masuk `.gitignore`.
  **File tetap ada di disk** (34.805 bytes) untuk dipakai pemilik.
- Riwayat ditulis ulang (`git filter-branch --index-filter`, 13 commit) agar
  script hilang dari seluruh riwayat, bukan hanya commit terakhir.
- Ketiga tag dibuat ulang agar menunjuk riwayat baru (sebelumnya masih
  menunjuk commit lama yang memuat script — sumber kebocoran).
- `README.md`: entri `make_proposal.py` dihapus dari daftar tools, ditambahkan
  ke daftar materi lokal.

**Bukti**
- `git rev-list --all --objects` → **tidak ada** objek bernama
  `make_proposal`, `rubrik`, `docs/brief/`, atau `docs/proposal/`.
- Tag diverifikasi menunjuk riwayat baru:
  `v1 → d575ef0`, `v2 → 623a117`, `v3 → c4d405f`.
- Force-push main + 3 tag sukses; `git ls-remote` mengonfirmasi remote.
- Tree publik (anonim, tanpa login) — **11 file**, tanpa satu pun dokumen
  akademik:
  `.gitattributes`, `.gitignore`, `AGENTS.md`, `CONTRIBUTING.md`, `README.md`,
  `docs/PRD.md`, `docs/checkpoint.md`, `docs/diagram/arsitektur.svg`,
  `tools/build.tcl`, `tools/make_architecture.py`, `tools/make_diagram.py`

**File lokal (tidak di-commit) — terverifikasi utuh**
`docs/rubrik.md` 3,3 KB · `docs/brief/ide-awal.md` 27,3 KB ·
`docs/brief/proyek-1.pdf` 201,9 KB · `docs/proposal/*.docx` 148,7 KB ·
`docs/proposal/*.pdf` 214,0 KB · `docs/proposal/gambar/diagram-blok.png`
111,3 KB · `tools/make_proposal.py` 34,0 KB

**Catatan**
- `reset --hard` dari `filter-branch` **tidak** menghapus file lokal kali ini,
  karena file akademik sudah berstatus untracked sejak pembersihan sebelumnya.
  Tetap di-backup lebih dulu sebagai pengaman.
- Pemilik akan mengganti `make_proposal.py` dengan versi bersih nanti
  (mis. template tanpa data anggota).

**Berikutnya**
- Menunggu: judul disepakati kelompok, deadline BRONE, model konverter
  VGA→HDMI → lalu fase 1 (analisis modul repo acuan).

---

### 2026-10-19 (lanjutan 5) — Audit lingkup kerja: git terisolasi, tidak ada file luar tersentuh

**Latar**
Pemilik menanyakan dua hal yang perlu dibuktikan, bukan diyakinkan:
(a) apakah ada dokumen akademik di luar folder project yang ikut terhapus,
(b) apakah `.git` menyebar ke folder lain.

**Hasil audit (semua terverifikasi)**

| Pemeriksaan | Hasil |
|---|---|
| `.git` di folder project | **ADA** — `...\Project-Terakhir-SDL\.git`, HEAD `refs/heads/main` |
| `.git` di folder induk (`VHDL`, `Project dan SourceCode`, `D:\Progamming`, `D:\`) | **TIDAK ADA** sama sekali |
| File di luar project yang terhapus | **TIDAK ADA** |
| `C:\Users\...\Downloads\Tugas 2 Conditional Programming_*.pdf` | **UTUH** |
| `WEBB\gamein`, `Aplikasi\Tazk`, `MATLAB`, `Lomba`, `Tes model`, `BEBAS CAMPURAN`, `Project C` | **SEMUA ADA** |
| Commit terakhir repo lain | Tazk `1a682e2` (2026-08-24), gamein `e55ddc2` (2026-10-19), Project_1 `1223b39` (2026-10-10) → **tidak berubah**, membuktikan tidak tersentuh |
| Operasi hapus sepanjang sesi | Hanya 3, semuanya di dalam project: `Remove-Item` PDF proposal (sebelum regenerate), `Move-Item` log Vivado ke `.tmp/`, `Rename-Item` folder project (gagal, ditunda) |
| Cakupan `git filter-branch --all` | Hanya ref **repo ini**: `refs/heads/main`, `refs/remotes/origin/main`, `refs/tags/stable-2026-10-19-v1`. Bukan repo lain di disk |

**Catatan teknis penting**
- `git rm -r --cached` hanya mengeluarkan dari index, **tidak** menghapus dari disk.
  Yang menghapus adalah efek samping `reset --hard` di akhir `filter-branch`,
  dan itu **terbatas di dalam repo ini**. Sudah dipulihkan penuh dari
  `.tmp/backup-akademik/`.
- Semua perintah git dijalankan dengan working directory = folder project ini;
  tidak pernah `cd` ke folder lain untuk urusan git.

**Status akhir**
- 19 file di project: 12 ter-track (publik) + 7 lokal (rubrik, brief ×2,
  proposal ×2, diagram, backup) — semuanya ada dan ukurannya sesuai.
- `git status` bersih → dokumen lokal tidak ter-track.

**Berikutnya**
- Menunggu keputusan: `tools/make_proposal.py` tetap publik atau dikeluarkan.
- Menunggu: judul disepakati kelompok, deadline BRONE, model konverter
  VGA→HDMI → lalu fase 1.

---

### 2026-10-19 (lanjutan 4) — Repo dijadikan PUBLIK + riwayat dibersihkan

**Dikerjakan**
- Repo diubah dari private → **PUBLIC** atas permintaan pemilik.
- Dokumen akademik dikeluarkan dari repo dan dari **seluruh riwayat git**:
  `docs/rubrik.md`, `docs/brief/`, `docs/proposal/`, dan `Ide-awal.md` (nama
  awal sebelum dipindah). Ditambahkan ke `.gitignore` (lokal-only).
- Riwayat ditulis ulang dengan `git filter-branch --index-filter` (10 commit),
  lalu `refs/original` dihapus, reflog di-expire, `git gc --prune=now`.
- Tag `stable-2026-10-19-v1` dibuat ulang di riwayat baru (menunjuk `0b76a83`).
- Proposal diregenerasi dengan **7 anggota** (tambah Irwanto Saputra Husni,
  255150300111001).

**Bukti**
- `gh repo view --json visibility` → `"PUBLIC"`, `isPrivate: false`
- Akses **anonim tanpa login**: `HTTP 200 | private=False | visibility=public`
- Tree publik (12 file): `.gitattributes`, `.gitignore`, `AGENTS.md`,
  `CONTRIBUTING.md`, `README.md`, `docs/PRD.md`, `docs/checkpoint.md`,
  `docs/diagram/arsitektur.svg`, `tools/build.tcl`,
  `tools/make_architecture.py`, `tools/make_diagram.py`, `tools/make_proposal.py`
- Riwayat lokal: `git rev-list --all --objects` → **tidak ada** objek bernama
  rubrik / docs-brief / docs-proposal / Ide-awal.
- Proposal: OCR halaman 1 mengonfirmasi 7 nama + NIM, termasuk Irwanto.

**Insiden & perbaikan**
- `git filter-branch` melakukan `reset --hard` di akhir sehingga file akademik
  **terhapus dari disk**. Sudah diantisipasi: sebelumnya di-backup ke
  `.tmp/backup-akademik/` → seluruh file berhasil dipulihkan dan terverifikasi
  (rubrik 3,3 KB; ide-awal 27,3 KB; proyek-1.pdf 201,9 KB; DOCX 148,7 KB;
  PDF 214 KB; diagram 111,3 KB).
- `git status` bersih → dokumen lokal benar-benar tidak ter-track.

**Batasan yang diketahui**
- Commit lama masih dapat diakses lewat **API GitHub jika SHA-nya diketahui**
  (mis. `c7d6e08`). Tidak terhubung ke branch/tag mana pun dan tidak bisa
  ditemukan lewat browsing, tetapi belum dipurge dari sisi GitHub. Pemilik
  memilih menerima risiko ini alih-alih menghapus repo.
- `tools/make_proposal.py` **tetap publik** dan memuat teks proposal serta daftar
  nama + NIM. Pemilik sudah menyetujui nama & NIM tampil publik.

**Berikutnya**
- Menunggu keputusan: apakah `tools/make_proposal.py` tetap publik atau
  dikeluarkan juga.
- Menunggu: judul disepakati kelompok, deadline BRONE, model konverter
  VGA→HDMI → lalu fase 1.

---

### 2026-10-19 (lanjutan 3) — README profesional, diagram SVG, checkpoint tag

**Dikerjakan**
- README ditulis ulang secara profesional: fokus rekayasa (arsitektur, video
  pipeline, status berbasis bukti), tanpa framing akademik.
- `tools/build.tcl` dibuat (sebelumnya disebut README tapi belum ada).
- Diagram ASCII di README diganti **SVG vektor** (`docs/diagram/arsitektur.svg`)
  karena box-drawing ASCII pecah di GitHub.
- `AGENTS.md` §5.0: aturan wajib menawarkan commit + tag + push setiap
  pekerjaan besar.

**Bukti**
- `build.tcl` dijalankan nyata: root ber-spasi ter-resolve benar, gagal dengan
  pesan jelas saat `src/` kosong (sesuai rancangan).
- SVG: XML valid (74 elemen), dirender Chrome headless 2× → 2400×2080 px,
  OCR membaca **29 label** dengan confidence 0.92–1.00.
- Tag `stable-2026-10-19-v1` dibuat (annotated) dan **ada di remote**
  (`git ls-remote --tags origin` mengonfirmasi).
- `git status` bersih; `main` sinkron dengan `origin/main`.

**Koreksi**
- Draft README pertama menulis "running on a Digilent Basys 3 board"
  (present tense) padahal belum ada RTL → dikoreksi jadi "targeting".
- README menyebut `tools/build.tcl` yang belum ada → file dibuat, bukan
  klaimnya yang dihapus.

**Belum terverifikasi**
- Tampilan README & SVG di GitHub (butuh jaringan + render browser; hanya
  diverifikasi lokal via Chrome).
- Badge di README belum dicek render-nya.

**Berikutnya**
- Menunggu: judul disepakati kelompok, konfirmasi deadline BRONE, model
  konverter VGA→HDMI, lalu mulai fase 1 (analisis modul repo acuan).

---

### 2026-10-19 (lanjutan 2) — Repo GitHub: private, contributor, batasan platform

**Dikerjakan**
- Repo dibuat dan dipublikasikan: **https://github.com/MuhammadFaza-DU/MarioKan**
- Visibilitas: **PRIVATE**.
- `CONTRIBUTING.md` diperluas: pembagian peran, alur branch/PR, aturan bukti,
  dan perintah mengundang collaborator.

**Bukti**
- `gh repo view MuhammadFaza-DU/MarioKan --json visibility` → `"PRIVATE"`
- `gh api repos/MuhammadFaza-DU/MarioKan --jq .private` → `true`
  (dua sumber independen, sepakat)
- `gh api .../collaborators --jq '.[].login'` → hanya `MuhammadFaza-DU`
- `gh api .../invitations` → kosong (belum ada undangan terkirim)
- `git ls-files` → 15 file; **tidak ada** bitstream, log Vivado, `.tmp/`,
  atau kredensial yang ter-commit.

**Gagal / tidak bisa (penting)**
- **Branch protection TIDAK dapat dipasang.** Dua jalur dicoba, dua-duanya
  ditolak **HTTP 403** dengan pesan "Upgrade to GitHub Pro or make this
  repository public to enable this feature":
  1. `PUT /branches/main/protection` (classic branch protection)
  2. `POST /rulesets` (repository rulesets)
- Artinya: aturan "jangan push langsung ke `main`" **hanya konvensi tertulis**,
  bukan paksaan teknis. Semua collaborator secara teknis tetap bisa push ke
  `main`. Ini dicatat juga di `CONTRIBUTING.md` agar tidak menyesatkan.
- Opsi untuk memaksakan: (a) upgrade akun ke **GitHub Pro**, atau (b) jadikan
  repo **publik** setelah tugas selesai.

**Keputusan**
- Undangan collaborator **dilakukan pemilik sendiri** (bukan oleh agent),
  memakai perintah `gh api --method PUT .../collaborators/<USERNAME> -f permission=push`
  yang sudah ditulis di `CONTRIBUTING.md`.
- Hak yang diberikan: **`push`** (bukan `admin`) → tidak bisa menghapus repo
  atau mengubah setting.

**Belum diverifikasi**
- Username GitHub kelima anggota belum diketahui → **belum ada yang diundang**.
- Belum ada Pull Request / branch dari kontributor (belum ada kontributor).

**Berikutnya**
- Pemilik mengundang 5 anggota dengan akses `push`, lalu mereka menerima
  undangan lewat email / halaman invitations.

---

### 2026-10-19 (lanjutan) — Proposal Proyek 1 (DOCX + PDF)

**Dikerjakan**
- Menyerap `docs/brief/proyek-1.pdf` → transkripsi terstruktur di `docs/rubrik.md`.
- Merapikan struktur dokumen: dokumen mentah dipindah ke `docs/brief/`.
- Menulis **proposal Proyek 1** sesuai 4 poin wajib dosen (judul, tujuan & fungsi,
  gambaran cara kerja, rencana implementasi).
- Membuat diagram blok sistem (PNG) via `tools/make_diagram.py`.
- Generator dokumen: `tools/make_proposal.py` (python-docx).
- Output: `docs/proposal/Proposal-Proyek-1-MarioKan.docx` + `.pdf`.
  > **Catatan (2026-10-22):** kedua file ini **sudah dihapus** dari disk atas
  > instruksi pemilik. Bisa diregenerasi dari `tools/make_proposal.py` bila perlu.

**Bukti**
- DOCX tersimpan, dikonversi ke PDF via Word COM: **10 halaman**, 2.455 kata.
- Teks terverifikasi lewat OCR PDF: cover tanpa nomor halaman, tidak ada baris
  tabel terpotong antar halaman, seluruh tabel & daftar pustaka tercetak utuh.
- Diagram terverifikasi lewat OCR PNG: 16 baris teks, confidence 0,98.

**Temuan penting**
- `websearch` mengembalikan **0 hasil**; Bing/Google/DuckDuckGo via fetch
  mengembalikan konten tidak relevan (GameHouse, Zhihu). Riset format proposal
  karena itu **tidak memakai sumber web** — disusun dari struktur akademik umum
  + penalaran atas rubrik. Ini keterbatasan yang harus diketahui.
- Referensi yang **terverifikasi aksesnya**: Digilent `Basys-3-Master.xdc`
  (isi file dibaca, pin cocok) dan README repo `FPGA-Mario` (penulis, toolchain).
  Referensi lain (UG472, UG473, UG901, IEEE 1076, CEA-861, Chapweske) adalah
  dokumen kanonik; URL AMD hanya memuat aplikasi JS saat diakses.

**Keputusan**
- Struktur proposal: **ikut persis 4 poin dosen** (bukan BAB I–III), atas
  permintaan pemilik.
- Judul dipakai: "MarioKan: Implementasi Game Platformer Bergaya Super Mario
  Bros. pada FPGA Basys 3 Menggunakan VHDL" — masih menunggu diskusi kelompok.
- Audio & mouse ditulis sebagai fitur dengan **catatan status jujur**
  (pengembangan lanjutan / opsional menunggu verifikasi).
- Bukti `SYN` (MMCM 148,4375 MHz, WNS +4,041 ns, bitstream) dimasukkan ke
  subbab 4.6 sebagai bukti kelayakan — mengangkat komponen rubrik terbesar (30%).

**Belum diverifikasi**
- Judul belum disepakati kelompok; daftar judul kelompok lain tidak bisa diakses.
- Tanggal pengumpulan proposal dari dosen: pemilik menyebut 23 Oktober 2026 23:59
  (perlu konfirmasi ulang di BRONE).
- Format resmi proposal tidak diberikan dosen; struktur mengikuti 4 poin wajib.

**Berikutnya**
- Review proposal oleh pemilik + kelompok → revisi bila perlu → unggah via BRONE.
- Setelah judul disetujui: mulai fase 1 (analisis modul repo acuan).

---

### 2026-10-19 — Fondasi: verifikasi toolchain & keputusan awal

**Dikerjakan**
- Membaca brief awal (`Ide-awal.md`) dan memeriksa repo sumber
  `nicklesimba/FPGA-Mario` (915 file, dapat diakses).
- Verifikasi toolchain Vivado di mesin ini.
- Menetapkan aturan kerja proyek (`AGENTS.md`) termasuk batas wilayah kerja.
- Menyiapkan kerangka repo (README, CONTRIBUTING, .gitignore, .gitattributes).

**Bukti**
- `SYN` — Vivado **v2026.1** di `D:\AMDDesignTools\2026.1\Vivado`.
  Device `xc7a35tcpg236-1` tersedia (30 varian `xc7a35t*`).
- `SYN` — Uji penuh desain *probe* (counter + `MMCME2_BASE`):
  `synth_design → opt → place → route → write_bitstream` **sukses**,
  0 error / 0 critical warning, **bitstream 2,19 MB** terbentuk.
- `SYN` — MMCM `CLKFBOUT_MULT_F=11.875`, `DIVCLK_DIVIDE=1`,
  `CLKOUT0_DIVIDE_F=8` menghasilkan `clk_pix` **148,438 MHz**
  (period 6,737 ns), **WNS +4,041 ns**, 0 DRC error.
  → Premis 1080p di speed grade `-1` **layak**, bukan spekulasi.
- Repo sumber: PNG sprite asli **tersedia** di
  `ECE385-HelperTools-master/.../sprite_originals/` (24 file) → tidak perlu
  rekonstruksi sprite dari ROM.
- Python 3.12 + Pillow 12.2.0 tersedia → tooling konversi sprite bisa jalan.

**Temuan penting**
- Path repo mengandung spasi (`Project dan SourceCode`) → Vivado memecah
  argumen. Workaround `[list $path]` sudah diverifikasi berfungsi.
  Rename folder induk **ditunda**: ada agent lain yang aktif di folder itu
  (proses `astro preview` PID 2324 di `WEBB\gamein`).
- Rename folder project sendiri juga gagal karena dikunci session yang sedang
  berjalan → dilakukan bersamaan saat rename induk nanti.
  > **Update 2026-10-22:** rename induk **SUDAH SELESAI**.
  > `D:\Progamming\Project dan SourceCode` -> `D:\Progamming\Project-SourceCode`.
  > Path repo sekarang **tidak mengandung spasi**, jadi masalah pemecahan argumen
  > Vivado di atas sudah tidak berlaku. Workaround `[list $path]` tetap dipakai.

**Keputusan**
- Audio **ditunda** ke pengembangan lanjutan (deviasi resmi dari brief —
  hardware audio belum tersedia). Wajib tercatat di PRD.
- Contributor: **dokumentasi & testing saja**, tidak menyentuh RTL.
- Knowledge graph tidak dipakai; progres dilacak di file ini.
- Konverter VGA→HDMI **sudah dimiliki** (TV hanya punya HDMI).

**Belum diverifikasi**
- Semua RTL game — belum ada.
- Uji papan fisik — belum ada.
- Perilaku konverter VGA→HDMI terhadap clock 148,4375 MHz — belum diuji.

**Berikutnya**
- Menunggu dari pemilik proyek: spesifikasi alat, rubrik penilaian,
  ketentuan tugas akhir → lalu menulis `docs/PRD.md`.
