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
from `--cook-cmd` or `COOK_CMD`. The default is the non-runnable
`REPLACE_WITH_COOK_CMD` placeholder. The harness:

- runs the command with the isolated checkout as its current directory;
- supplies the prompt on stdin and in `{prompt_file}`;
- captures stdout as the final response unless the command writes
  `{output_file}`;
- applies a hard subprocess `{timeout_seconds}`;
- records only the SHA-256 of the command, never the command text or environment;
- starts the cook with an allowlisted path/locale environment (no inherited
  API keys, tokens, or credentials);
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
| `{tag}` / `{phase}` | Stable cell label and call phase |
| `{max_tokens}` | Required: this call's share of the matched token cap |
| `{timeout_seconds}` | This call's share of the matched wall cap |
| `{safe_mode}` | Expands to `--safe-mode` for a command containing `claude` |

Do not wrap placeholders in another layer of shell quotes; the harness
shell-quotes path values. A wrapper that produces token accounting should write:

```json
{
  "input_tokens": 1000,
  "output_tokens": 500,
  "total_tokens": 1500
}
```

For example, a local wrapper could be configured as:

```bash
export COOK_CMD='my-cook-wrapper --run-dir {run_dir} --max-tokens {max_tokens} --usage {usage_file}'
```

Authenticate that wrapper through a local credential store or broker. The
harness deliberately does not make inherited secret environment variables
available to model-facing processes.

For a Claude-based command, the harness fails closed unless the literal
`--safe-mode` or `{safe_mode}` appears in `COOK_CMD`. Use a wrapper that both
applies that flag and enforces the passed token cap, for example:

```bash
export COOK_CMD='my-claude-wrapper {safe_mode} --max-tokens {max_tokens} --usage {usage_file}'
```

Real execution is rejected if `{max_tokens}` is absent. If the chosen CLI does
not report token usage, condition 7 cannot pass: the
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
manifest. Every result, including an empty source patch or a failed cook, is
frozen; there is no cherry-picking.

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
~/.swebench-venv/bin/python run_trial.py --phase plans
~/.swebench-venv/bin/python run_trial.py --phase decisions
```

All B plans are frozen before the first candidate decision. Decision-cell order
is seeded and randomized across arms. Each A artifact gets the entire matched
token/wall cap in one call. Each B artifact gets the identical total cap split
evenly across its candidate-blind plan and candidate-visible validation calls.
Both arms see the same base repository, candidate, and public tests; neither
receives gold, `test_patch`, `FAIL_TO_PASS`, or `PASS_TO_PASS`.

The decision phase creates `artifacts/trial/fidelity-audit-input.json`, which is
blind to SWE-bench outcomes, and `fidelity-result.template.json`. Run the frozen
cross-family GLM-5.2/DeepEval audit over both-arm trajectories, then write
`artifacts/trial/fidelity-result.json` with the same fields and bound
`audit_input_sha256`. The fidelity audit may veto for leakage or failed
discipline; it never supplies candidate truth.

### 5. Freeze repeated SWE-bench truth

Only after all decisions—and preferably the blinded fidelity audit—are frozen:

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

For an uninterrupted head-chef run, `run_trial.py --phase all` executes plans,
decisions, and oracle in that order. Phase commands are resumable: already
frozen cells are checked and skipped, and a changed configuration is rejected.

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
python3 score.py --help
```
