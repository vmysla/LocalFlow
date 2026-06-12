# Decision Records

Append a new record whenever a non-obvious architectural or product
decision is made. Newest records at the top.

## 2026-05-14 — Skip full LinkedIn-skill onboarding; bootstrap config from the article + 4-question quickstart

**Context:** The `write-linkedin-post` skill prescribes a 16-question onboarding (5 batched `AskUserQuestion` calls) when `./linkedin/config/` is missing. User asked for a LinkedIn post about an article they had just written and clearly wanted a fast turnaround, not a 20-minute config dance.
**Decision:** Asked one consolidated 4-question batch (profile, audience, length, CTA), inferred the remaining config (voice, topics, hooks, banned-words, formatting) from the article itself, and wrote all 8 config files plus the draft in one pass.
**Rationale:** The article is 19k words of the user's own voice — a stronger style reference than any answer to "describe your voice in three adjectives" would have produced. The four questions cover the irreversible choices (whose name is on it, who it's for, how long, where the link goes); the rest is editable.
**Consequences:** Config files now exist and will be reused for future posts without re-onboarding. If the inferred voice/topics don't match what the user wants long-term, they can edit any file in `linkedin/config/` and the next run picks up changes. Cost: future posts may need a "redo voice / change topics" refinement turn.
**Related:** `linkedin/config/*.md`, `linkedin/drafts/2026-05-14-1024-wispr-moat-152-lines.md`, change.log 2026-05-14 entry.

## 2026-05-14 — Launch article framed around 5-monitor agent workflow, not pure tech comparison

**Context:** Article needed a hook beyond "I cloned a SaaS product over lunch." User requested an opener built on their actual daily practice: yelling at AI from 5 monitors + phone running 24/7 parallel Claude Code / Codex sessions, with voice dictation as the steering wheel.
**Decision:** Open with the morning scene; treat voice dictation as load-bearing infrastructure for an agent-orchestration workflow, not as a productivity nicety. Use the build story as the second beat, the competitive table as the third, the privacy/subprocessor section as the punchline.
**Rationale:** The thesis ("the moat is gone") is more persuasive coming from someone whose livelihood depends on the tool than from a hobbyist. The workflow framing also positions LocalFlow's offline + zero-third-parties profile as a hard requirement, not a preference.
**Consequences:** Article is longer and more personal — better for Substack/Medium than a dry teardown, but less neutral. Locks the framing to this specific author's voice; not re-usable as generic documentation.
**Related:** requirements.md §Features → "Launch article"; change.log 2026-05-14 entry.

## 2026-04-20 — Source-available license rather than MIT

**Context:** The underlying Whisper model is MIT, and freeflow/OpenWhispr both went MIT. Default expectation for a "free local alternative" is permissive.
**Decision:** Custom license — free for personal/educational/research, commercial use requires written permission.
**Rationale:** Discourages another vendor from wrapping LocalFlow's installer and reselling it at $X/mo. The point of the project is to undercut that motion, not to seed it.
**Consequences:** Loses some goodwill from purist OSS audiences; cannot be casually bundled into other apps. Users who want a permissively-licensed equivalent can use OpenWhispr.
**Related:** `LICENSE.md`, README.md.

## 2026-04-20 — One-file architecture, no abstraction

**Context:** The whole product is "record while a key is held, transcribe, paste." It would be trivial to split into modules (recorder, transcriber, paster, config).
**Decision:** Keep everything in a single `ptt.py` (~152 lines). All tunables are constants at the top.
**Rationale:** The thesis is that this is a weekend hack, not a framework. Splitting into modules implies more sophistication than the product warrants and makes extension harder, not easier — readers can fork one file and rewrite `_transcribe_and_paste` in five minutes.
**Consequences:** No unit tests yet; concurrency lives in a module-level `_state` dict guarded by a lock, which is fine for one process but would not survive growth.
**Related:** `ptt.py`, README.md "How it works".
