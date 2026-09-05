# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: N/A (self-study, not enrolled) \
SUNet ID: N/A \
Citations: Ollama structured outputs docs (https://ollama.com/blog/structured-outputs); course starter code in `assignments/week2/`

This assignment was completed for personal learning (not for Gradescope).


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
In assignments/week2/app/services/extract.py, add extract_action_items_llm(text, model=None) that uses the local Ollama Python client to extract action items from free-form notes.

Requirements:
- Use ollama.chat with a clear system prompt
- Force structured JSON via format= (see https://ollama.com/blog/structured-outputs), schema like {"action_items": [string, ...]}
- Empty/whitespace input returns [] without calling the model
- Parse JSON, validate shape, raise a clear error on bad output
- Clean bullet/checkbox prefixes and dedupe case-insensitively (reuse shared helper if useful)
- Model name from OLLAMA_MODEL env var with a small local default
- Add brief comments marking the LLM-powered section
``` 

Generated Code Snippets:
```
assignments/week2/app/services/extract.py
- L83–97: _dedupe_preserving_order (shared by heuristic + LLM)
- L99–133: TODO 1 section — DEFAULT_OLLAMA_MODEL, ACTION_ITEMS_SCHEMA, SYSTEM_PROMPT, LLMExtractionError
- L138–193: extract_action_items_llm()
```

### Exercise 2: Add Unit Tests
Prompt: 
```
Add unit tests for extract_action_items_llm in assignments/week2/tests/test_extract.py.

Cover:
- bullet / checkbox lists
- TODO:/Action: keyword-prefixed lines
- empty / whitespace input (must not call the model)
- empty action_items list from the model
- structured-output format= and default model are passed correctly
- model override
- cleanup + case-insensitive dedupe
- non-string items ignored
- invalid JSON / wrong shape raise LLMExtractionError

Mock ollama.chat with monkeypatch so tests are fast and do not need a running Ollama server.
Optional: one opt-in live test gated by RUN_OLLAMA_TESTS=1.
``` 

Generated Code Snippets:
```
assignments/week2/tests/test_extract.py
- L15–27: existing heuristic test (unchanged)
- L30–36: TODO 2 section header
- L39–56: _fake_chat helper
- L59–68: test_llm_extract_bullet_list
- L71–76: test_llm_extract_keyword_prefixed_lines
- L79–85: test_llm_extract_empty_input_skips_model
- L88–90: test_llm_extract_no_action_items
- L93–102: test_llm_extract_uses_structured_output_and_default_model
- L105–110: test_llm_extract_model_override
- L113–118: test_llm_extract_cleans_and_dedupes
- L121–125: test_llm_extract_ignores_non_string_items
- L128–131: test_llm_extract_invalid_json_raises
- L134–145: test_llm_extract_wrong_shape_raises
- L148–155: test_llm_extract_live_ollama (skipped unless RUN_OLLAMA_TESTS=1)
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
Refactor the Week 2 FastAPI backend for clarity. Do NOT change product behavior.

Scope (assignments/week2/app/):
1. Add schemas.py with Pydantic models for notes and action-items request/response bodies.
2. Update routers/action_items.py and routers/notes.py to use those schemas instead of Dict[str, Any].
3. Update main.py: remove module-level init_db(); initialize DB in a FastAPI lifespan; remove unused imports.
4. Light cleanup in db.py only if needed (e.g. clearer helpers). Keep SQLite + existing tables.
5. Add brief comments marking refactor changes.

Constraints:
- Keep existing routes working for the current frontend Extract flow.
- Keep extract_action_items / extract_action_items_llm behavior unchanged.
- After changes, summarize touched files + line ranges for writeup.md Exercise 3.
``` 

Generated/Modified Code Snippets:
```
assignments/week2/app/schemas.py
- L1–end: new Pydantic contracts (NoteCreate/NoteOut, ExtractRequest/ExtractResponse,
  ActionItemOut, MarkDoneRequest/Response)

assignments/week2/app/routers/action_items.py
- full file: ExtractRequest/ExtractResponse, ActionItemOut, MarkDone* schemas;
  404 when mark_done updates 0 rows

assignments/week2/app/routers/notes.py
- full file: NoteCreate / NoteOut response models

assignments/week2/app/main.py
- lifespan context manager calls init_db() on startup (no import-time init)
- removed unused imports

assignments/week2/app/db.py
- mark_action_item_done → returns bool (row updated?) for router-level 404 mapping
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
TODO 4 for Week 2 Action Item Extractor:

1. Add POST /action-items/extract-llm that uses extract_action_items_llm with the same
   ExtractRequest/ExtractResponse schemas as /extract. Map LLMExtractionError to HTTP 502.
2. Add GET /notes that returns all saved notes (declare before /notes/{note_id}).
3. Update frontend/index.html: add "Extract LLM" and "List Notes" buttons wired to those
   endpoints; keep existing Extract + checkbox done behavior.
4. Mark TODO 4 changes with brief comments. Summarize files/lines for writeup.md.
``` 

Generated Code Snippets:
```
assignments/week2/app/routers/action_items.py
- POST /extract-llm using extract_action_items_llm (+ LLMExtractionError → 502)

assignments/week2/app/routers/notes.py
- GET "" list_all_notes() before /{note_id}

assignments/week2/frontend/index.html
- Extract LLM + List Notes buttons
- shared extractVia() helper for heuristic vs LLM paths
- list notes renderer
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
Analyze the Week 2 Action Item Extractor under assignments/week2/ and generate a
clear README.md that includes at least:
- brief project overview
- setup and how to run the server (use assignments.week2.app.main:app)
- API endpoints and functionality (notes + action-items, including extract-llm)
- how to run the test suite
- short project layout

Keep it accurate to the current code (Pydantic schemas, lifespan DB init, frontend buttons).
``` 

Generated Code Snippets:
```
assignments/week2/README.md (new)
- Overview, Setup, Run the server
- API endpoints (notes + action-items)
- Frontend usage
- Tests + project layout
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 
