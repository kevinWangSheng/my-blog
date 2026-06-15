# C04 verification — first high-quality KB content batch

Date: 2026-06-15

## Scope

C04 published the first KB-derived RAG / Context Engineering batch:

- Essay already synced in C03 and used as C04 main essay: `site/src/content/essays/rag-as-evidence-chain.md`
- New note: `site/src/content/notes/retrieval-eval-before-answer-eval.md`
- New note: `site/src/content/notes/when-graphrag-is-worth-it.md`
- New link: `site/src/content/links/anthropic-contextual-retrieval.md`
- Toy/sample downlined without deletion: `site/src/content/notes/synced-agent-note.md` set to `visibility: "draft"`

## Source tracing

Review records:

- `docs/content-pipeline/reviews/rag-as-evidence-chain.md`
- `docs/content-pipeline/reviews/retrieval-eval-before-answer-eval.md`
- `docs/content-pipeline/reviews/when-graphrag-is-worth-it.md`
- `docs/content-pipeline/reviews/anthropic-contextual-retrieval.md`

Manifest staging:

- `docs/content-pipeline/manifests/rag-as-evidence-chain/`
- `docs/content-pipeline/manifests/retrieval-eval-before-answer-eval/`
- `docs/content-pipeline/manifests/when-graphrag-is-worth-it/`
- `docs/content-pipeline/manifests/anthropic-contextual-retrieval/`

## Commands run

```bash
pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/retrieval-eval-before-answer-eval
pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/retrieval-eval-before-answer-eval
pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/when-graphrag-is-worth-it
pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/when-graphrag-is-worth-it
pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/anthropic-contextual-retrieval
pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/anthropic-contextual-retrieval
pnpm --dir site build
```

## Verification results

- `content:check`: all 3 new staging packages passed with `ok: true`, `errors: []`, `warnings: []`.
- `content:sync`: wrote all 3 new content files into `site/src/content`.
- `pnpm --dir site build`: passed, generated 22 pages after downlining the fixture.
- Route checks:
  - `/essays/rag-as-evidence-chain/` generated.
  - `/notes/retrieval-eval-before-answer-eval/` generated.
  - `/notes/when-graphrag-is-worth-it/` generated.
  - `/links/` contains `Anthropic Contextual Retrieval` and the external Anthropic URL.
  - `/notes/synced-agent-note/` is no longer generated after `visibility: "draft"`.
- RSS checks:
  - RSS contains `RAG 不是向量库，而是证据链工程`.
  - RSS contains both new notes.
  - RSS no longer contains `Synced agent note`.
- Public leak check:
  - No `/Users/shenghuikevin/kb-vault` or `docs/content-pipeline` internal path found in the new public markdown/html checked.

## External freshness sources checked

- Anthropic Contextual Retrieval: https://www.anthropic.com/engineering/contextual-retrieval
- OpenAI File Search docs: https://developers.openai.com/api/docs/assistants/tools/file-search
- Google Cloud RAG Engine overview: https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview
- Microsoft GraphRAG docs: https://microsoft.github.io/graphrag/

## Conclusion

C04 acceptance is satisfied: first high-quality KB-derived essay is present, 3 companion notes/links are synced, the obvious sync fixture is downlined without deletion, and build/RSS/route/link/privacy checks passed.
