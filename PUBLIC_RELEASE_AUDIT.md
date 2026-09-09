# Public educational release audit

**Final owner authorization:** Visser Labs LLC confirmed ownership/licensing authority and approved MIT for original code/documentation, Copyright (c) 2026 Visser Labs LLC, and publication of this reviewed export at visser-labs/ai-treasure-hunt. See [LICENSE](LICENSE). Third-party software and data retain separate rights. Earlier pending-approval passages below are historical preparation records.


Prepared 2026-09-08. Status: **prepared locally; not published**. No version has demonstrated a robust trading edge. Decision D remains unchanged.

## Scope and preservation

Publish code, requirement files, reference mapping/correction record, frozen methodology/lock, prompts, research log and human-readable findings. Do not publish installed environments, Yahoo daily/minute caches, raw retrieval snapshots, generated runtime outputs, personal journals or temporary verification copies. They remain locally available; no research evidence was deleted.

The proposed Git-visible file set was inspected for usernames, absolute home-directory paths, common secret/key formats, private-key headers, binaries and oversized artifacts. No such findings were detected in that public set. The largest file is the research log (about 152 KB); the complete public set is about half a megabyte. This is a scoped pattern/content review, not a guarantee that automated secret detection finds every possible secret.

.gitignore excludes data/output payloads except empty .gitkeep markers, cookie/cache databases, .engine_dependencies, virtual environments, local editor/agent folders, private key and .env files, logs, ZIPs and .release_check. Git check-ignore confirmed exclusion of the actual local Yahoo snapshot, cookie cache, installed dependencies, personal journal and verification workspace. Do not force-add ignored files or upload a ZIP of the entire working directory. Use Git's reviewed nonignored file set. Existing .git metadata is local administration, not a file to upload as content; no remote or staged/tracked public files existed at review.

.gitattributes disables automatic checkout line-ending conversion because the frozen lock verifies exact bytes. Do not reformat frozen source/specification files or regenerate their hashes just to make a failing check pass.

## Reproducibility checks actually performed

- Created a separate copy using only Git-visible public files, with no original data, outputs, local dependency folder or private configuration.
- Created a separate Python 3.13 virtual environment and installed requirements-engine.txt. Yahoo transitive dependencies were explicitly pinned to the tested first-live-run environment after detecting that the earlier requirement list allowed version drift.
- pip check passed; yfinance 0.2.66 imported successfully.
- Public runtime integrity verification passed with 105 absent archive files explicitly reported. Missing required methodology/source is still an error; a dedicated tamper test confirms this. Present archive files remain hash-checked. Original strict archive verification was not changed.
- Public-copy frozen suite: 26 tests, 24 passed and two skipped because private archive evidence was absent. Engine/release suite: 11 tests, nine passed and two archive-dependent checks skipped. Thus 33 checks passed, four skipped, no failures in the clean public copy.
- An offline end-to-end engine run in the public copy processed all 50 synthetic stock series plus SPY successfully. No Yahoo network acquisition, real performance analysis or production journal update was performed for this release check.
- Original workspace tests passed with the archive present. Frozen historical source/specification/lock and prior research result artifacts remain unchanged. The current watchlist builder reproduces the already-authorized ordering from the saved scan.

Windows/Python 3.13 was executed. macOS/Linux commands were reviewed but not run on those platforms. Network availability, package wheels/build tools and unexpected exchange closures remain platform/operational limits. The isolated virtual environment was installed and checked locally, not tested on a new physical machine.

## Hidden assumptions resolved or disclosed

The live engine originally required all ignored historical Yahoo data through verify_freeze(). A separate src.release_integrity runtime verifier now checks all shipped frozen files/settings and any archive files present while permitting missing unpublished archives. The original verifier still protects full historical replication. This is a packaging/availability change, not a methodological relaxation: the equations, parameters, timing, universe, sectors and correction rules are unchanged.

The educational watchlist had previously been created as a one-off operation. src.build_watchlist now exposes that exact ordering as a repeatable separate command. No ranking score or journal membership is added. Historical plotting dependencies are separated into requirements-research.txt. No compiled environment is shipped.

The public repository can reproduce the environment, equations, synthetic checks and new research scans. It cannot guarantee bit-for-bit reproduction of historical results from fresh vendor downloads. The original archive is excluded; historical evaluator/report-writer scripts are preserved for inspection and depend on that archive. The earlier frozen acquisition path deliberately refuses overwrite after freeze. Do not describe it as a turnkey fresh historical download/reconstruction command. README and operating notes disclose these boundaries.

