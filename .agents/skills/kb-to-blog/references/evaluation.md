# KB to Blog evaluation

Use this reference when deciding whether a KB-derived draft can enter human review.

## Pass/fail gates

A draft is blocked if any item is true:

- It copies KB prose without public framing or editorial restructuring.
- It exposes secrets, private markers, forbidden-publish markers, private person/company data, or internal paths in public prose.
- It fabricates project results, customer/user feedback, public repo/demo links, external endorsement, or personal experience not supported by the source.
- It makes fast-moving model/vendor/protocol/benchmark/security claims without refresh or explicit uncertainty.
- It is not legible as one of the blog content types: essay, note, log, link, or project.

## Rubric

Score each item 0-2. Below 8/12 should not enter human review.

| item | 0 | 1 | 2 |
|---|---|---|---|
| Public value | Internal record only | Topic exists but reader payoff is vague | Stranger can name the judgment, method, or map they gained |
| Source grounding | Source unclear | Source exists but claims are not traced | Key claims trace to KB paths and refreshed sources when needed |
| Rewrite maturity | KB copy/paste | Partial rewrite | Public title, structure, context, and transitions are complete |
| Safety/privacy | Clear risk present | Risk unresolved | No secrets/private markers/personal data/fabricated claims |
| Freshness | Outdated or unstated | Some fast-moving facts need refresh | Fast-moving facts refreshed or explicitly scoped by date |
| Blog fit | Off-topic | Weakly related | Fits AI learning, agent systems, project practice, or knowledge workflows |

## Adversarial review prompt

```text
Use $kb-to-blog to adversarially review this KB-derived blog review draft.

Check:
1. Is it a public blog draft direction, or just KB material copied into a template?
2. Are the source paths and key claims traceable?
3. Are there secrets, private markers, forbidden-publish markers, private data, or internal paths exposed in public prose?
4. Does it fabricate achievements, public links, project results, customer/user feedback, or external endorsement?
5. Do model/vendor/protocol/benchmark/security claims need current official/primary source refresh?
6. Does it fit the blog's AI learning / agent systems / project practice / knowledge workflow identity?

Output:
- blockers:
- non-blocking risks:
- recommended edits:
- should enter human review: yes/no
```
