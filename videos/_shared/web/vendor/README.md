# Vendored web assets (HyperFrames beats)

**Name:** web-vendor
**Description:** The animation library and the font every HyperFrames
composition loads, checked in so no render fetches from a CDN or Google
Fonts.
**When to use:** any HyperFrames beat or prototype. Link this folder into
the composition folder as `vendor/` (a symlink; HyperFrames rejects `../`
paths above the project root) and load `vendor/gsap.min.js` and
`vendor/Inter-ExtraBold.woff2`. How, in `agents/beat-brief-hyperframes.md`.
**How it works:** plain files, pinned by version and sha256 below.
`tests/test_hyperframes_offline.py` fails if a file is missing or its hash
changes. To upgrade: fetch the new version the same way, replace the file,
update the table and the hash in the same commit.

| File | What | Version | License | Source | sha256 |
|---|---|---|---|---|---|
| `gsap.min.js` | GSAP core, UMD build (defines `window.gsap`) | 3.14.2 | GSAP Standard "no charge" license | `dist/gsap.min.js` from the npm tarball `gsap@3.14.2` (`npm pack gsap@3.14.2`), byte-identical to the jsDelivr copy the scaffold loaded | `c174bfce53a729418d57a8ad8625e7247c793a22fef8e2851e3cfa3de9cd8280` |
| `Inter-ExtraBold.woff2` | Inter, weight 800, full character set | Inter 4.1 (npm `inter-ui@4.1.1`) | SIL OFL 1.1 | `web/Inter-ExtraBold.woff2` from `npm pack inter-ui@4.1.1` | `6f75025856f8db1b2186e9cb89be9de9894932c8b7b20f4df5e65916ff714e34` |
| `Inter-LICENSE.txt` | Inter's OFL 1.1 license text | 4.1 | SIL OFL 1.1 | `LICENSE.txt` from the same tarball | `cc36dd53b88f8c7f138b9708e0c4b598816e4e52c7e252859e67e1e7edbcf117` |

Only weight 800 is vendored because it is the only weight the prototypes
use (all text and captions are `font-weight: 800`). Add another weight
from the same package version when a beat needs it, with its row here.

## Diligence (2026-10-03)

- **gsap@3.14.2.** npm registry: maintainer `greensock <info@greensock.com>`,
  repository `github.com/greensock/GSAP`, homepage gsap.com, ~6.7 M
  downloads a week, 3.14.2 published 2025-12-12 (latest is 3.15.0; we pin
  3.14.2 because that is what the HyperFrames 0.8.115 scaffold loads and
  what the prototypes were tuned on). The tarball has no separate license
  file; the license notice is the header of `gsap.min.js` itself, kept
  intact.
- **inter-ui@4.1.1.** The npm package named in Inter's own README
  (github.com/rsms/inter, "npm: inter-ui"); maintained by Philip Belesky,
  `author` field Rasmus Andersson, OFL-1.1, ~260 K downloads a week,
  4.1.1 published 2025-06-22. Its
  changelog says 4.1.0 updated the files to the Inter 4.1 release, which is
  the latest rsms/inter release (v4.1, 2024-11-16). `@fontsource/inter` is
  popular but is not listed by the Inter project, so it was not used.
- Nothing installed: both tarballs were fetched with `npm pack` into a
  scratch directory and only the files above were copied. No
  `package.json` gained a dependency.

## License terms in short

- **GSAP Standard "no charge" license** (gsap.com/standard-license,
  effective 2025-04-30, owned by Webflow): free for commercial and
  non-commercial use on any site, app or digital interface, all plugins
  included. Restriction: GSAP may not be used in a product that lets users
  build visual animations without code in competition with Webflow, and
  proprietary notices must not be removed. No attribution requirement
  beyond keeping the notice. Rendering our own videos is ordinary use. It
  is not an open-source license; Webflow can change it for future
  versions, so do not upgrade without re-reading it.
- **SIL Open Font License 1.1** (Inter): use, embed and redistribute
  freely, including in commercial work; keep the license with the font
  files; the font may not be sold on its own.
