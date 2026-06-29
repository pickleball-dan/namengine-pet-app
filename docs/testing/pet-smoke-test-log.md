# NamEngine Pet Smoke Test Log

Use this as the readable product/testing record. Keep the CSV files as backup data, but make decisions from these summaries.

## 2026-06-28 - Early Pet smoke test, rounds 1-2

Data backups:

- `namengine_pet_smoke_test_20260628-171247.csv`
- `namengine_pet_smoke_test_20260628-171732.csv`

Scope:

- Curated and original Pet naming paths.
- Sortable labels: `PET001`-`PET011`, `Pet Curated`, `Pet Original`.
- Round 1: 76 total rows, 56 curated names, 20 original names.
- Round 2: same format, rerun after first analysis request.

Summary:

- Dog was the strongest lane. Names like `Toby`, `Milo`, `Rory`, `Dex`, and `Jude` showed the callability/acoustic tuning working.
- Horse was mostly strong. `Atlas`, `Hudson`, `Sierra`, `Cedar`, `Flint`, and `Dakota` fit steady outdoor/barn energy.
- Bird was directionally good, especially when names were bright, repeatable, and musical: `Zazu`, `Echo`, `Koda`, `Lyric`, `Bixby`, `Jazz`, `Coda`, `Tempo`, `Aria`.
- Cat could support mythic/elegant names, but the first pass skewed too ornate or invented: `Nyxara`, `Mistra`, `Vespera`, `Isolde`, `Thalia`.
- Rabbit could support romantic or mythic names, but the first pass was too fancy/elegant-human: `Aurelia`, `Celandine`, `Amoret`.
- Reptile overcorrected into deity, demon, religious, and heavy myth names: `Azazel`, `Vishnu`, `Sekhmet`, `Brontes`.
- Original mode was acceptable as a more exploratory path, but still needed pet-wearability guardrails. Better examples included `Branlo`, `Kelvo`, `Farlo`, `Renko`; weaker examples included `Zyphra`, `Meloq`, `Vaelor`, `Trilix`.

Decision:

- Keep stronger acoustic/callability weighting for dogs.
- Allow cats to be mythic/elegant, but avoid over-ornate or invented fantasy shapes.
- Allow rabbits to be soft mythic/romantic, but keep them simple and gentle.
- Make birds less mythic and more bright, repeatable, social, and musical.
- Make reptiles more visual/personality/texture/color driven, and avoid deity, demon, or religious names unless requested.
- Penalize original-name shapes that read too fantasy/app-name, especially `ae`, `zy`, `x`, `q`, `-lor`, and `-ian`, unless the user's request clearly calls for that.

Engine changes made:

- `94ca29d Add species-weighted Pet naming logic`
- `90c2330 Tighten Pet species guardrails`

Current testing rule:

- Smoke CSVs are backup data.
- Summaries are the primary decision artifact.
- Each summary should connect data signals to engine changes, including commit IDs when changes are made.
