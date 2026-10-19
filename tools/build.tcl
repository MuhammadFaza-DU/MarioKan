# build.tcl — Vivado batch build untuk MarioKan (Basys 3, XC7A35T-1CPG236-1)
#
# Pakai:
#   vivado -mode batch -source tools/build.tcl
#   vivado -mode batch -source tools/build.tcl -tclargs --synth-only
#
# Catatan penting:
#   Path yang mengandung spasi akan dipecah oleh parser Tcl Vivado.
#   Karena itu SEMUA argumen path dibungkus [list ...] di bawah.

set root [file normalize [file join [file dirname [info script]] ..]]
set src_dir   [file join $root src]
set constr_dir [file join $root constraints]
set build_dir [file join $root build]
set rpt_dir   [file join $build_dir reports]

file mkdir $build_dir
file mkdir $rpt_dir

set part "xc7a35tcpg236-1"
set top  "top_basys3"

puts "== MarioKan build =="
puts "root : <$root>"
puts "part : $part"
puts "top  : $top"

# ---------------------------------------------------------------- sumber
if {![file isdirectory $src_dir]} {
    puts "ERROR: folder sumber tidak ada: <$src_dir>"
    exit 1
}

set vhd_files [concat \
    [glob -nocomplain -directory $src_dir *.vhd] \
    [glob -nocomplain -directory $src_dir *.vhdl] \
]

if {[llength $vhd_files] == 0} {
    puts "ERROR: tidak ada file VHDL di <$src_dir>"
    exit 1
}

foreach f $vhd_files {
    puts "  read $f"
    read_vhdl -vhdl2008 [list $f]
}

# ---------------------------------------------------------------- constraint
set xdc_files [glob -nocomplain -directory $constr_dir *.xdc]
if {[llength $xdc_files] == 0} {
    puts "WARNING: tidak ada berkas XDC di <$constr_dir>"
} else {
    foreach f $xdc_files {
        puts "  xdc  $f"
        read_xdc [list $f]
    }
}

# ---------------------------------------------------------------- sintesis
synth_design -top $top -part $part -flatten_hierarchy rebuilt

report_utilization  -file [list [file join $rpt_dir post_synth_util.rpt]]
report_timing_summary -file [list [file join $rpt_dir post_synth_timing.rpt]]

if {[lsearch -exact $argv "--synth-only"] >= 0} {
    puts "== selesai (synth only) =="
    exit 0
}

# ---------------------------------------------------------------- implementasi
opt_design
place_design
route_design

report_timing_summary  -file [list [file join $rpt_dir timing_summary.rpt]]
report_utilization     -file [list [file join $rpt_dir utilization.rpt]]
report_clock_utilization -file [list [file join $rpt_dir clock_utilization.rpt]]
report_drc             -file [list [file join $rpt_dir drc.rpt]]
report_power           -file [list [file join $rpt_dir power.rpt]]

# ---------------------------------------------------------------- bitstream
write_bitstream -force [list [file join $build_dir "$top.bit"]]

puts "== selesai =="
puts "laporan : <$rpt_dir>"
puts "bitstream: <[file join $build_dir "$top.bit"]>"
