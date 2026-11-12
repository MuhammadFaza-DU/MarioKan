# MarioKan

**A planned hardware game engine for FPGA.** MarioKan is being designed as a
2D platformer implemented entirely in programmable logic, without a CPU or
operating system. The game RTL is not implemented yet; current evidence is
limited to the probes listed below.

[![Target](https://img.shields.io/badge/target-Basys%203%20%C2%B7%20XC7A35T--1-informational)](#hardware-target)
[![HDL](https://img.shields.io/badge/HDL-VHDL--2008-informational)](#)
[![Toolchain](https://img.shields.io/badge/toolchain-Vivado%202026.1-informational)](#)
[![Video](https://img.shields.io/badge/video-1920%C3%971080%20%40%2060%20Hz-informational)](#video-pipeline)

---

## Overview

The design covers player physics, enemies, items, collision, scoring and a
game state machine in synthesizable VHDL, targeting a Digilent Basys 3 board
(Xilinx Artix-7 `XC7A35T-1CPG236C`). The intended game runs standalone on the
board, with no host computer in the loop; this is not a claim of a working game.

The minimum delivery is one complete level. Up to four additional maps are
optional development after that baseline is verified, reusing the same
mechanics and assets rather than introducing a separate game engine per level.

The design is defined by what it deliberately leaves out:

- **No framebuffer.** There is no external SDRAM or DDR on the board, and no
  on-chip memory large enough to hold a 1920×1080 frame. Every pixel is
  computed as it is scanned out, in a short pipelined datapath that reads tile
  and sprite ROMs on demand.
- **No soft CPU.** No NIOS, no MicroBlaze, no RISC-V core. Game logic is
  concurrent hardware, updated 60 times per second via a clock enable derived
  from the vertical blanking interval.
- **No derived clocks.** A single MMCM output feeds the entire design; slower
  rates are expressed as clock enables, which keeps timing analysis honest.
- **No floating point.** Position and velocity are fixed-point integers
  (Q13.8 for world position, Q8.8 for velocity), because `real` is not
  synthesisable and never will be. Q13.8 is 21-bit signed — 12 integer bits
  give ±4095.996 px, enough for a 3392 px level; a 20-bit Q12.8 would saturate
  at ±2047.996.

The renderer is planned around a 384×216 logical resolution upscaled by an
exact integer factor of 5 to 1920×1080. Reusing logical pixels may reduce
work, but does not automatically provide 25 consecutive clocks per fetch.
ROM/port scheduling and integrated timing still need verification.

## Hardware target

| | |
|---|---|
| Board | Digilent Basys 3 |
| FPGA | Xilinx Artix-7 `XC7A35T-1CPG236C` |
| Logic capacity | ~20,800 LUTs · 41,600 FFs · 50 BRAM36 · 90 DSP · 5 MMCM |
| Board clock | 100 MHz (`W5`) |
| Video out | VGA, 4 bits per channel (12-bit color) |
| Display path | Direct VGA to a monitor; the test monitor must be borrowed and its 1080p input support is not verified yet |
| Input | Two planned full control paths: USB keyboard via PIC24/**PS/2**, or the five on-board buttons |
| Audio | No codec on board; deferred from the baseline, optional future Pmod work |
| External memory | None usable |

For the five on-board buttons and external USB keyboard connection, see the
[Input guide](docs/INPUT_GUIDE.md). The board-button mapping and press/hold
behavior were approved on 2026-11-12. Session reset was approved separately:
`sw[0]=1` holds reset, returning it to `0` opens the menu, and START begins a
fresh game with three lives, zero score/coins and initial time/map state.
The stored high score is preserved by this switch reset, but is not persistent
across power-off or reprogramming. The keyboard mapping and press/hold rules
were also approved separately on 2026-11-12; see the input guide for keys and
examples. Neither gameplay control path nor session reset is implemented yet.
The separate raw-input diagnostic is not their implementation.

## Video pipeline

CEA-861 timing for 1920×1080 @ 60 Hz:

| | Active | Front porch | Sync | Back porch | Total |
|---|---|---|---|---|---|
| Horizontal (px) | 1920 | 88 | 44 | 148 | **2200** |
| Vertical (lines) | 1080 | 4 | 5 | 36 | **1125** |

2200 × 1125 × 60 Hz = 148.5 MHz. The MMCM produces **148.4375 MHz** from the
100 MHz board clock (`CLKFBOUT_MULT_F=11.875`, `DIVCLK_DIVIDE=1`,
`CLKOUT0_DIVIDE_F=8`), a deviation of about −0.042%. This does not guarantee
that a particular monitor accepts the mode; the actual VGA display must be tested.

```
clk 100 MHz ──► MMCME2_BASE ──► clk_pix 148.4375 MHz ──► vga_timing ──► scaler ──► renderer ──► RGB444
                                      │
                                      └──► clock enable @ 60 Hz ──► game logic
```

Pixel coordinates are mapped to a 384×216 logical grid (48×27 tiles of 8×8),
then scaled ×5. All video outputs — `hsync`, `vsync`, `de`, RGB — are
registered together so they stay aligned.

## Architecture

The approved system-level diagram is
[`docs/diagram/arsitektur.drawio`](docs/diagram/arsitektur.drawio).
It was reviewed in draw.io by the owner and approved on 2026-11-12.
The editable master uses monochrome native shapes and connectors.

This is a functional architecture, not a synthesized RTL netlist. A block
can contain several VHDL entities; detailed implementation interfaces remain
part of the technical design. See [Project status](#project-status) for what
has actually been implemented.

| Functional block | Responsibility |
|---|---|
| Clock & Reset | Pixel clock, boot initialization and session-reset input |
| Input Processing | Keyboard reception/decoding, button debounce and normalized actions |
| Game Controller | Menu/game FSM, update coordination and render-state collection |
| Player | Player motion, form and animation state |
| Enemy | Goomba management and behavior |
| Items / Blocks | Items, fireballs and mutable block behavior |
| Collision Detection | Tile/object checks, hit results and game events |
| Game Data | Score, coins, lives, time and high score |
| Level Memory | Initial map and mutable active map |
| Asset Memory | Synchronous tile, sprite, font and palette storage |
| Video Generator | Timing, scaling, composition and aligned VGA output |
| Status Display | LED encoding and seven-segment scanning |

Rendered report/README exports must come from the approved draw.io master.
The report now embeds an official draw.io export; it is kept with the
local-only academic document, not published here. The old
`docs/diagram/arsitektur.svg` and its generator are retained as legacy,
not as the current architecture source. Rejected v2 candidates and their
generator/tests are local-only and ignored; no file was deleted. Do not
overwrite the approved design with those candidates.

Asset readiness and the limits of the preliminary memory estimate are recorded
in [Asset feasibility](docs/ASSET_FEASIBILITY.md). Source PNGs are available,
but target sprite ROMs and the conversion tool are not implemented yet.
The platform/interface comparison with the pinned reference HDL is in
[Adaptation notes](docs/PORTING_NOTES.md), not a claim of a completed port.

## Project status

This project is built in stages, and each stage has a defined exit criterion.
The table below reports **what has actually been proven**, not what is planned.

Evidence levels used throughout this repository:

| Level | Meaning |
|---|---|
| `SIM` | Verified in simulation only |
| `SYN` | Verified through synthesis, place & route, and timing closure |
| `BOARD` | Verified running on physical hardware |

| Milestone | Status | Evidence |
|---|---|---|
| Toolchain and target device available | `SYN` | Vivado 2026.1; `xc7a35tcpg236-1` present among 30 installed `xc7a35t*` parts |
| 148.4375 MHz pixel clock achievable on `-1` speed grade | `SYN` (archived probe) | `clk_pix` period 6.737 ns; final report **WNS +4.043 ns**, WHS +0.254 ns; 0 DRC findings |
| Bitstream generation | `SYN` | 2.19 MB `.bit` produced |
| Standalone input diagnostic (not game controls) | `SIM` / `SYN` | `tb_input_probe` passes; diagnostic at 148.4375 MHz: WNS +2.068 ns, WHS +0.128 ns, 99 LUT / 216 FF, 0 latch/DRC/critical warning; not programmed or physically tested yet |
| Game RTL (video, input, gameplay, audio) | — | **not implemented yet** |
| On-board verification | — | **not performed yet** |

> There are two separate probes: the archived MMCM/counter and the newer raw
> input diagnostic. Neither is the game. Their SIM/SYN evidence does not
> establish physical input behavior, gameplay or a compatible VGA monitor.

## Repository layout

```
CHECKPOINTS.md      Work log and current status
src/                Production VHDL RTL              (planned, empty)
constraints/        Production Basys 3 XDC           (planned)
sim/                Production VHDL testbenches      (planned)
tools/
  build.tcl         Vivado batch build script
  make_architecture.py   Legacy SVG generator (not the approved diagram source)
  make_diagram.py        Legacy proposal PNG generator (not the draw.io master)
  check_project_notes.py Active-note and public-checkpoint consistency guard
  check_patch.py      Preflight for one-file update patches (no changes applied)
docs/
  PRD.md            Specification — authoritative requirements
  checkpoint.md     Legacy pointer to ../CHECKPOINTS.md
  INPUT_GUIDE.md    Approved physical controls and evidence limits
  ASSET_FEASIBILITY.md Source asset audit, not final ROM utilization
  PORTING_NOTES.md  Pinned-reference platform/interface comparison
  diagram/          Approved editable draw.io master and legacy diagram material
```

Local-only material (not tracked, excluded via `.gitignore`): `docs/brief/`,
`docs/rubrik.md`, `docs/proposal/`, `tools/make_proposal.py`, `.tmp/`,
`reference/`, and the rejected v2 diagram candidates listed in `.gitignore`.
The public checkpoint preserves source documentation and the approved master,
not local academic documents, diagnostic binaries or scratch evidence.

`build.tcl` expects `src/` to exist and to contain at least one `.vhd` file;
it exits with an explicit message otherwise. As of now `src/` is still empty.

## Building

Requires Vivado 2026.1 with the Artix-7 device family installed.
Run from the repo root, placing Vivado's working files under `.tmp/build/`:

```powershell
$repo = (Get-Location).Path
New-Item -ItemType Directory -Force "$repo/.tmp/build" | Out-Null
Push-Location "$repo/.tmp/build"
try {
    & 'D:/AMDDesignTools/2026.1/Vivado/bin/vivado.bat' -mode batch -source "$repo/tools/build.tcl"
    # For synthesis only, append: -tclargs --synth-only
} finally {
    Pop-Location
}
```

Outputs land in `build/`:

```
build/reports/timing_summary.rpt
build/reports/utilization.rpt
build/reports/clock_utilization.rpt
build/reports/drc.rpt
build/reports/power.rpt
build/top_basys3.bit
```

The build writes those reports; the project's acceptance gates are then checked
against them: **WNS ≥ 0**, **WHS ≥ 0**, **zero inferred latches**, **zero DRC
errors**, and utilization below the device limits listed above. Build
artifacts (`build/`, `*.bit`, `*.dcp`, `.Xil/`) are git-ignored.

> **Path caveat.** Vivado's Tcl parser splits arguments on whitespace. If the
> checkout path contains spaces, an unwrapped path produces
> `ERROR: File 'C:/some/path' is a directory`. Wrap every path argument in
> `[list ...]`:
>
> ```tcl
> read_vhdl -vhdl2008 [list $f]
> ```
>
> `tools/build.tcl` already does this throughout. The parent folder rename
> completed on 2026-10-22; the current checkout has no spaces in its path.
> Keep quoting paths for checkouts elsewhere. See `CHECKPOINTS.md` for history.

## Checking notes and tooling

```powershell
python -B tools/check_project_notes.py
New-Item -ItemType Directory -Force .tmp | Out-Null
python -B -m unittest discover -s tools/tests -v
```

The first command checks selected active-note invariants and local-only
boundaries, including the Git index. The suite tests patch preflight and the
retained legacy SVG generator, not the draw.io export or VHDL game.
Academic DOCX tests and raw-input diagnostic evidence are local-only; they
are not expected to exist after cloning just the public repository.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for roles, branch workflow, and the
evidence rules that apply to every claim made in this repository.

## Design notes

Behavioural reference for game physics, enemy logic, and sprite sequencing is
[nicklesimba/FPGA-Mario](https://github.com/nicklesimba/FPGA-Mario)
(Nikhil Simha, Pranith Bottu) — an academic DE2/Quartus project using a NIOS II
soft core. MarioKan is not a port: the original design's soft CPU, Qsys
subsystem, USB host interface, and audio codec have no counterpart here. What
is carried over is *behaviour* — jump curves, collision response, animation
order — reimplemented as standalone hardware.

## Licensing and attribution

Source code in this repository is provided for educational and non-commercial
use.

Character designs and sprite artwork are the property of Nintendo and are used
here solely for non-commercial, academic purposes. No affiliation with or
endorsement by Nintendo is claimed or implied.
