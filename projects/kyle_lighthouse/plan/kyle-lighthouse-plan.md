# Kyle — The Signal Fire

**Summary**: A one-minute 16:9 photoreal adventure short: a boy carries a lantern out along a storm causeway to a dead lighthouse, climbs the tower, strikes a match and relights the lamp. The fourth LoRA-driven film, and the first whose **subject** was chosen to satisfy the constraint rather than its shot list.

**Sources**: [[kyle-lora-plan]] (the trained identity), [[lindsey-summit-plan]] §6, [[kyle-debut-plan]] §6, [[lindsey-palace-plan]] §6, [[headless-cli-pipeline]].

**Last updated**: 2026-09-29

---

## 1. The idea behind the idea

Three films in, the accumulated rule is blunt: **LTX responds to what a shot is *of*, and not at all to instructions about what not to do.** "She does not turn her head" turned anyway, twice. "The compass never lifts" lifted anyway, twice.

If prompts cannot forbid motion, the only remaining lever is to pick subjects whose **natural** motion is already the motion wanted. That is the whole reason this film is set in a storm on a dead lighthouse:

| Shot needs to hold for | What is moving in it | Why it cannot go wrong |
|---|---|---|
| s1, s8 | surf, spray, cloud, a lighthouse beam | sea and weather have no correct state to drift away from |
| s3 | a lantern **hanging on a hook** | swinging *is* its natural behaviour — the exact failure from [[lindsey-summit-plan]] s3, inverted |
| s4 | a match flame in cupped hands | fire animates itself, and it is hands in front of a stationary head |
| s6 | lantern light moving on a curved wall as he climbs | the light moves because he does, and he is seen from behind |
| s5, s7 | rain on glass; light strengthening on a face | small, bounded, self-evident |

s3 is the pointed one. On the last film a held compass floated out of frame twice, including once told explicitly not to. Here the object hangs from a hook, so the model's instinct to move it produces the shot instead of ruining it.

## 2. Inherited rules, applied without rediscovery

- **Face shots budgeted at 7.0–7.5 s** (s2, s7) — every frontal face clip across three films has drifted at ~8 s.
- **No shot asks for a head turn.** Stills are straight-on with nowhere to rotate to.
- **s4 is the one shot with real human movement**, and it is hands cupped around a match in front of a stationary head — the pattern that held 9.5 s on both `kyle_debut` s6 and `lindsey_summit` s4.
- **"The light stays constant"** in every motion prompt, which eliminated the dim-to-black failure on the last film.
- **Kyle's dataset is close-heavy** (16 turnaround frames, one full body), so the wides sit at 0.85 with the face small or turned away, and the two shots with no person carry no LoRA.

## 3. Shot list

| # | Shot | Input master | LoRA weight | Budget |
|---|---|---|---|---|
| s1 | Establishing: the causeway and how small he is, from behind | coast | 0.85 | 9.0 s |
| s2 | Close-up: salt spray on his face | kyle | 1.0 | 7.0 s |
| s3 | Macro: the storm lantern swinging on its hook — no face | kyle | 0.6 | 7.0 s |
| s4 | He strikes a match and shields the flame in both hands | kyle | 1.0 | 9.5 s |
| s5 | The dark lamp room and the great cracked lens — no person | lamproom | **none** | 8.0 s |
| s6 | The climb: the iron spiral stair, from behind and below | lamproom | 0.85 | 9.5 s |
| s7 | The lamp catches — warm light floods his face | kyle | 1.0 | 7.5 s |
| s8 | The beam goes out across the water — no person | coast | **none** | 8.5 s |

66.0 s kept − 7 × 0.75 s crossfades = **60.75 s**.

Palette is cold desaturated grey with warm firelight — the third distinct look in three films, after the palace's warm gold and the summit's cold blue dawn.

## 4. Locks

- **subject** — `kyle_kx boy`, a nine-year-old boy, this exact face, neat dark hair wet with spray
- **wardrobe** — heavy oiled canvas coat in dark slate, thick cream fisherman's wool sweater, coil of rope over one shoulder, battered brass storm lantern
- **coast** — storm-battered granite headland at dusk, black wet rock, white surf, a stone causeway out to a ruined pale-stone lighthouse, iron-grey cloud and spray
- **lamproom** — a great cracked fresnel lens on a brass carriage, salt-clouded panes, rusted railings, a spiral stair through the floor
- **style** — anamorphic 35mm live-action adventure, photoreal wet wool and oiled canvas, storm light at dusk, cold desaturated colour with warm firelight

## 5. Settings

| Stage | Setting |
|---|---|
| Still | FLUX.2 [klein] 9B (8-bit S), 1024×576, 4 steps, CFG 1, shift 3, DDIM Trailing (sampler 16), edit mode strength 1.0 |
| LoRA | `kyle_lora_2000_lora_f32.ckpt` @ none / 0.6 / 0.85 / 1.0 per the table |
| Clip | LTX-2.3 22B [distilled] 1.1, 1024×576, 249 frames @ 25 fps, 8 steps, CFG 1, shift 5, TCD Trailing (sampler 19), SSS 0.3 — ~11 min each |
| Upscale | Real-ESRGAN x4plus → 3840×2160, crop fit, 40M — ~10 min per clip |
| Assemble | 0.75 s crossfades, clip audio kept, 1920×1080 delivery copy |

## 6. Log

- **2026-09-29** — spec written. All three masters right on one seed each (seed 3), now the fourth film running
  for which that is true. Still candidates rendering.

## Related pages
- [[kyle-lora-plan]]
- [[lindsey-summit-plan]]
- [[kyle-debut-plan]]
- [[lindsey-palace-plan]]
