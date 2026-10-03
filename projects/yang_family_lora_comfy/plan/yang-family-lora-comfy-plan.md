# Yang Family LoRA for ComfyUI

**Summary**: Get the three-subject family LoRA working in ComfyUI. Training it there is blocked on Apple Silicon, so the plan converts the existing Draw Things adapter to safetensors instead.

**Sources**: measured on this machine 2026-10-02; upstream issue trackers cited inline.

**Last updated**: 2026-10-02

---

## The goal

`kyle_kx boy`, `lindsey_kx girl` and `ivy_kx woman` rendering in ComfyUI from a single adapter,
the same way they already do in Draw Things. See [[model-storage-locations]] for where the weights
live.

## Why this is not simply "train it again"

The obvious plan — point a ComfyUI-native trainer at the 87-pair dataset and get safetensors out —
does not work on this machine. Checked 2026-10-02:

| trainer | FLUX.2 klein 9B | Apple Silicon |
|---|---|---|
| [Fizgig](https://github.com/shootthesound/Fizgig) | supported, LoRA from 10 GB VRAM | **Windows/Linux, NVIDIA or AMD only** |
| [ai-toolkit](https://github.com/ostris/ai-toolkit/issues/871) | supported | **MPS issue closed "not planned"** |
| [musubi-tuner](https://github.com/kohya-ss/musubi-tuner/issues/860) | open klein 9B error | — |

The ai-toolkit report is the most thorough: six configurations, none converging. NaN loss with
cached text embeddings, OOM on fp16 even with gradient checkpointing, and loss oscillating in a
0.45–0.56 band rather than descending. Suspected cause is MPS gradient precision plus torchao
kernels with no Triton on Metal. No maintainer response; closed as not planned.

This is consistent with what is already recorded in [[apple-silicon-inference]]: Metal is a
second-class training target, and FP8 — the thing that makes klein training cheap elsewhere —
does not exist here at all.

## So: convert, don't retrain

The adapter already exists and took 9 h 22 m to train. Converting it is local, free, costs no
privacy, and reuses that work. Three facts make it viable, all verified rather than assumed:

**1. The weights are plain float32.** Draw Things `.ckpt` files are SQLite databases, not PyTorch
checkpoints — but unlike the quantized base models, a trained LoRA is not quantized:

```
564 tensors, single datatype, every dim product x 4 == byte length (564 match, 0 mismatch)
__dit__[t-c_q-0-0]__down__   dim=[32, 4096]
__dit__[t-c_q-0-0]__up__     dim=[4096, 32]
```

**2. The layer naming parses completely.** All 564 names fit one pattern, and the architecture
falls straight out of it:

```
8 double blocks  (0..7)    c_q c_k c_v c_o + c_gate_proj c_up_proj c_down_proj   text stream
                           x_q x_k x_v x_o + x_gate_proj x_up_proj x_down_proj   image stream
24 single blocks (8..31)   x_q x_k x_v x_o + x_w1 x_w2 x_w3                      SwiGLU MLP
x_embedder, linear                                                               in / out
```

**3. ComfyUI takes `diffusion_model.`-prefixed keys** mapped directly onto the model's own state
dict, so there is a concrete target rather than a guess at some trainer's convention.

## The one real problem: fused qkv

Draw Things stores `x_q`, `x_k`, `x_v` separately. klein fuses them:

```
Draw Things   __dit__[t-x_q-0-0]__{down,up}__      three rank-32 pairs
klein         double_blocks.0.img_attn.qkv.weight  one fused matrix
```

This is solvable **exactly**, with no SVD and no loss. The three deltas occupy disjoint row ranges
of the fused matrix, so:

```
down_fused = [ Dq ; Dk ; Dv ]                 (96 x in)
up_fused   = [ Uq  0   0  ;
               0   Uk  0  ;
               0   0   Uv ]                   (3*out x 96)
```

reproduces the stacked delta identically at rank 96. Single blocks fuse further — klein's
`linear1` carries qkv *and* the MLP input — so the same construction extends with more blocks on
the diagonal.

## Steps

1. **Extract** — read the 564 tensors out of SQLite with `numpy.frombuffer`, honouring the `dim`
   blob for shape. Already proven to work.
2. **Map** — Draw Things layer name to klein state-dict key, per block type.
3. **Fuse** — build the block-diagonal qkv (and `linear1`) pairs as above.
4. **Emit** — one safetensors file of `diffusion_model.*.lora_{down,up}.weight` keys.
5. **Verify** — load in ComfyUI against `flux-2-klein-9b.safetensors` and render `lindsey_kx girl`
   at weight 1.0. The test is whether Lindsey's face comes back, against a no-LoRA control.

Step 5 is the only one that can fail quietly: a LoRA whose keys do not match is **silently
ignored** by ComfyUI, which looks identical to a LoRA that changed nothing. The control column is
not optional — the same trap is already recorded for `draw-things-cli` in [[log]].

## If conversion fails

Renting a GPU is the fallback, and it carries a cost the local path does not: the dataset is 87
images of Kevin's children. Those raw photographs are deliberately git-ignored in a public repo on
the principle that consent to train on a face is not consent to publish the face. Uploading them
to a rented machine is the same decision in a different form, and it is Kevin's to make, not a
default to fall into.

## Related pages
- [[model-storage-locations]]
- [[apple-silicon-inference]]
- [[character-consistency]]
- [[headless-cli-pipeline]]
