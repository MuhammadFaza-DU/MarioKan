# Adaptation notes: FPGA-Mario to MarioKan

## Evidence and scope

Reference: [nicklesimba/FPGA-Mario](https://github.com/nicklesimba/FPGA-Mario),
revision `077d8a510f398e90e20650698b9795cc2d5f797e`. Ten source files
were retained read-only under the ignored `reference/fpga-mario-077d8a5/`;
`manifest.json` records the source URL and SHA256 of each file. This is a
source-level comparison, not simulation of the reference or a completed port.
Preserve attribution and check applicable rights before redistributing source
or character artwork. Reference material is not included in the public repo.

## What must change

| Reference evidence | MarioKan design response |
|---|---|
| `lab8.sv:16–67` exposes CLOCK_50, 8-bit RGB channels, CY7C67200 OTG, SDRAM and audio/SRAM interfaces. Lines 152–202 instantiate HPI, a Qsys-generated NIOS system and VGA controller. | Replace the platform layer, not just pin names. Basys 3 uses 100 MHz, MMCM pixel clock, RGB444 VGA and the PIC24 PS/2 keyboard interface. No soft CPU, SDRAM or mandatory audio. |
| `ball.sv:21–53` combines position, collision-facing coordinates, health, score and room outputs. Lines 57–83 use 10-bit coordinates and a 639×479 boundary. Lines 95–123 instantiate multiple combinational wall probes and detect frame edges. | Reimplement Player physics using Q13.8/Q8.8, separate Game Data counters, camera/world coordinates and sequential collision requests. Use clock-enable scheduling; do not copy coordinate ranges or assume parallel ROM reads are free. |
| `goomba_controller.sv:30–37` instantiates four enemies at fixed room coordinates; `goomba.sv:17–48` uses screen bounds and repeated wall probes. | Preserve the intended enemy behavior as a reference only. Specify bounded slots, spawn records, off-screen policy and synchronous collision access for the new map/camera. |
| `qblock.sv:1–20,43–55` has per-object position/room and empty state. `coin.sv:1–24` and `mush.sv:1–30` receive block/spawn information and track collection. | Items / Blocks requests writes from one Level Memory owner. New game reloads the map; respawn retains used blocks and collected map state. Counter changes are events to Game Data, not independent score writers. |
| `fball.sv:1–16` has room/start coordinates and visual/position outputs, without a player-fire request in that interface. | Do not equate the same module name with the new projectile contract. Player FIRE eligibility is checked by the controller; Items allocates a bounded slot once per press and drops a request when full. |
| `wall.sv:1–17` computes room geometry in always_comb using 20-pixel wall dimensions. | Replace hardcoded geometry with an initial map and mutable active map; define synchronous read latency, arbitration and tile attributes. Map dimensions and physical BRAM allocation remain implementation gates. |
| `Color_Mapper.sv:17–55,92–129` selects many per-sprite color outputs and exposes RGB888. | Build a synchronous indexed tile/sprite/font pipeline with four 16-entry RGB444 palette banks. Delay sync/de by the same latency as color. Source PNG payload is not target ROM utilization. |

## Verification gates

- **SIM, not yet tested for the game:** compare intended motion/contact/item
  behavior with the new requirement; test signed boundaries, memory latency,
  event ownership, pause, reset versus respawn and commit timing.
- **SYN, not yet tested for the game:** integrated clock/port constraints,
  WNS/WHS ≥ 0, no latch/critical warning/DRC, and measured resource budgets.
- **BOARD, not yet tested for the game:** independently play through both
  input paths, then verify the required level on the actual 1080p VGA display.

The reference is not evidence that the new platform or complete design works.
Current progress and any independent diagnostic results belong in
`CHECKPOINTS.md`; this comparison does not upgrade their evidence level.
