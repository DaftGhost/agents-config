---
name: bilingual-pairs
description: Translate text faithfully while keeping original wording, translation, and explanation distinguishable. Use whenever the user asks to translate, provide a bilingual rendering, translate sentence by sentence, or explain content in a language different from the current conversation language, even if they do not explicitly name this skill.
argument-hint: "[text-or-path-or-url] [target-language]"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebFetch
---

# Bilingual Pairs with Clear Attribution

Follow the user's requested target language, scope, order, and format. If no target language is specified and the context does not establish one, use the current conversation language.

Make the distinction between original text, translation, and explanation explicit. Apply the following defaults unless the user specifies a different treatment.

- **Original text:** Identify quoted source wording as original text and preserve it as supplied.
- **Translation:** Identify translated wording as translation and keep it faithful to the source. Put added commentary, interpretation, and background in the explanation rather than presenting them as part of the translation.
- **Explanation:** Identify explanations as explanations. Keep analysis, context, and interpretation distinguishable from both the source wording and its translation.

Use clear labels or distinct blocks for the components included in the response. Separation does not require including all three components; include only what serves the user's request.

The user's explicit requirements take precedence. If the user asks only for an explanation, provide the explanation without adding an unrequested translation. If the user asks for sentence-by-sentence translation, organize the response by sentence rather than imposing three document-wide sections. Follow any other requested scope, order, format, or additions instead of forcing the default arrangement.

Before responding, check that the reader can distinguish the included original wording, translated wording, and explanatory additions, and that the response follows the user's specific requirements.
