# BOT Builders Champion, comic cut — 90-Second Team Film from a 3-Page Comic

**Summary**: A 90-second, 16:9, 3D-animated film of Kevin's FIRST LEGO League team, made from a 3-page, 15-panel comic. The team discovers a tiny insect at the farm, studies it, builds it a habitat, tests the robot through failures, and wins the competition. It's the third film through the [[idea-to-video-blueprint]] and the first with five recurring characters, all shown in group close-ups.

**Sources**: `projects/bot_builders_champion/v2-comic-cut/raw/comic_page1.jpg`, `comic_page2.jpg`, `comic_page3.jpg` (1024×1536 each, added 2026-09-23); [[idea-to-video-blueprint]]; [[lindsey-art-plan]] §0 and [[kyle-antarctic-rescue-plan]] §0 (method, masters, rules).

**Last updated**: 2026-09-24 (**delivered** at 63.5 s — §0 results; the five-kid rule cost ~27 s against the 90 s plan)

---

## 0. Results — 2026-09-23 23:20 → 2026-09-24 04:11

**Delivered**: `projects/bot_builders_champion/v2-comic-cut/final/bot_builders_1920x1080.mp4` (**63.5 s**, 100 MB), `bot_builders_3840x2160.mp4` master (308 MB), `bot_builders_1280x720.mp4` preview (27 MB). Music from 0 s with a 2 s fade; mean −15.8 dB, peak −0.4 dB.

![Final film, one frame every 4 s](assets/fll-bot-final-strip.jpg)

![Masters: Kyle, second boy, Lindsey, girl A, girl B, and the team master every shot was locked to](assets/fll-bot-masters.jpg)

**Short of the 90 s plan.** The five-kid rule came first. In 7 of 12 clips LTX pulled the camera back after 3–6 s and invented extra children in the new margins, or a teammate walked out. Every such clip is cut before the first wrong frame, and there was no time left to re-render the tight shots wider. Nothing in the film has six kids.

| Shot | Take | Kept | Why it stops there |
|---|---|---|---|
| S1 farm | v1 | 6.8 s | end fade |
| S2 magnifier | v1 | 5.2 s | black edge bar, then a pull-back |
| S3 poster | v2 | 5.2 s | the standing girl drifts out after f130 (v1: 3.6 s) |
| S4 workbench | v1 | 8 s | end fade |
| S5 robot test | v1 | 4.8 s | pull-back, a 6th kid at f130; v2 was the same |
| S6 oops | v1 | 7 s | end fade |
| S7 adjust | v1 | 3.4 s | pull-back, 6th and 7th kids from f90; v2 worse |
| S8 hall | v1 | 5.2 s | end fade (framing held) |
| S9 judge | v1 | 6.4 s | camera slides right; teammates leave frame |
| S10 mission | v1 | 4.4 s | pull-back, extra girl ~f140 |
| S11 champions | v1 | 5.4 s | end fade |
| S12 trophy | v1 | 10 s | its fade is the film's ending |

15 LTX renders for 12 shots, 45 still candidates plus 5 targeted edits, 6 masters.

![Rejected frames: S5 v1 and S7 v2 extra kids from a pull-back · S10 v1 extra girl · S3 v1 teammate walked out](assets/fll-bot-rejects.jpg)

### Stills: the count rule caught 4 of 12 on the first pass
- **S3, S10:** six or seven kids. The comic panel for S10 has six figures behind the table; every seed copied it.
- **S11:** four kids, and the trophy covered a face.
- **S6:** heads cut at the frame edge.
- **Fixes:** a left-to-right roster in the prompt (S11), a new padded input (S6), and **S10 rebuilt as an edit of the approved S5**, so the correct five came from pixels, not from the comic.
- **S3 unresolved:** girl A kept rendering with straight hair (9 candidates plus 2 targeted edits; the braids moved onto other kids instead). Kept by the failure rule (best attempt): five kids, but only one of the braided girls is visibly braided.

### New rules (→ [[idea-to-video-blueprint]])
1. **Tight group framing makes LTX pull back and invent people in the new margin.** "The camera does not move at all: no zoom, no pull-back, no pan … no one enters from any edge" helped S8 hold, but did **not** stop S5, S7 or S10. For group shots, frame the still **wider with room around the group** so there's no margin to fill, or plan 4–5 s shots.
2. **A comic panel with extra figures gets copied, whatever the prompt says.** Rebuild that still as an edit of an approved shot with the right cast.
3. **A standing character next to a seated group walks off.** Seat everyone, or keep the shot short.
4. **Budget for group films:** expect ~5 s usable per 10 s clip. A 90 s film needs about 18 shots, not 12.

## 1. Decisions (Kevin, 2026-09-23 intake)

