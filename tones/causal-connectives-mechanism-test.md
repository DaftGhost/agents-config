# Causal Connectives Must Pass the Mechanism Test

What: Using "therefore," "so," "because," "which is why," "this led to" to join events that are merely correlated, sequential, or parallel; presenting weakly and strongly relevant factors side by side with equal weight; letting a conclusion written in causal form stand in for missing reasoning steps.

Why: A causal connective is a promise to the reader: the premises suffice for the conclusion. When the promise is not kept, the reader is either misled or forced to reconstruct the argument chain. Once a conclusion is written in causal form, later text treats it as established and builds on it, propagating the error. Equal-weight listing of unequal factors prevents the reader from allocating weight.

How: Every causal connective must pass the mechanism test: can you write out the transmission path from cause to effect? If not, downgrade to correlation wording ("over the same period," "associated with; direction and strength not established"). State main factors, secondary factors, and background conditions in separate layers, not side by side. Where reasoning has a gap, mark it explicitly ("this step assumes H, unverified") instead of bridging it with "therefore."

Example Before: The service was rewritten in Go, so latency dropped 40%. After: In the release that rewrote the service in Go, latency dropped 40%; the same release changed the serialization format and the connection-pool policy, so the drop cannot be attributed to the language change alone.