FROZEN_SPECIFICATION.md was reviewed for ATR seed/recurrence, OHLC adjustments, strict crossover inequalities, prior-20 exclusion, next-open entry, ten intervals, matched SPY and metrics. It remains unchanged; historical “next stage” wording belongs to its original preregistration context, not the current project status.

## License and attribution

THIRD_PARTY_NOTICES.md records the AGPL-3.0 crossover concept source, independent implementation, reviewed alternatives and installed library licenses. No third-party strategy engine or package source is vendored. Yahoo data rights are distinct from yfinance's software license, so raw data are not distributed. MIT is recommended for original code/documentation, but no LICENSE is applied without the owner's decision and copyright wording. If provenance review uncovers copied protected code, resolve it before publication.

## Remaining before GitHub publication

**Full-original-prompt gate (2026-09-09): PASSED after source restoration.** All 14 original prompts are now present in full and verified byte-for-byte against authoritative original attachments or conversation messages. No privacy redactions were required. The earlier unsuccessful summary audit remains below as a historical finding; it is superseded by the restoration verification.

1. Owner approves the project's license and copyright-holder wording; add LICENSE after that decision.
2. Owner chooses the public account/repository name and approves publication. No remote URL is invented, no repository created and no push performed.
3. Review the actual staged file list and final diff, including license/attribution and ignored-file exclusions; commit the reviewed educational release with line-ending preservation.
4. Publish that reviewed commit, verify the rendered links and clone instructions on GitHub, and share the real repository URL with viewers. Enable the host's secret-scanning protections where available.
5. Socrates Mode is now a complete pasteable interview instruction, reviewed in the subsequent documentation stage. It is not an installed or automatically activated agent. Verify its rendered instruction block in the published repository alongside the other documentation.

No promotion, optimization, V2, new historical comparison or additional live run was performed during public preparation.


## Final documentation review — Socrates Mode

The later authorized Socrates stage replaced the placeholder with a one-question-at-a-time interview, research brief and explicit approval gate. README and START_HERE now explain its use. Earlier log/prompt references to the placeholder remain as historical facts. All seven example domains, falsification and cheap-test criteria, verified open-source guidance and beginner steps are present. The complete file ends with “Same tools. New questions. Your treasure hunt.”

No new package, source change, engine run, data acquisition or public artifact beyond the requested documentation was introduced. Clean-environment test results above remain the prior executed results, not newly repeated tests. This review checks instruction consistency and public file hygiene, not whether every AI product will follow a prompt perfectly. Publication and license decisions remain with the owner.


## Prompt completeness audit — 2026-09-09

*Historical finding before restoration; resolved by the verification below.*

User requested verification that all 14 prompts were present in full and had not been shortened during documentation. Count check: PASS, entries 001–014 are present with no numbering gaps. Full-text check: NOT PASSED. Entries 001–007 explicitly say “faithful edited summary”; later entries are condensed instruction records, including 013–014 explicitly labeled edited instructions. The file's reader guide expressly says these are not verbatim transcripts. Thus the existing record cannot be described as all 14 original prompts in full.

Earlier public-preparation instructions permitted a full prompt or a sufficiently complete original instruction; that explains the labeled-summary format, but it does not satisfy the newly requested full-text standard. This check does not establish whether any additional accidental omissions occurred. A source-by-source comparison is required to establish that, rather than assuming a summary preserves every constraint.

Required pre-publication work: recover the original text for each prompt, preserve it in chronological numbered sections with results separate, label privacy-only redactions, and verify every section against the original conversation/attachment. If any original is unavailable, disclose the gap rather than manufacture exact wording or mark the audit passed. No original wording was reconstructed in this audit, and nothing was published.


## Publication fix — all 14 original prompts restored (2026-09-09)

This maintenance instruction is not a research prompt and has not been numbered as Prompt 15. Restored complete original submitted text to PROMPTS.md, with PROMPT NUMBER, CHAPTER / STAGE, PURPOSE, FULL ORIGINAL PROMPT — VERBATIM and a separate RESULT / DECISION for each entry.

Authoritative recovery: Prompts 1, 5, 7, 8, 11, 13 and 14 came from the original submitted text attachments; Prompts 2, 3, 4, 6, 9, 10 and 12 came from the original user-message records of this project conversation. All sources were available. No summary, paraphrase, grammar repair, reordered text or reconstruction from memory was used. Application-generated attachment-location wrappers were not treated as part of the submitted attachment content.

