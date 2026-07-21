# The Cookbook

The chain's standards — a way of working with Claude Code — packaged as an installable
plugin so any kitchen, on any machine, can cook by them.

Status: **test print.** The only thing in the book right now is a single deliberately
distinctive rule, used to verify that rules delivered by this plugin are obeyed with the
same force as hand-written user-level instructions. The real content (the method, with
the machine-specific staff roster separated out) gets written only if the test print
sticks.

## Try it

```
claude plugin marketplace add <path-or-url-of-this-repo>
claude plugin install chain-standards@cookbook
```

Then, in a fresh session anywhere, say `pineapple-check`. If the reply begins with
`COOKBOOK RULE ACTIVE`, the book works.
