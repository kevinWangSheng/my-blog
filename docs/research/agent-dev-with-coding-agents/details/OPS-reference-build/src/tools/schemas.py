"""Strict JSON Schema (inputSchema) definitions for expense-agent's three tools.

These dicts are passed verbatim to the Claude Messages API `tools` array
(`client.messages.create(tools=ALL_TOOLS)`). All three set `strict: True` so the
API hard-validates tool inputs against the schema before your handler runs.

Two API-level invariants are enforced here, both load-bearing:

1. Tool `name` must match the official regex `^[a-zA-Z0-9_-]{1,64}$`. A literal
   dot is OUTSIDE that character class, so a name like "expense.ocr_extract"
   returns a 400 invalid_request_error before any handler runs. We use
   underscore namespacing (expense_ocr_extract / expense_fx_rate /
   expense_post_ledger_entry).

2. Strict-mode schema rules: top-level `additionalProperties: false`, every
   property listed in `required`, and only supported JSON Schema keywords.
   `format` on a string IS supported (date/date-time/uuid/...), but
   numeric/string size constraints (minLength/minimum/pattern) are NOT.
   [推断: the exact keyword subset Anthropic supports in strict mode may vary
   by API version; treat this list as current-observed, not guaranteed-stable.]

NOTE: the `category` enum below MUST stay in sync with the gold categories used
in evals/dataset/*.jsonl. It includes `equipment` (used by ext-005 / cls-005);
adding/removing an enum value here without updating the dataset (or vice versa)
makes an agent output that satisfies the schema but fails the grader, or one
that the API 400s on a valid gold label.
"""

OCR_EXTRACT_TOOL = {
    "name": "expense_ocr_extract",
    "description": (
        "Call an external OCR API to extract the raw text of one invoice or "
        "receipt file. Read-only with respect to the local machine: it makes a "
        "paid outbound network call and returns text, but writes nothing to "
        "disk or to ledger.db. Call this once per source document before any "
        "field extraction. Do NOT call it on a file you have already OCR'd in "
        "this turn."
    ),
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": (
                    "Absolute path to the invoice/receipt file to OCR "
                    "(.pdf, .png, .jpg, or .txt). Must be a path the agent was "
                    "given as input; do not synthesize or guess paths."
                ),
            }
        },
        "required": ["file_path"],
        "additionalProperties": False,
    },
}

FX_RATE_TOOL = {
    "name": "expense_fx_rate",
    "description": (
        "Call an external foreign-exchange API to get the conversion rate from "
        "`currency` to the ledger base currency on a specific date. Read-only, "
        "makes a paid outbound call, writes nothing locally. FX is fast-moving "
        "data: always fetch the rate for the invoice date rather than reusing "
        "a remembered rate. Call this only after the invoice currency and date "
        "are known from extraction."
    ),
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "currency": {
                "type": "string",
                "description": (
                    "ISO 4217 source currency code to convert FROM, e.g. "
                    "'EUR', 'JPY', 'USD'. Exactly 3 uppercase letters."
                ),
            },
            "date": {
                "type": "string",
                "format": "date",
                "description": (
                    "Invoice date the rate is quoted for, as an ISO-8601 "
                    "calendar date 'YYYY-MM-DD'. Use the date extracted from "
                    "the document, not today's date."
                ),
            },
        },
        "required": ["currency", "date"],
        "additionalProperties": False,
    },
}

POST_LEDGER_ENTRY_TOOL = {
    "name": "expense_post_ledger_entry",
    "description": (
        "Write one finalized accounting entry into the local ledger.db SQLite "
        "database. THIS HAS SIDE EFFECTS AND IS NOT REVERSIBLE by the agent: it "
        "mutates local financial records. Only call it after all fields are "
        "extracted, the base-currency amount is computed, and (if needs_human "
        "is true) a human has approved. The harness gates this tool behind an "
        "approval prompt by default."
    ),
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "vendor": {
                "type": "string",
                "description": "Vendor / supplier name exactly as extracted.",
            },
            "date": {
                "type": "string",
                "format": "date",
                "description": "Invoice date, ISO-8601 'YYYY-MM-DD'.",
            },
            "amount": {
                "type": "number",
                "description": (
                    "Total invoice amount in the original invoice currency."
                ),
            },
            "currency": {
                "type": "string",
                "description": (
                    "Original invoice ISO 4217 currency code, 3 uppercase "
                    "letters."
                ),
            },
            "amount_base": {
                "type": "number",
                "description": (
                    "Amount converted to the ledger base currency using the "
                    "expense_fx_rate result."
                ),
            },
            "category": {
                "type": "string",
                "enum": [
                    "travel",
                    "meals",
                    "software",
                    "office_supplies",
                    "professional_services",
                    "utilities",
                    "equipment",
                    "other",
                ],
                "description": "Accounting category for this expense.",
            },
            "needs_human": {
                "type": "boolean",
                "description": (
                    "True if confidence was low or a human approval gate "
                    "applies to this entry."
                ),
            },
        },
        "required": [
            "vendor",
            "date",
            "amount",
            "currency",
            "amount_base",
            "category",
            "needs_human",
        ],
        "additionalProperties": False,
    },
}

ALL_TOOLS = [OCR_EXTRACT_TOOL, FX_RATE_TOOL, POST_LEDGER_ENTRY_TOOL]
