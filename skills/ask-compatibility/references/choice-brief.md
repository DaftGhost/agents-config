# Choice Brief

Read this when you are about to ask the user to decide a compatibility or retention choice.

## Layout

Keep the brief short enough to answer in one reply. Cover, in this order:

1. **What the change touches**: the interface, code, or data, and how it is used (known consumers, readers, jobs).
2. **What could not be verified**: consumers or data outside the repository.
3. **Options**: two or three feasible ones, each with user impact and maintenance cost.
4. **Recommendation**: one option and the evidence behind it.
5. **What you are doing meanwhile**: the independent work you continue and the state you leave intact.

Ask one question per decision. When compatibility and data retention both apply, ask them as separate choices.

## Example

User: "Rename `user_name` to `username` in the user API response and clean up."

```text
Renaming `user_name` changes a field that other clients read, so I haven't edited the serializer or OpenAPI yet.

Affected: GET /v2/users/{id}. CONSUMERS.md lists mobile app 3.x (reads `user_name`; releases take ~2 weeks to reach users), partner-sync (external, integration version unknown), and admin web (this repo). I can't verify what partner-sync reads.

Options:
1. Hard rename now: simplest, but breaks mobile 3.x and possibly partner-sync until they update.
2. Output both fields until an exit condition (for example mobile 3.x end of support), then drop `user_name`: no breakage, small temporary duplication.
3. Keep `user_name` and add nothing: no work, naming stays inconsistent.

Recommendation: option 2, because two consumers are outside this repo and one cannot be verified.

Meanwhile I'm leaving the serializer and OpenAPI unchanged. Which option, and for option 2, what exit condition?
```
