# Portfolio rebuild — 2026-09-21

## Bugs found (verified, not guessed)

| Bug | Evidence |
|---|---|
| `assets/img/d455.jpg` renders as a black tile | mean luma **7**, **99.9%** of pixels near-black. Shipped as the "RGB-D colour fusion" gallery tile. |
| `emme.mp4` is unusable in a video slot | **1280x2770** (1:2.16 portrait). A full-page screen recording in a landscape frame. |
| Hero mispositions the candidate | "I build robots that have to work in the **water**." Every role in the current application queue is perception / SLAM / embedded / AMR / manipulation software. |
| Theme flips mid-page | dark hero -> white body -> dark again. Reads as three different sites; this is the "cluttered, hard to decipher" complaint. |
| No scannable hierarchy | 5 dense prose paragraphs per project. The strong numbers (1.62 m error, $8,710 removed, 321k samples) are buried inside sentences. |
| Wrong evidence class for the target roles | As-built wiring diagram, Rev B power tree, interconnect and companion-wiring drawings are electronics-design artifacts on a software application. |

## Decisions

- **One theme, dark throughout.** The instrument/telemetry look was already the
  strongest part of the design; the white middle section was fighting it.
- **Lead with morphology breadth.** Quadruped RL, 64-robot parallel training,
  manipulation, drone, underwater, SLAM. This is the single most differentiating
  thing about the candidate and it was buried below six long writeups.
- **Numbers become instruments.** Every measured figure is pulled out of prose
  into a labelled readout, so a hiring manager scanning for 20 seconds still
  gets the evidence.
- **Schematics out.** Ferbin's call, and the right one: he is applying for
  software roles, so a power tree reads as off-target. The *bring-up narrative*
  stays, because debugging under uncertainty is software evidence.
- **Prose cut to two paragraphs per project**, with the third-level detail kept
  in a collapsible block for the reader who wants it.

## Media added (all from Ferbin's own Udemy course work)

| Clip | Source | Shows |
|---|---|---|
| `quadruped_rl.mp4` | isaac-lab-custom promo | Single Barkour quadruped, learned gait |
| `rl_parallel.mp4` | isaac-lab-custom promo | 64 robots training in parallel |
| `go2_gait.mp4` | quadruped-go2 promo | Unitree Go2, measured reward finding |
| `manipulation_vla.mp4` | vla footage (cropped to strip Isaac UI) | Franka arm, block manipulation |
| `isaac.mp4` (existing) | Archenaux | Gerstner-wave ocean, RTX |
| `perimeter.mp4` (existing) | Lytespace | ArduCopter SITL perimeter patrol |
| `detection.mp4` (existing) | Archenaux | Underwater detector, live confidence |

All re-encoded h264 CRF 30, faststart, 1280px, 262-655 KB each.
