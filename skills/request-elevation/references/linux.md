# Linux Elevation

Read this reference only for commands executing on Linux. Apply the shared scope, approval, and verification rules in `SKILL.md`.

## Select the Mechanism

Prefer `pkexec` when it is installed and a usable Polkit authentication interface is available. It uses a registered authentication agent; when none exists, its internal text agent requires an interactive terminal. A non-interactive agent tool is not itself an authentication interface.

If `pkexec` or its authentication interface is unavailable, select `sudo` only when existing sudo policy and an available authentication path support the authorized operation. Read [sudo execution](sudo.md) before constructing that invocation. Missing prerequisites may justify this selection; an authentication cancellation or authorization denial does not.

Complete selection when the utility, required target account, and authentication path are verified. Otherwise report the missing prerequisite.

## Construct a pkexec Invocation

Resolve all placeholders before execution:

```text
pkexec --user <target-user> <program> <literal-arguments>
```

Always supply the program: omitting it can start a shell. Use its default working-directory and sanitized environment behavior; avoid `--keep-cwd` and caller-environment restoration through `env`.

For an authorized restart, when the commands are available in the execution environment:

```bash
pkexec --user root systemctl restart example.service
```

After completion, verify separately without elevation where permitted:

```bash
systemctl is-active example.service
```

`pkexec` passes program arguments without validating them. Review the operation's effects before execution even if Polkit grants retained authorization.

## Interpret the Result

`pkexec` reports `126` when the authentication dialog is dismissed and `127` for authorization or other setup errors. After successful invocation it returns the program's exit status, which can also be `126` or `127`. Inspect diagnostics and observable state before assigning a cause. Apply the shared stop and retry rules after cancellation or denial.

Source: [Polkit pkexec manual](https://www.freedesktop.org/software/polkit/docs/latest/pkexec.1.html).
