# Molecular Gastronomy trust-decision trial harness

This directory builds and orchestrates the trial frozen in
`PRE-REGISTRATION.md`. It does not contain trial results. The scripts deliberately
do not import or modify `research/molecular-gastronomy/ab_run.py`.

The checked-in `tasks.json` is the frozen 30-task bank: 15 tasks in each OpenAI
difficulty band (`15 min - 1 hour`, `1-4 hours`), from the allowed network-free
repository set, with issue #24's instances excluded.

## Runtime prerequisites

Use the SWE-bench environment directly:

```bash
python3 -m venv ~/.swebench-venv
~/.swebench-venv/bin/pip install swebench
```

SWE-bench 4.1.0 was present when the harness was built. Task selection and every
SWE-bench command should use `~/.swebench-venv/bin/python`. Docker is required
only when the head chef later runs calibration or candidate grading. GitHub
network access is required to create the disposable repository mirrors; cooks
are told not to use the network.

All examples below run from `experiments/molgas-trial/`.

## `COOK_CMD` convention

`gen_candidates.py` and `run_trial.py` receive one configurable shell template
from `--cook-cmd` or `COOK_CMD`, plus an exact model identifier from
`--cook-model` or `COOK_MODEL`. Both defaults are non-runnable placeholders.
The harness:

- runs the command with the isolated checkout as its current directory;
- supplies the prompt on stdin and in `{prompt_file}`;
- captures stdout as the final response unless the command writes
  `{output_file}`;
- applies a hard subprocess `{timeout_seconds}`;
- records only the SHA-256 of the command, never the command text or environment;
- starts the cook with an allowlisted path/locale environment (no inherited
  API keys, tokens, or credentials);
- gives each call isolated `HOME` and `TMPDIR` directories under `{run_dir}`;
- exposes only the harness values as `MOLGAS_*` environment variables; and
- reads optional numeric token accounting from `{usage_file}`.

For the pre-registered fidelity audit, the wrapper must also leave its
tool trajectory in `{run_dir}`. The harness bounds retained output and artifact
sizes, removes symlinks, secret-screens/redacts retained files, and fails the
cell closed on any screening violation. It then content-hashes the entire run
directory, plans, decisions, and final responses before the blinded audit;
`score.py` rejects any post-audit mutation.

Available placeholders are:

| Placeholder | Meaning |
| --- | --- |
| `{run_dir}` | Per-call directory containing `prompt.txt` and `run.spec.json` |
| `{prompt_file}` | Absolute prompt path |
| `{output_file}` | Absolute path where the wrapper may write the final response |
| `{usage_file}` | Optional JSON token-usage path |
| `{checkout}` | Absolute isolated checkout |
| `{model}` | Required: the fixed `COOK_MODEL` identifier |
| `{max_compute_tokens}` | Required: this call's share of the reasoning/compute-token cap |
| `{max_tokens}` | Required: this call's share of the matched token cap |
| `{max_tool_calls}` | Required: this call's share of the tool-call cap |
| `{timeout_seconds}` | This call's share of the matched wall cap |
| `{safe_mode}` | Expands to `--safe-mode` for a command containing `claude` |

Do not wrap placeholders in another layer of shell quotes; the harness
shell-quotes path values. A wrapper that produces token accounting should write:

```json
{
  "input_tokens": 1000,
  "output_tokens": 500,
  "total_tokens": 1500,
  "compute_tokens": 400,
  "tool_calls": 12
}
```

For example, a local wrapper could be configured as:

```bash
export COOK_CMD='my-cook-wrapper --model {model} --run-dir {run_dir} --max-tokens {max_tokens} --max-compute-tokens {max_compute_tokens} --max-tool-calls {max_tool_calls} --usage {usage_file}'
export COOK_MODEL='exact-provider-model-id'
```

Authenticate that wrapper through a local credential store or broker. The
harness deliberately does not make inherited secret environment variables
available to model-facing processes. For a non-Claude cook, the wrapper must
also enforce filesystem/network de-contamination equivalent to Claude
`--safe-mode`; the harness prompts forbid access beyond the isolated checkout.

For a Claude-based command, the harness fails closed unless the literal
`--safe-mode` or `{safe_mode}` appears in `COOK_CMD`. Use a wrapper that both
applies that flag and enforces the passed token cap, for example:

```bash
export COOK_CMD='my-claude-wrapper {safe_mode} --model {model} --max-tokens {max_tokens} --max-thinking-tokens {max_compute_tokens} --max-tool-calls {max_tool_calls} --run-dir {run_dir} --usage {usage_file}'
```

Real execution is rejected unless `{model}`, `{max_compute_tokens}`,
`{max_tokens}`, and `{max_tool_calls}` are all present. The same exact command,
model, and aggregate caps are frozen for both arms; B splits each cap across its
two calls. If the chosen CLI does not report token usage, condition 7 cannot pass: the
scorer reports the token-cost ratio as unavailable. Use a wrapper that writes
`{usage_file}`. The same exact `COOK_CMD` is frozen and used for both arms.

## Run order

### 1. Verify or reconstruct the frozen task bank

`tasks.json` is already frozen and should not be regenerated after outcomes
exist. To reproduce selection without replacing it:

```bash
~/.swebench-venv/bin/python select_tasks.py \
  --output /tmp/molgas-tasks-reproduction.json
```

