# Predicate Extraction Reference

Kept separate from `SKILL.md` for maintainability — this material is only
relevant to the predicate extraction procedure in `SKILL.md` Step 2, not to
the rest of the skill. `agent.py` concatenates it into the agent's
instruction at load time, since this agent has no file-reading tool of its
own; an agent that does have one (see `kb-search/SKILL.md`) could instead
load it on demand.

**Predicates from the table only.** You MUST only use predicates from the
Predicate Reference Table below. If a keyword does not map to a predicate,
you MUST ignore it. NEVER invent a new predicate.

### Rule #1: The Output Format

*   Your response MUST be in the following exact format. Do not include any
    other text, greetings, or explanations.
*   Do **not** wrap the output in markdown formatting (e.g., \`\`\` or \`).
*   Do **not** include any newlines after the response.
set of predicates like: `projectid:your-project-id AND type=table`
*   If the natural language query is empty, unclear, or does not contain any
    mappable keywords, the output MUST be an empty set.

### Rule #2: Strict Adherence to Definitions

*   **Only Use Official Predicates:** You MUST only use predicates from the
    **Predicate Reference Table**. If a keyword does not map to a predicate, you
    MUST ignore it. NEVER invent a new predicate.
*   **Only Use Allowed Operators:** Each predicate has a specific list of
    allowed comparison operators. You MUST only use an operator that is valid
    for that predicate.
*   **Logical Operators:** The logical operators `AND` and `OR` MUST be in
    uppercase.
*   **Negation:** To exclude a term, you MUST prefix the predicate with a hyphen
    (`-`). For example: `-name:foo`.
*   **Warning on Logical Expressions:** The placement of parentheses `()` is
    critical when using logical operators like `AND`, `OR`, and `-`. Ensure that
    you group conditions correctly to reflect the precise intended logic. For
    example, `(A AND B) OR C` is not the same as `A AND (B OR C)`. Verify the
    logical structure of your output to prevent errors.
*   **Warning on name and description:** The `name` and `description` predicates MUST ONLY BE USED WHEN THE QUERY EXPLICITLY USES TERMS
     LIKE "name" or "description" to refer to a property of a
    resource. For example, in "show me all datasets having name xx_yz", `name` is a valid predicate. In contrast, for "give me the names of all systems", the word "names" does not refer to
    the `name` predicate.

### Predicate Reference Table

This is your single source of truth for all predicates.
| Predicate         | Allowed          | Common Keywords & | Explanation       |
:                   : Operators        : Triggers          :                   :
| :---------------- | :--------------- | :---------------- | :---------------- |
| **`type`**        | `=`              | `table`,          | **(Default        |
:                   :                  : `tables`,         : Type)** Matches a :
:                   :                  : `dataset`,        : specific resource :
:                   :                  : `datasets`        : type.             :
| **`system`**      | `=`              | `bigquery`,       | Matches the       |
:                   :                  : `cloud_sql`,      : source system     :
:                   :                  : `dataplex`        : (e.g., BigQuery). :

| **`description`** | `=`              | `description`     | Matches the text  |
:                   :                  :                   : in the resource's :
:                   :                  :                   : description.      :
| **`name`**        | `:`, `=`, `!=`   | `name`            | Matches the       |
:                   :                  :                   : resource ID. Use  :
:                   :                  :                   : `\:` for          :
:                   :                  :                   : "contains."       :
| **`displayname`** | `:`, `=`, `!=`   | `display name`    | Matches the       |
:                   :                  :                   : human-readable    :
:                   :                  :                   : display name.     :
| **`projectid`**   | `=`, `:`         | `project`,        | Matches a         |
:                   :                  : `project id`,     : specific Google   :
:                   :                  : `projectid`       : Cloud project ID. :
| **`parent`**      | `=`, `:`         | `parent`          | Matches the       |
:                   :                  :                   : hierarchical      :
:                   :                  :                   : parent of a       :
:                   :                  :                   : resource.         :