Each written original block was extracted from PROMPTS.md using its recorded UTF-8 byte count and compared to its source. All 14 match byte-for-byte, including whitespace and original line endings. Each entry records its source kind, original byte count, SHA-256 and status. Code fences and editorial metadata/results are outside the verified source text. The final verification table includes every prompt and states:

**ALL 14 ORIGINAL PROMPTS VERIFIED FOR PUBLICATION: YES**

Privacy review found no credentials, API keys, passwords, private filesystem paths or personal identifying information requiring removal in the original prompt bodies. Generic instructions discussing privacy are retained unchanged. **Privacy redactions: NONE. Sources required: NONE. Verified: 14 / 14.**

The prompt archive is READY for publication under the full-original-text requirement. Existing owner decisions on the project license, copyright wording, account/repository and actual publication authorization remain separate and outstanding. Nothing was published. Research code, frozen specifications, historical decisions/results and live journal/output files were not changed.

## GitHub setup approval package — 2026-09-09

See [GITHUB_PUBLICATION_REVIEW.md](GITHUB_PUBLICATION_REVIEW.md) for the current exact 51-file proposal (47 PUBLISH, four REVIEW), ignored categories, findings and unchecked human approvals. The earlier 50-file/size description is a historical audit snapshot. Current privacy pattern/content review passed with no redactions. All 14 original prompts remain unchanged. README's opening and START_HERE now explicitly invite different research questions and data sources; the exact Socrates on-ramp is prominent. THIRD_PARTY_NOTICES proposes MIT and Copyright (c) 2026 Visser Labs LLC for approval, without applying a license. Reference data-use rights and ownership/provenance remain human review items.

Publication setup is not Prompt 15. No research code, results or frozen definitions were changed, no market acquisition performed, and no GitHub remote created or push made. Technical preparation is READY FOR HUMAN APPROVAL. Actual publishing remains unauthorized.

## Current public packaging policy — supersedes earlier file lists

Publish ONLY the reviewed public export, never this original working tree: original documents retain private Yahoo correction facts for frozen integrity. Owner command: `python -m src.export_public <new-destination>`. This owner utility is not shipped to viewers. The export excludes both reference files, archives/output payloads, archive-specific tests/test_freeze.py and owner exporter; adds PUBLIC_RUNTIME_LOCK.json. Original prompts remain byte-identical. Vendor-price literals in historical prose are explicitly omitted; formulas and reported results remain unchanged.

Public runtime integrity checks shipped frozen code and separately hashed public documentary exceptions. No private sector/correction reads remain in the daily engine, even when those files exist locally. Missing sector metadata is UNAVAILABLE; invalid bars quarantine dependent calculations. Prior claims of reference inclusion and correction replay are historical descriptions superseded for public runs. Original FROZEN_LOCK is not regenerated. No LICENSE, remote or publication.

## Public packaging verification — executed 2026-09-09

The public copy had no reference/sectors.csv, reference/data_corrections.json or historical archives. Twenty formula/data tests passed; twelve engine/public-integrity tests passed with two historical-archive tests explicitly skipped. Sector retrieval failure and anomaly quarantine were tested synthetically. An actual Yahoo network scan then downloaded all 50 stocks plus SPY, retrieved all 50 current sector labels, and generated 3 V0 / 2 V1 signals on the latest completed date, 2026-09-08. Zero invalid bars and zero historical corrections were applied. Five version records were correctly retrospective, with no completed outcomes; all test outputs stayed isolated and are not shipped. Initial sandbox network access failed; the authorized network-enabled retry succeeded. This was packaging validation, not a new performance comparison.

The public export explicitly omits historical vendor literals in FIRST_LIVE_RUN.md, FROZEN_SPECIFICATION.md and RESEARCH_LOG.md. Links to excluded generated charts become explicit omission notes in the public copy; reported numbers are unchanged. Reported research returns, mathematical definitions and all 14 original prompts remain intact; prompts compare byte-for-byte. The private original specification, lock, references and historical results are preserved. Socrates Mode is unchanged and available without market data. Publish only the final export and its manifest, not the private source workspace or generated test outputs.

Clean Python 3.13 environment creation and installation from the public requirements succeeded; pip check reported no broken requirements. Initial restricted ensurepip execution failed; the authorized environment-creation retry succeeded. No dependencies or research parameters were changed. Public release is ready for final owner authorization, with ownership/account decisions outstanding.
