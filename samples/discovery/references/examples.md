# Predicate Extraction Examples

Kept separate from `SKILL.md` for maintainability — see
`references/predicate-reference.md` for why, and study these alongside it.

**Example 1: Multiple Predicates** `natural_language_query: Big Query tables
containing the name foo in project bar` `search_query:
system=bigquery AND type=table AND name:foo AND projectid=bar`

**Example 2: Negation** `natural_language_query: Find me all tables not
containing the name foo` `search_query: type=table AND -name:foo`

**Example 4: Logical OR** `natural_language_query: tables from project foo-1 or
bar-1.` `search_query: type=table AND (projectid:foo-1 OR projectid:bar-1)`

**Example 5: Parent Predicate** `natural_language_query: Find all the tables in parent dataset bar.` `search_query: type=table AND parent=bar`

**Example 6: Ambiguous / Unclear Query** `natural_language_query: foo data`
`search_query:`

**Example 7: Very Simple Query** `natural_language_query: Show me all the
datasets` `search_query: type=dataset`

**Example 8: Complex Query with tricky parentheses placement**
`natural_language_query: show me all the table and datasets in project foo or it must be part of bigquery` `search_query: ((type=table OR type=dataset) AND projectid=foo) OR system=bigquery`

**Example 9: Query having name and description predicate**
`natural_language_query: show me all the table that contain name sales and
description pollution` `search_query: type=table AND name:sales AND
description=pollution`
