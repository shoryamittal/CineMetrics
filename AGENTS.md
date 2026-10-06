# CineMetrics — Agent Guidelines (Karpathy Principles)

These guidelines govern all AI coding agents working on this repository, derived from Andrej Karpathy's observations on LLM coding pitfalls.

## 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**
- State assumptions explicitly before modifying files.
- If multiple architectural approaches exist, present tradeoffs rather than choosing silently.
- Push back when a simpler, more maintainable alternative exists.

## 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**
- Zero speculative complexity or unused abstractions.
- No single-use helper libraries or layers.
- If 200 lines could be 50, simplify.

## 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**
- Do not make drive-by edits to unrelated code, comments, or formatting.
- Match existing repository patterns and styles.
- When deleting or refactoring, clean up any orphan imports or dead variables created by your change.

## 4. Goal-Driven Execution
**Define success criteria. Loop until verified.**
- Define verifiable goals before running modifications.
- Validate JSON structures, DOM bindings, and script execution before completion.
