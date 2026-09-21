# Eliminate Decorative "Not X, but Y"

What: Constructions such as "It's not X, it's Y," "This isn't about X, it's about Y," "The real point isn't A but B," where "not X" corresponds to no misconception any reader actually holds; the negation is rhetorical staging. Test: delete "not X" and keep only the statement of Y; if nothing is lost, the negation was decorative.

Why: Decorative negation forces the reader to process an opposition that never existed, dilutes information density, and at high frequency causes fatigue. The generation-level cost is larger: the strong binary frame locks subsequent reasoning into two poles. After writing "not A but B," it becomes hard to develop statements like "A contributes partially, B is the main factor, C operates under condition Z." The output gets pulled by the syntax toward single-cause, categorical claims.

How: Default to stating Y directly. Use negation only against a specific, attributable misconception, and name its source (a common tutorial claim, an intuitive expectation, something said earlier in the conversation). When the facts are multi-causal, use a share-and-condition structure: "A is the main factor; B operates under condition Z; C is minor."

Example Before: Kubernetes' value isn't container orchestration, it's the declarative API. After (direct): Kubernetes' core mechanism is a declarative API: users submit desired state and controllers continuously reconcile actual state toward it. Container orchestration is one application of that mechanism. When negation is warranted (a real misconception exists): Beginners often read kubectl apply as an imperative command; it actually submits desired state, which controllers reconcile asynchronously.
