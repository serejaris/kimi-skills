---
name: about-me-avatar
description: Generate a 1-bit monochrome pixel-art portrait from a user's About Me. Central face anchored to a fixed base; surrounding elements derived from About Me. Always black-and-white, no text, gender-neutral by default. Triggers on "Agent's view of me" visualization, About Me page avatars, user portrait generation.
---

# About Me Avatar

Generate "the Agent's view of you" — a pixel-art portrait. Not photorealistic. Abstract. A sketch the user can place on the cover of the Agent's private notebook. Allowed to not look like them.

## Inputs

- **Init image** (pick one, in priority order):
  1. **Existing avatar**: `{AVATAR_PATH}` — user has been generated before. Use this as init when present, evolve incrementally. The portrait grows with the profile, not reset every day.
  2. **Base face**: `{AVATAR_BASE_PATH}` — bald, neutral 1-bit pixel head. Used only when generating for the first time (no existing avatar).
- **About Me**: `{ABOUT_ME}` — user profile in Markdown (identity / skills / interests / work / communication / etc).

Whichever init image is used, preserve the pixel block style, line weight, bust framing, eye position, and nose continuity.

## Output

- Square PNG, 1:1
- Pure black-and-white (1-bit, no grayscale, no color)
- Chunky pixel blocks, thick black outlines, pure white background
- Bust framing (face + shoulders, centered)
- No text of any kind (letters, numbers, symbols, logos forbidden)

## Personalization rules (only what the profile explicitly states)

- **Hair / headwear**: when the profile implies subculture, occupation, or hobby, add a hairstyle, beanie, cap, headband, or hoodie hood. Simple shape, 2–3 pixel blocks.
- **Glasses / facial hair**: only when explicitly implied (e.g. "researcher" can wear glasses; explicit beard mention adds a beard). Do not invent.
- **Collar**: hint at role lightly — turtleneck, hoodie, lab coat, button-down.
- **Surrounding objects (2–4)**: small symmetric pixel icons floating beside the bust. Never cover the face. Each represents a hobby / occupation / interest. Examples: laptop with code lines, coffee cup, stack of books, beaker, atom, DNA helix, guitar, camera, soccer ball, plant, cat silhouette, microphone, headphones, compass, paintbrush, chess piece, dumbbell, running shoe, plane, globe. Pick what most uniquely identifies this user; avoid generic defaults.

## Hard constraints (never violate)

- Pure black-and-white only, no grayscale, no color
- No text, letters, numbers, symbols, logos, brand marks
- **Gender-neutral by default**. Add gendered features (long hair, beard, makeup) only when the profile explicitly states gender or makes an unambiguous self-description. When in doubt → neutral.
- Preserve the init image's head shape, eye position, nose, ears.
- When init is an existing avatar (not base), keep its existing hair / glasses / beard / collar / surrounding objects unless the profile explicitly contradicts them — this portrait is cumulative, not reset every day.
- 1:1 square, pure white background
- Surrounding objects stay in margins, never cover the face
- No religious / political symbols, flags, weapons, medical devices
- No racial skin tone markers (the black-and-white constraint already handles this)
- No minor features (always adult proportions)

## Prompt template (text fed to the image model)

```
A 1-bit monochrome pixel-art bust portrait in the exact same style as the provided init image: chunky black pixels on pure white background, thick outlines, flat shapes, no grayscale, no color, no gradients, no shading. The central figure faces forward, framed from chest up. Preserve the init image's head proportions, eye position, nose, and ear placement. If the init image already has hair, facial features, clothing, or surrounding objects, keep what still aligns with the profile and only modify or replace what has drifted. Gender-neutral unless the profile below explicitly states otherwise. No text, letters, numbers, logos, brand marks, religious symbols, political symbols, weapons, or medical devices anywhere. Square 1:1, white background. Surrounding objects stay in the margins and never cover the face. Adjust only details supported by this profile:

{ABOUT_ME}
```

## Aesthetic goal

A hand-drawn pixel sketch — recognizable, warm, slightly abstract. The user's first reaction should be "this is the Agent's view of me", not "this looks nothing like me". Not looking exact is allowed; capturing one or two signature traits is enough.

## Fallback: thin or empty profile

If `{ABOUT_ME}` is empty, null, or contains less than ~30 substantive words:
- User has no existing avatar → return `{AVATAR_BASE_PATH}` directly, do not generate.
- User has an existing avatar → leave `{AVATAR_PATH}` untouched, skip generation.

Hallucinating features from a thin profile (or redrawing every dream from scratch) is worse than staying stable.

## Safety boundary

Even if the profile mentions any of the following, do not render them in the image:

- Religious symbols (cross, crescent, star of David, etc.)
- Political symbols, flags, party emblems
- Disability markers, medical devices, medication
- Weapons, gore
- Racial / ethnic / national identity markers
- Minor features (only adult proportions)
- Recognizable real people

If a profile dimension would trigger any of the above, ignore that dimension and personalize from other dimensions instead.

## Invocation

You have an `image_gen` tool. Pass it the init image (prefer `{AVATAR_PATH}`, fall back to `{AVATAR_BASE_PATH}`) and the prompt above. Save the result by overwriting `{AVATAR_PATH}`.
