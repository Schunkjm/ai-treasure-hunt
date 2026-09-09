# Third-party notices and license decision

**Final owner authorization:** Visser Labs LLC confirmed ownership/licensing authority and approved MIT for original code/documentation, Copyright (c) 2026 Visser Labs LLC, and publication of this reviewed export at visser-labs/ai-treasure-hunt. See [LICENSE](LICENSE). Third-party software and data retain separate rights. Earlier pending-approval passages below are historical preparation records.


Reviewed for public preparation on 2026-09-08. No third-party package source, wheel, environment, cookie database or Yahoo cache is included in the proposed public file set. Dependencies are installed separately and retain their own notices. This is a provenance record, not a grant of rights over third-party code or market data.

## Concept and source review

| Project | License / source | What was used | Attribution and reuse boundary |
| --- | --- | --- | --- |
| [kernc/backtesting.py](https://github.com/kernc/backtesting.py) | [AGPL-3.0](https://github.com/kernc/backtesting.py/blob/master/LICENSE.md) | SMA crossover Quick Start and strict crossover concept; independent pandas implementation | Retain conceptual attribution. No source was copied or framework imported. If copying/modifying upstream code later, follow its AGPL requirements, including applicable source and notice obligations; do not assume this project's eventual license covers it. |
| [pmorissette/bt](https://github.com/pmorissette/bt) | MIT, recorded at original review | Momentum candidate, rejected by human override | Reviewed only; no code incorporated. Preserve review history. |
| [bukosabino/ta](https://github.com/bukosabino/ta) | MIT, recorded at original review | Indicator concepts considered | Reviewed only; no package or implementation copied. |
| [peerchemist/finta](https://github.com/peerchemist/finta) | LGPL-3.0, recorded at original review | Squeeze concept considered | Reviewed only; not a dependency. |
| [mementum/backtrader](https://github.com/mementum/backtrader) | GPL-3.0, recorded at original review | Alternative SMA example considered | Reviewed only; not incorporated. |

Other screened repositories and uncertain/no-license cases remain in RESEARCH_LOG.md. Their code was not included. Historical popularity estimates are dated observations, not current counts or evidence of trading profitability.

## Installed dependencies

| Project | URL / license | Use and notices |
| --- | --- | --- |
| yfinance | [Apache-2.0](https://github.com/ranaroussi/yfinance/blob/main/LICENSE.txt) | Yahoo acquisition; installed unchanged. Preserve license/copyright and applicable NOTICE if redistributing the package. |
| exchange_calendars | [Apache-2.0](https://github.com/gerrymanoim/exchange_calendars/blob/master/LICENSE) | XNYS calendar; installed unchanged; upstream includes Quantopian attribution. Preserve license/notices if bundled. |
| pandas | [BSD-3-Clause](https://github.com/pandas-dev/pandas/blob/main/LICENSE) | Tables/rolling calculations. Retain copyright, terms and disclaimer when redistributing. |
| NumPy | [BSD-3-Clause and bundled-component notices](https://github.com/numpy/numpy/blob/main/LICENSE.txt) | Numerical operations. Distribution wheels may include additional component licenses; retain them if bundled. |
| Matplotlib | [Matplotlib license and component notices](https://github.com/matplotlib/matplotlib/blob/main/LICENSE/LICENSE) | Optional historical charts, not needed by the daily engine. Preserve its license and bundled notices if redistributed. |

requirements-engine.txt pins the direct environment requirements, including calendar dependencies (pyluach, toolz, korean-lunar-calendar, tzdata, pytz, python-dateutil and six). The Yahoo client transitive dependencies are also pinned to the tested live-run environment. Plotting tools bring additional transitive dependencies. This table is not an exhaustive bill of materials for redistributing an installed environment. This repository distributes requirement files, not those packages; installers supply the packages' license files. A future binary/container distribution needs a complete dependency-notice review.

## Market data

A software package license does not grant Yahoo market-data redistribution rights. Download your own data subject to the provider's terms. Raw daily/minute snapshots, retrieval metadata, personal journals and runtime caches are excluded. The public research reports preserve results and methodology; they do not supply a licensed replacement for a market-data feed. Exact historical snapshot reproduction remains limited without the retained original archive.

## Recommended project license — approval pending

Recommend **MIT** for the independently written project code and original documentation, subject to the owner's confirmation of rights and desired copyright attribution. It is a simple permissive option suited to educational adaptation. **No LICENSE file has been silently applied.** Before publication, the owner must approve the license and copyright-holder wording and resolve any uncertainty about third-party source provenance. Until then, the preparation is not a claim that this repository already grants open-source reuse rights.

The upstream AGPL code is not being relicensed. If review later finds copied protected source, resolve its obligations before publishing rather than placing an MIT label over it. The research record states independent implementation and inspection found no vendored strategy engine.

## Specific owner decision requested — 2026-09-09

Recommend MIT for our original code and associated educational documentation, including original prompts to the extent the owner can license them. A single license makes mixed prose/code examples simpler to reuse. MIT permits reuse, modification and commercial distribution, with preservation of its copyright and permission notice; it supplies an as-is disclaimer. It does not require publication of downstream modifications. See the [official MIT text](https://opensource.org/license/mit).

Separate MIT code / CC BY 4.0 prose is a reasonable alternative if distinct educational-content attribution is desired: [Creative Commons overview](https://creativecommons.org/cc-licenses/). It introduces two scopes and additional attribution/change-marking administration. Recommend the single MIT approach here, not both alternatives simultaneously. No license has been applied.

Proposed notice for approval: **Copyright (c) 2026 Visser Labs LLC**. The year follows this project's documented creation in 2026; the entity name was supplied by the owner. Human review must confirm that Visser Labs LLC owns or is authorized to license the original contributions, including submitted prompts. This proposal does not establish ownership or copyrightability of every AI-assisted element.

Source inspection and the recorded development provenance found no copied/vendored third-party strategy implementation or imported copyleft strategy framework. The mathematical crossover concept is attributed; this is not a claim to relicense [upstream AGPL source](https://github.com/kernc/backtesting.py/blob/master/LICENSE.md). No conflict was identified for the proposed source-only release, subject to owner confirmation of provenance. Dependencies keep their own licenses and are installed separately. Existing source/license URLs above remain the attribution record; historical popularity is adoption evidence only.

Human review also covers the small factual Yahoo-derived sector mapping/correction reference records. They are proposed for auditability, not as a market-data feed; MIT cannot grant rights in third-party data. No raw Yahoo archives or generated market tables are proposed for publication.

## Public reference-data removal — current policy

Neither reference/sectors.csv nor reference/data_corrections.json is distributed. Public documents explicitly omit historical Yahoo correction values. Original sectors came from Yahoo/yfinance; public runs retrieve optional current labels into ignored local outputs. No official GICS data or private archive is redistributed. Runtime data remains subject to provider terms, not MIT.

The owner provisionally approved MIT for original code/documentation, ai-treasure-hunt and Copyright (c) 2026 Visser Labs LLC, subject to ownership confirmation. THIRD_PARTY_NOTICES.md is approved for inclusion. No LICENSE is applied; publication remains unauthorized.

frozendict 2.4.6 is LGPL-3.0; certifi is MPL-2.0. They are separately installed, not vendored, and do not relicense our independent application. Bundling requires applicable copyleft and notice compliance. Other pinned support libraries: beautifulsoup4, curl_cffi, peewee, platformdirs, cffi, charset-normalizer, soupsieve, urllib3 (MIT); multitasking, requests (Apache-2.0); idna, protobuf, websockets, pycparser, toolz (BSD-3-Clause); typing-extensions (PSF-2.0); pyluach, korean-lunar-calendar, pytz, six (MIT); python-dateutil (Apache/BSD portions); tzdata (Apache package, underlying timezone-data provenance). Preserve supplied component notices if distributing packages. No environment is shipped. Earlier proposals to include Yahoo reference files are superseded by this section.
