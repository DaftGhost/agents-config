# macOS Elevation

Read this reference only for commands executing on macOS. Apply the shared scope, approval, and verification rules in `SKILL.md`.

## Select the Authentication Path

- When an interactive terminal the user controls is available, or existing sudo policy permits non-interactive execution, read [sudo execution](sudo.md) and use that path. It also supports an explicitly selected target account when policy permits.
- When the task needs `root`, terminal authentication is unavailable, and the environment permits a macOS system authentication dialog, use the AppleScript procedure below. Verify that `osascript` and an interactive GUI session are available.

`with administrator privileges` runs as `root`; it does not select an arbitrary target user. For another account, use a permitted sudo path. When neither path is available, report the missing prerequisite and continue unaffected work. Do not switch paths after cancellation or denial.

Complete selection when the chosen path supports the required identity and the user can authenticate without disclosing credentials to the agent.

## Construct the System Dialog Invocation

`do shell script` passes a string to its shell, whose configured PATH can differ from the caller's. Verify that the command is available in that environment. This is a narrow authentication-transport exception to direct execution: the resulting shell string must contain exactly one verified utility invocation with literal arguments. Keep all other preparation and verification outside it.

Use a fixed AppleScript program and pass the reviewed executable and arguments through `osascript`'s argument vector. Within AppleScript, apply `quoted form of` to the executable and each argument separately. When the outer tool uses a shell, quote those outer arguments too; AppleScript quoting does not protect the outer shell.

For one authorized directory creation, with the utility and destination already reviewed:

```bash
osascript -e 'on run argv' -e 'set commandText to quoted form of (item 1 of argv)' -e 'repeat with argumentValue in (items 2 thru -1 of argv)' -e 'set commandText to commandText & " " & quoted form of (contents of argumentValue)' -e 'end repeat' -e 'do shell script commandText with administrator privileges' -e 'end run' mkdir '/Library/Application Support/Example'
```

The loop only quotes arguments for one invocation; it does not execute multiple operations. Adapt the executable and arguments to the reviewed operation, retaining this boundary. Show both the full `osascript` invocation and the underlying command during review so the operation remains inspectable.

Use `with administrator privileges` without `user name` or `password` clauses. The user authenticates directly in the system dialog. Do not nest `sudo`, an additional shell, or another interpreter in `commandText`.

Complete construction when both quoting layers preserve the exact reviewed argument values and the resulting command performs only the authorized operation.

## Interpret and Verify

A nonzero shell exit status raises an AppleScript error, with diagnostics from the command. Authentication can also fail or be canceled before the command runs; inspect the actual error rather than treating every AppleScript error as a program exit. Stop after cancellation or denial under the shared rules.

Verify resource state in a separate unprivileged call where possible. For the example, inspect the directory and its owner and permissions; receiving a dialog or an empty successful result alone does not establish the desired state.

Source: [Apple Technical Note TN2065: do shell script](https://developer.apple.com/library/archive/technotes/tn2065/_index.html). This archived note documents the authentication and quoting interface; verify current host behavior rather than relying on its historical implementation details.
