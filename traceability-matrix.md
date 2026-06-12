# Traceability Matrix

Links every tracked requirement to the prompt that produced it, the
implementation artifacts, the decision record, the changelog entry, and
the verification (tests / review).

| Requirement | Prompt excerpt | Implementation | Decision | Changelog | Verification |
|-------------|----------------|----------------|----------|-----------|--------------|
| Push-to-talk transcription | (2026-04-20) initial build — "hold a key, speak, release, paste" | `ptt.py` | 2026-04-20 one-file architecture | 2026-04-20 v0.1.0 Added | Manual: hotkey → text in focused app |
| Clipboard preservation | (2026-04-20) "restore previous clipboard after paste" | `ptt.py:_paste` | — | 2026-04-20 v0.1.0 Added | Manual: copy text A, dictate, paste — clipboard back to A |
| One-line installer | (2026-04-20) "curl \| bash, set up venv, launch" | `install.sh`, `requirements.txt` | — | 2026-04-20 v0.1.0 Added | Manual: fresh machine → working install |
| Permissions guidance | (2026-04-20) README polish — mic + accessibility prompts | `README.md` | — | 2026-04-20 v0.1.0 Added | Manual: first launch triggers macOS prompts |
| Source-available license | (2026-04-20) custom license | `LICENSE.md` | 2026-04-20 source-available license | 2026-04-20 v0.1.0 Added | Visual review |
| Launch article | (2026-05-14) "write a fancy article I can post on Substack or Medium…" + follow-up on Wispr Flow subprocessor footprint + opener on 5-monitor agent workflow | `articles/wispr-flow-killer.md` | 2026-05-14 launch article framing | 2026-05-14 Added (Unreleased) | Self-review; pricing claims cite vendor pricing pages; privacy claims cite docs.wisprflow.ai |
| LinkedIn distribution config | (2026-05-14) "Create me a linkedin post about this article." + 4-question quickstart (profile/audience/length/CTA) | `linkedin/config/company.md`, `audience.md`, `voice.md`, `topics.md`, `hooks.md`, `ctas.md`, `formatting.md`, `snippets.md` | 2026-05-14 skip-full-onboarding bootstrap | 2026-05-14 Added (Unreleased) | User edits any file in `linkedin/config/` to refine; next post run picks up changes |
| LinkedIn post — Wispr moat | (2026-05-14) "Create me a linkedin post about this article." + (2026-05-14) "change the post title to I replaced a $144/year app in <2 hours. (keep bold formatting)" | `linkedin/drafts/2026-05-14-1024-wispr-moat-152-lines.md` | 2026-05-14 skip-full-onboarding bootstrap | 2026-05-14 Added + Updated (Unreleased) | char_count 775 (≤800 target); hook ≤12 words; payoff above ~210 fold; two link CTA; pending user review |
