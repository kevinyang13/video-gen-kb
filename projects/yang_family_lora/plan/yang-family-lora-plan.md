# Yang Family — One LoRA, Three Subjects

**Summary**: The first multi-subject LoRA here: Kyle, Lindsey and Ivy trained into a single adapter, each behind its own trigger and class word. The thing it can do that three separate LoRAs cannot is put two of them in one frame.

**Sources**: [[kyle-lora-plan]] (v2 dataset), [[lindsey-lora-plan]], [[ivy-lora-plan]], [[blueprint-v2-research]].

**Last updated**: 2026-09-30

---

## 1. Why one adapter instead of three

Draw Things will load more than one LoRA at a time, but two *character* adapters fight over the same face — each
one is trained to pull any person in frame toward its own subject. So three separate LoRAs can render three
people one at a time and cannot render two of them together. A single adapter that knows all three can.

## 2. The setup is unusually favourable

All three existing datasets already lead every caption with a **distinct trigger and a distinct class word**:

| Subject | Trigger | Class word | Frames available |
|---|---|---|---|
| Kyle | `kyle_kx` | boy | 55 (v2) |
| Lindsey | `lindsey_kx` | girl | 32 |
| Ivy | `ivy_kx` | woman | 22 |

Two independent axes of separation — the token and the class — is the main defence against the failure mode
here, which is **identity bleed**: one subject's features leaking into another's prompt. The class words being
genuinely different (a boy, a girl, an adult woman) helps more than three arbitrary tokens would.

Every caption also already follows the Isolation Rule, so nothing had to be rewritten. The datasets were
merged as-is.

## 3. The balance decision

Kyle was capped at **33 of his 55** frames, giving **33 / 32 / 22** instead of 55 / 32 / 22.

Imbalance is what makes a multi-subject LoRA bleed: the majority subject becomes the model's default face, and
the minority subjects get whatever capacity is left. Kyle had 50% of the pool and Ivy 20%, which would have
made Ivy the weakest of the three for no good reason.

What was kept, and why:

- **all 11 full-body frames** — that coverage is exactly what `kyle_lora` v2 was built to add, and it is the
  scarcest thing in the pool
- **9 of 14 medium** — the band that was missing before v2
- **12 of 25 close-ups** — he had the most, and close identity is the easiest thing for a LoRA to learn

Nothing is lost by the cap: `kyle_lora_v2` stays on disk for Kyle-only work.

| | close-up | medium | chest-up | full body | total |
|---|---|---|---|---|---|
| Kyle | 12 | 9 | 1 | 11 | **33** |
| Lindsey | 12 | — | 7 | 13 | **32** |
| Ivy | 10 | 5 | 4 | 3 | **22** |

Ivy is the weak one on framing — only three full-body frames — so if anyone fails at distance it will be her,
and that is a dataset limit rather than anything about the merge.

## 4. Settings, and what changed from single-subject runs

| Setting | Single-subject | Here | Why |
|---|---|---|---|
| Rank | 32 | **64** | three identities need more capacity than one; rank is the cheapest place to buy it. Checkpoints roughly double, ~800 MB |
| Steps | 2000–2500 | **4000** | 87 frames across three subjects, against 55 of one |
| Learning rate | 1e-4 | 1e-4 | unchanged |
| Bucketing | `--use-aspect-ratio` | same | the three sets have different aspect ratios |
| Save every | 400–500 | **800** | five checkpoints, at ~800 MB each |

At roughly 0.2 it/s that is about five hours. It was queued to start automatically when `kyle_lora` v2
finished, since the GPU runs one job at a time.

## 5. How it will be judged

1. **Each subject alone**, at weight 1.0 and 0.85 — is the face actually right?
2. **Bleed** — does `kyle_kx boy` come out with Lindsey's or Ivy's features, and the reverse?
3. **Two subjects in one frame** — the thing that justifies the whole exercise.
4. **Family-Kyle against standalone `kyle_lora_v2`** — what does sharing the adapter cost a subject that has
   its own dedicated LoRA?

Test 4 is the one that decides whether this replaces the per-person LoRAs or sits alongside them.

## 6. Log

- **2026-09-30** — dataset merged (87 pairs, no new photographs, no caption rewrites) and training queued
  behind `kyle_lora` v2.

## Related pages
- [[kyle-lora-plan]]
- [[lindsey-lora-plan]]
- [[ivy-lora-plan]]
- [[blueprint-v2-research]]
