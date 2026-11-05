# sudo Execution

Read this reference only when the Linux or macOS procedure selects `sudo`. Apply the shared scope, approval, and verification rules in `SKILL.md`.

## Select an Available Mode

Verify `sudo` availability, the target account, and applicable existing policy. For non-interactive execution, use:

```text
sudo -n -u <target-user> -- <program> <literal-arguments>
```

`-n` exits with an error if authentication requires user interaction. It works only when existing policy and any applicable cached credentials permit the operation. It does not grant permission or prove authorization. Run the reviewed operation itself; a separate `sudo -v` only refreshes credentials and does not establish that the command is permitted.

When authentication is required, use an interactive terminal the user controls, through a permitted terminal tool, with this shape:

```text
sudo -u <target-user> -- <program> <literal-arguments>
```

The user enters credentials directly into sudo's terminal prompt. Do not capture their input, use `sudo -S`, supply a password through stdin, or configure an askpass helper to handle credentials. If the environment cannot provide a terminal the user controls, report the blocker or use the platform's documented system-dialog path only if there has been no cancellation or denial.

Use the verified utility directly. Keep sudo's default environment handling; do not use `-E`, an elevated login shell, or an interactive root shell to make the operation work.

Complete mode selection when the exact invocation is reviewable and authentication can occur without the agent handling credentials.

## Interpret the Result

Use stderr and observed state to distinguish an authentication requirement, a sudo policy denial, an execution error, and a failure returned by the program. A nonzero status alone is insufficient to determine whether the program ran. Inspect possible effects before retrying; stop after cancellation or denial under the shared rules.

Consult the host's `man sudo` for installed-version behavior, especially `-n`, `-u`, authentication, and exit values.