| Question | Answer |
|---|---|
| Project | **separate** from `fll_farm`; that film's no-faces rule stays with it |
| Faces | OK. All five families consent. Faces come from the comic; no photos |
| **Extra kids** | **none**. Exactly the five teammates in every frame. Background people are adults only (judge, announcer, blurred crowd). Any extra child is an automatic reject |
| Team | Kyle (white cap) and Lindsey (long straight hair) reuse their masters from [[kyle-antarctic-rescue-plan]] and [[lindsey-art-plan]], re-dressed. New masters for the second boy (spiky hair), braided girl A (black shirt) and braided girl B (pink sleeves) |
| Look | 3D animated, same as the other two films |
| Size | **16:9**: 1024×576 render → 3840×2160 master plus 1920×1080 and 1280×720 copies. Five kids fit side by side (9:16 would cramp them) |
| Length | 90 s, 12 shots |
| Logos and text | removed. Black team shirts carry a small round blue-and-green bug emblem with no lettering; banners are plain; no brand logos |
| Group shots | **full group close-ups** (Kevin's choice over the safer mix of groups and pairs) |
| Music | **"Victory"**, The_Mountain (Pixabay, 2:19) → `raw/clips/music/victory_the_mountain.mp3`. First 90 s: quiet for 45 s, then a steady climb to −10 dB by 90 s. 2 s fade out |
| Overnight | Claude judges at full size and restages a shot that keeps failing. Deliver the film plus this report, commit, push and notify |

## 2. Storyboard (approved)

| # | Keep | Panel | Shot | Kids |
|---|---|---|---|---|
| S1 | 8 s | 1 | farm: five kids lean over leaves and nasturtiums | 5 |
| S2 | 7 s | 2 | Kyle's magnifying glass on a tiny larva, the second boy amazed | 2 |
| S3 | 8 s | 3 | Lindsey points at a life-cycle poster, four watch | 5 |
| S4 | 8 s | 4+6 | workbench: sketches, the insect habitat jar | 5 |
| S5 | 8 s | 7 | robot testing on the competition field, laptop | 5 |
| S6 | 5 s | 8 | "oops": the robot tips over, five gasp | 5 |
| S7 | 7 s | 9 | girl B adjusts the robot, the others watch | 5 |
| S8 | 8 s | 10 | competition hall entrance, cheering (standing, not walking) | 5 + adults |
| S9 | 8 s | 11 | judging table, Lindsey presents to a judge | 5 + 1 |
| S10 | 7 s | 12 | the robot places the ring, fists clenched | 5 |
| S11 | 8 s | 14 | champions announced, hands on cheeks, glowing trophy | 5 + 1 |
| S12 | 10 s | 15 | hugging the trophy, confetti | 5 |

Dropped panels: 5 (the "let's go" cheer duplicates S12), 6 (folded into S4), 13 (hands-in huddle; a pile of hands is the Lindsey S3 failure mode).

## 3. Consistency

- **Five masters**, all edits at klein strength 1.0 on a studio background:
  - **Kyle:** his Antarctic master with a white cap and the team shirt added (seed 2).
  - **Lindsey:** her master in the team shirt (seed 3).
  - **Second boy:** from panel 2 (seed 2).
  - **Girl A:** from panel 1 (seed 1).
  - **Girl B:** from panel 1, pink sleeves (seed 3).
- **Team master** (`masters/team.png`): a collage of the five masters in comic order, edited into one waist-up group portrait (seed 1; exactly five, faces kept). It's the left half of **every** diptych, so all five identities ride in one reference.
- **Every still prompt** names all five by look and says *"Exactly five children in the frame, all five fully visible, no other children anywhere"*. Adult shots add "the background people are all adults".
- **Every motion prompt** says *"Exactly the same five children stay in the frame the whole time; no one enters or leaves"*, and the camera holds completely still. No walking. Everyone stays in place, because walking groups merged and teleported in `fll_farm` v1.
- **QC at full size**, with an explicit **child count** in every still and at five frames per clip. Also hands per person, intersections, faces against the team master, and the end fade (auto-detected).

## 4. Run

The run-spec is `projects.json → fll_bot_builders["run-spec"]`: every shot is a diptych with the `team` master, at 1024×576.

```bash
scripts/film_run.py fll_bot_builders stills      # 36 candidates
scripts/film_run.py fll_bot_builders pick sN K   # judge, full size, count kids
scripts/film_run.py fll_bot_builders clips
scripts/film_run.py fll_bot_builders qc          # judge sets take + trim
scripts/film_run.py fll_bot_builders finish
```

Estimate: stills ~40 min, clips 12 × 9.5 min plus redos ~2.5 h, upscale ~1.8 h. About 5–5.5 h in total.

## Related pages
- [[idea-to-video-blueprint]] · [[scripts-reference]]
- [[kyle-antarctic-rescue-plan]] · [[lindsey-art-plan]] — Kyle's and Lindsey's masters come from here
- [[projects]]
