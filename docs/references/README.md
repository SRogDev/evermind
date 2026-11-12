# References

How to record literature for Evermind. A full literature review is
**not** required yet — this file defines the format and records the
verified sources used during repository creation. **Do not fabricate
citations.** Add only sources that were actually located and verified;
distinguish primary research from secondary commentary.

## Recording format

Each entry records:

- **Title**
- **Authors**
- **Year**
- **Venue / preprint** (journal, conference, arXiv, or official project
  page)
- **Canonical URL / DOI / arXiv identifier**
- **Relevant method** — what the work does, in one or two sentences
- **Supported claim** — which Evermind claim or question it bears on
- **Limitations** — what it does not show
- **Relevance to Evermind** — why it is here

## Verified sources

### 1. SmolLM3 technical report (primary source for the base model)

- **Title:** SmolLM3: smol, multilingual, long-context reasoner
- **Authors:** Bakouch, Elie; Ben Allal, Loubna; Lozhkov, Anton; Tazi,
  Nouamane; Tunstall, Lewis; Patiño, Carlos Miguel; Beeching, Edward;
  Roucher, Aymeric; Reedi, Aksel Joonas; Gallouédec, Quentin; Rasul,
  Kashif; Habib, Nathan; Fourrier, Clémentine; Kydlicek, Hynek;
  Penedo, Guilherme; Larcher, Hugo; Morlon, Mathieu; Srivastav,
  Vaibhav; Lochner, Joshua; Nguyen, Xuan-Son; Raffel, Colin; von
  Werra, Leandro; Wolf, Thomas
- **Year:** 2025
- **Venue / preprint:** Hugging Face blog / technical report (citation
  as published on the official model card)
- **Canonical URL:** <https://huggingface.co/blog/smollm3>
- **BibTeX (as given on the model card):**

  ```bibtex
  @misc{bakouch2025smollm3,
    title={{SmolLM3: smol, multilingual, long-context reasoner}},
    author={Bakouch, Elie and Ben Allal, Loubna and Lozhkov, Anton
      and Tazi, Nouamane and Tunstall, Lewis and Patiño, Carlos Miguel
      and Beeching, Edward and Roucher, Aymeric and Reedi, Aksel Joonas
      and Gallouédec, Quentin and Rasul, Kashif and Habib, Nathan and
      Fourrier, Clémentine and Kydlicek, Hynek and Penedo, Guilherme
      and Larcher, Hugo and Morlon, Mathieu and Srivastav, Vaibhav and
      Lochner, Joshua and Nguyen, Xuan-Son and Raffel, Colin and von
      Werra, Leandro and Wolf, Thomas},
    year={2025},
    howpublished={\url{https://huggingface.co/blog/smollm3}}
  }
  ```

- **Relevant method:** 3B-parameter decoder-only Transformer (GQA,
  NoPE), pretrained on 11.2T tokens, 64k training context with YaRN
  extrapolation to 128k.
- **Supported claim:** SmolLM3-3B-Base is a documented, open-weight,
  ~3B starting point with the architecture and training information
  Evermind needs to plan adaptation.
- **Limitations:** The report documents the base model as trained; it
  says nothing about continuous event-stream operation, bounded state,
  or silence/signal behavior — those are Evermind's research questions,
  not the report's findings.
- **Relevance to Evermind:** Primary source for the initial model
  candidate (model card: <https://huggingface.co/HuggingFaceTB/SmolLM3-3B-Base>;
  upstream project: <https://github.com/huggingface/smollm>).

## Sources not yet added

No other literature is cited in this foundation phase. Candidate
families named in `architecture/candidate-architectures.md` (recurrent
memory mechanisms, state-space approaches, gated delta-rule
architectures, hybrid attention/recurrent designs) are **research
directions for literature review, not cited claims** — their primary
sources belong here only once located and verified, using the format
above.
