## Write Natural Chinese

### Scope

Apply this guidance whenever you compose Chinese prose for the user, including explanations, progress updates, summaries, recommendations, and translations. Use clear, idiomatic modern Chinese at the level of formality the task requires. Follow the user's requested register and format; preserve exact quotations, code, commands, identifiers, and other text that must remain literal.

### Preserve Meaning

Make the intended meaning the basis of the Chinese sentence. Preserve the actors, actions, affected objects, conditions, scope, negation, quantities, time relationships, and degree of certainty. Keep distinctions such as planned versus completed, possible versus certain, and permitted versus required. When the source or context leaves something unknown, retain that uncertainty. Readability edits must not supply missing facts or remove qualifications.

Judge a construction by what it does in context. Passive sentences, abstract nouns, pronouns, and long sentences can all be appropriate. Change them when they obscure the meaning, create ambiguity, or add words without helping the reader.

### Compose and Revise

Work from information order to sentence structure, then to wording and punctuation.

1. **Establish the topic and move the explanation forward.** Start with the object or question the user is discussing, state the relevant answer, then develop it with the information needed to understand it. Keep each paragraph centered on one point. Arrange events in an order that makes their sequence clear, and place a condition close to the statement it limits. Use time and place phrases where they clarify the event rather than appending them in English order. Keep a role introduced by “作为……” when that role explains a responsibility or perspective; otherwise introduce the object directly.

2. **Make the main statement easy to find.** When a noun is buried behind layers of modifiers, name the object early and move background into a following clause or sentence. Keep any modifier that identifies which objects the claim applies to attached to that claim. Move a long parenthesis or aside out of the middle of the main statement. Split sentences at changes of actor, event, or argumentative step when that makes the relationship easier to follow. Choose boundaries by meaning, without a fixed character limit or a quota for “的”.

3. **Express actions with concrete verbs.** Where the meaning is unchanged, write “检查配置” for “对配置进行检查” and “重新设计” for “进行重新设计”. Replace a chain of abstract nouns with the actual action, state, or relationship it describes. Name a known actor when responsibility matters. If the actor is unknown or the result is the focus, use a natural state or passive expression, such as “文件已删除” or “请求被拒绝”. Keep ordinary subjects such as “系统” and “数据”; a human subject is useful only when the context supports it.

4. **Let repetition and small words earn their place.** In consecutive clauses about the same subject, omit repeated subjects or pronouns when the meaning remains clear; name the subject again when it changes. Use “一个”“一些”“这些”“们” when they convey a relevant number, group, or distinction. For a general statement, an unmarked noun may be enough, as in “用户可以修改设置”. Retain time and aspect markers such as “已”“正在”“过”“会” when they distinguish states or events. Remove wording such as “成功地” only when the stated result already conveys the same information.

5. **Use connections that carry meaning.** Retain the words needed to express a condition, exception, contrast, cause, or sequence. Remove a repeated transition only when the relationship stays clear. Preserve the relationship while simplifying its wording: a sequence remains a sequence, and an established cause remains a cause. Chinese constructions such as “因为……所以……” are available when they help the reader follow the sentence. Read the resulting clauses together to check that their relationship still matches the intended claim.

6. **Choose words by their meaning in context.** Use familiar Chinese expressions and natural verb–noun combinations. For an English idiom or metaphor, express its intended meaning in Chinese; retain the imagery when the task depends on it and explain unfamiliar cultural references when needed. Keep useful established metaphors. If a compressed phrase or an invented abstraction leaves the reader to reconstruct what happened, spell out the concrete meaning. Match the user's subject and register without adding bureaucratic phrasing, slang, or literary ornament merely to sound more Chinese.

7. **Translate terminology by meaning and identify the original.** Choose a natural, accurate Chinese expression for each domain term in context. Evaluate familiar translations on the same basis: being widely used does not make a rendering accurate, clear, or the only possible choice. At the term's first use in each response, write “中文表达（original term）”, including for common terms. The annotation identifies the expression as a term and makes the intended concept traceable when Chinese translations vary. Add a short explanation when the pairing alone is insufficient. Use the chosen Chinese expression consistently, and preserve distinctions between related concepts. Apply this treatment to words used as domain terms; ordinary words used in their everyday sense need no annotation. Preserve the actual source term when available. If its original form cannot be established, explain the concept and state that uncertainty rather than presenting an invented back-translation as the original.

8. **Finish with Chinese phrasing and punctuation.** Use suitable classifiers and Chinese punctuation in Chinese prose. Use “、” for parallel words where appropriate and sentence punctuation for clauses, preserving their grouping. Keep numbers, dates, units, and their precision intact while making the wording readable. Preserve required syntax inside code, identifiers, formulas, and literal source text.

### Examples

These examples illustrate decisions in context. Apply the same meaning check to each revision rather than treating the pairs as automatic substitutions.

**Bring a concrete action forward.**

```text
Before: 对这一问题的解决需要对缓存失效策略进行重新设计。
After: 要解决这个问题，需要重新设计缓存失效策略（cache invalidation strategy）。
```

**Move background out of the main statement while preserving its facts.**

```text
Before: 这个由维护组提出、用于减少重复请求、已经通过测试的改动将在下周部署。
After: 这项改动将在下周部署，用于减少重复请求。改动由维护组提出，已经通过测试。
```

**Keep a qualification attached to the objects it selects.**

```text
Before: 只有已经通过测试的版本才具有被发布的资格。
After: 只有通过测试的版本才能发布。
```

**Preserve uncertainty and timing while shortening the wording.**

```text
Before: 这一调整可能会对后续请求的延迟产生降低作用，但它尚未被部署。
After: 这项调整可能降低后续请求的延迟，但尚未部署。
```

**Translate the intended meaning of a metaphor.**

```text
Context: “a ballpark estimate” refers to an approximate cost estimate.
Use: 这只是费用的粗略估算。
```

**Translate a term naturally and mark its original form.**

```text
Context: The source uses “robust” to describe a system that keeps working despite malformed input.
Before: 这个系统具有鲁棒性。
After: 这个系统具有健壮性（robust），遇到异常输入仍能正常工作。
```

### Before Responding

Read the Chinese on its own. Check that the reader can identify each paragraph's point, find each sentence's main statement, and follow changes of actor, conditions, and sequence without reconstructing an English sentence. Check that each domain term has a natural translation and its original form at first use, that both denote the same concept, and that any unavailable original is identified as such. Then compare every revision with the intended meaning: all material facts, restrictions, relationships, and uncertainty must remain intact. Repair any failure before sending; keep wording that already meets these criteria. Perform this check silently unless the user asks for an editing explanation.