Compare its `task_bank_sha256` to `tasks.json`. If using a cached Arrow dataset,
pass `--dataset-arrow PATH`. Selection reads no pilot, candidate, or grader
outcomes.

### 2. Freeze two neutral candidates per task

```bash
~/.swebench-venv/bin/python gen_candidates.py --dry-run
~/.swebench-venv/bin/python gen_candidates.py \
  --max-tokens 16000 \
  --timeout-seconds 3600
```

This writes 60 source-only patches plus `artifacts/candidates.json`. Public-test
changes are excluded exactly as in the reference harness and recorded in the
manifest. A failed cook, cap/screening violation, or empty source patch stops
the fixed generation run; successful artifacts are never cherry-picked.

### 3. Calibrate every selected ruler before candidate outcomes

```bash
~/.swebench-venv/bin/python calibrate.py --dry-run
~/.swebench-venv/bin/python calibrate.py \
  --max-workers 2 \
  --test-timeout-seconds 1800
```

The script directly invokes:

```text
~/.swebench-venv/bin/python -m swebench.harness.run_evaluation ...
```

It performs four runs: gold twice and a behaviorally inert base control twice.
A literal empty prediction cannot be used because SWE-bench skips it, so the
base control creates a zero-byte `.molgas-empty-control` file and changes no
program behavior. A task calibrates only for gold `[true, true]` and base
`[false, false]`. Docker image IDs are frozen. Gold-bearing predictions and
evaluator logs live in a temporary directory and are deleted before
`artifacts/calibration.json` is written.

### 4. Freeze plans and randomized arm decisions

Run phases separately so the blinded fidelity audit can happen before candidate
truth is materialized:

```bash
~/.swebench-venv/bin/python run_trial.py --dry-run
~/.swebench-venv/bin/python run_trial.py --phase decision-pipeline
```

The decision pipeline freezes all B plans before the first candidate decision.
It is also resumable as separate `--phase plans` and `--phase decisions` calls.
Decision-cell order
is seeded and randomized across arms. Each A artifact gets the entire matched
compute-token/token/tool-call/wall cap in one call. Each B artifact gets the
identical aggregate caps split evenly across its candidate-blind plan and
candidate-visible validation calls.
Both arms see the same base repository, candidate, and public tests; neither
receives gold, `test_patch`, `FAIL_TO_PASS`, or `PASS_TO_PASS`.

The decision phase creates `artifacts/trial/fidelity-audit-input.json`, which is
blind to SWE-bench outcomes. Configure a DeepEval wrapper and run the
cross-family auditor:

```bash
export DEEPEVAL_CMD='my-deepeval-wrapper --model {model} --input {prompt_file} --output {output_file} --max-tokens {max_tokens} --max-thinking-tokens {max_compute_tokens} --max-tool-calls {max_tool_calls}'
~/.swebench-venv/bin/python audit_fidelity.py --dry-run
~/.swebench-venv/bin/python audit_fidelity.py
```

`audit_fidelity.py` fixes the auditor to GLM-5.2, refuses to run after
`oracle.json` exists, requires one evidence-bearing assessment per arm/candidate
cell, and deterministically derives the fidelity summary. It writes the bound
`artifacts/trial/fidelity-result.json`. The audit may veto for leakage or failed
discipline; it never supplies candidate truth.

### 5. Freeze repeated SWE-bench truth

Only after all decisions and the blinded fidelity audit are frozen:

```bash
~/.swebench-venv/bin/python run_trial.py --phase oracle \
  --max-workers 2 \
  --test-timeout-seconds 1800
```

SWE-bench collapses duplicate `instance_id` predictions, so the harness runs one
prediction file per candidate index and repeat: two candidate indices × two
repeats = four evaluator runs. A candidate must receive the same verdict twice.
Oracle work directories are temporary; `artifacts/trial/oracle.json` retains
only repeated boolean verdicts and hashes.

Oracle execution is blocked until the bound GLM-5.2/DeepEval result exists.
Phase commands are resumable: already frozen cells are checked and skipped, and
a changed configuration is rejected.

### 6. Score against the eight-condition bar

```bash
python3 score.py
# Optional machine-readable copy:
python3 score.py --json-output artifacts/trial/score.json
```

The scorer joins every frozen decision to repeated SWE-bench truth and prints:

- utility `+1 / -4 / 0`, averaged within each two-artifact task cluster;
- false-serve, true-serve, coverage, served reliability, and Brier score;
- median token, wall-time, and call costs;
- a seeded task-clustered bootstrap 95% interval;
- an exact task-level paired sign-flip p-value; and
- PASS/FAIL for all eight frozen conditions, ending in `EARN` or `NOT-YET`.

Missing/malformed arm output is a fail-closed `REFUSE` with `P_PASS=0`. Missing
token usage fails cost condition 7. Missing or unbound fidelity results fail
condition 8. Oracle instability or incomplete candidate coverage stops scoring;
the script never silently drops an artifact or task after outcomes are visible.

## Cheap validation

These commands do not call a cook, Docker, or SWE-bench grading:

```bash
python3 -m unittest -v test_harness.py
python3 -m compileall -q .
python3 select_tasks.py --help
python3 gen_candidates.py --dry-run
python3 calibrate.py --dry-run
python3 run_trial.py --dry-run
python3 audit_fidelity.py --dry-run
python3 score.py --help
```
