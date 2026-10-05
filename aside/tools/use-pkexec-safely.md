## Use pkexec Safely

### What

Use `pkexec` for a necessary, task-authorized operating-system operation only when the environment permits it. Each authorization request and its execution tool call must contain exactly one direct command for one reviewed operation. Request and execute additional commands separately, inspecting each result before proceeding.

`pkexec` does not replace the environment's sandbox or agent approval mechanism. Obtain required environment approval through that mechanism; never use `pkexec` to bypass a restriction or rejection.

### Why

Administrator privileges magnify the effects of incorrect paths, arguments, and hidden operations. A single scoped command makes the requested action reviewable. `pkexec` does not validate its program's arguments, and authentication does not establish that those arguments are safe.

### How

#### 1. Establish the Need and Scope

Check whether the operation can run with ordinary user privileges. Identify the exact resource, required target user, intended change, and material side effects. Use `root` only when the operation requires it. Preserve existing task authorization; clarify only missing scope or effects that exceed it.

Confirm that `pkexec` is installed and that a usable system authentication agent or interactive terminal is available. If either prerequisite is missing, report it and continue unaffected work rather than installing tools or changing authorization policy solely to obtain access.

Complete this step when elevation is necessary, the operation is within the user's authorized scope, and the environment permits the execution path.

#### 2. Prepare One Reviewable Command

Use this invocation shape, resolving every placeholder before requesting authorization:

```text
pkexec --user <target-user> /absolute/path/to/program <explicit-arguments>
```

- Invoke a trusted system utility by its verified absolute path. Inspect unfamiliar executables and resolve symbolic links before elevation; do not elevate executables from a repository, download, or user-writable temporary directory.
- Keep exactly one command in the request and execution call. Run preparation and verification in separate calls. Shell command lists, pipelines, background execution, and redirections are prohibited in the elevated request, including `;`, `&&`, `||`, `|`, `&`, and newline-separated commands.
- Pass fixed, reviewed arguments. Prefer an argument-vector API; when a tool requires a shell string, quote literal arguments correctly. Resolve paths and target sets beforehand; exclude command substitution, backticks, process substitution, and unreviewed wildcard or variable expansion. Use `--` where the target utility supports it to separate options from operands.
- Invoke the utility that performs the approved operation directly. Do not elevate a shell, an interactive editor, interpreter code, or a command dispatcher to run arbitrary commands. Do not package multiple operations into a script, function, Make/task target, or wrapper to present them as one command. Always supply a program: bare `pkexec` can start a shell.
- Review the utility's actual scope, including implicit hooks, plugins, and affected resources. One executable invocation is not proof of one safe operation. Keep those effects within the disclosed task scope; exclude options that execute additional arbitrary commands.
- Prepare file content without elevation and review its diff before requesting the privileged write. Verify source content and destination paths, including symbolic links, before execution; if they change after review, review the changed state again. Use a direct file-writing utility for the write, rather than an elevated shell or heredoc.
- Use absolute resource paths and `pkexec`'s default working-directory and environment handling. Do not add `--keep-cwd` or restore caller-controlled environment variables through `env` to make a command work. Investigate a dependency on those settings and choose a supported invocation before requesting authorization.

Complete this step when the executable, target user, arguments, affected resources, and side effects are fixed and inspectable, and the request contains no hidden command execution.

#### 3. Request Authorization and Execute

Present the exact command, why elevation is required, and what it will change or expose. Include any material interruption, data-loss risk, or recovery limit. Request permission only for that invocation; exclude broad executable-prefix approvals or persistent access grants.

Let the user authenticate through the system-provided authentication interface. Never ask for, enter, store, or log an administrator password, and never pipe credentials into a process.

Execute exactly the reviewed invocation through the permitted tool after required approval. A changed executable, target user, argument, or resource requires a new scoped request. Cached Polkit authorization or the absence of a new password prompt does not broaden approval. Do not alter Polkit rules, sudoers, executable privilege bits, or authentication settings to reduce prompts or grant later commands access.

Complete this step when the command has finished and its output and exit status are available, or when cancellation, denial, or an execution failure has been identified. An authorization prompt alone does not prove execution.

#### 4. Verify the Result and Handle Failure

Verify the intended resource state in a separate, preferably unprivileged call. A zero exit status supports command completion; it does not by itself prove a service is healthy or that a wider workflow completed. If verification also requires elevation, submit it as another single-command request.

For `pkexec`, exit status `126` can indicate a dismissed authentication dialog, and `127` can indicate authorization or execution setup failure. The invoked program can also return those values: inspect diagnostics and observable state before assigning a cause or retrying.

After cancellation or denial, stop that privileged operation. Retry only when new user authorization or a verified change in prerequisites supports it; never automatically reprompt or switch privilege tools to evade the result. For interruption or uncertain execution, inspect possible partial effects before proposing a retry. Preserve the command, non-sensitive diagnostics, confirmed state, and next required action.

Complete the operation when verification supports the intended result, or report the precise unresolved condition and continuation path while continuing unaffected work.

### Examples

For a task that authorizes restarting the specific service, request only this command:

```bash
pkexec --user root /usr/bin/systemctl restart example.service
```

After it finishes, verify separately with an ordinary-user command:

```bash
/usr/bin/systemctl is-active example.service
```

Reject these request shapes; split the work into direct, separately reviewed commands:

```bash
pkexec --user root /usr/bin/systemctl restart example.service && /usr/bin/systemctl is-active example.service
pkexec --user root /bin/sh -c 'command-one; command-two'
pkexec --user root /bin/bash /tmp/batch-admin-operations.sh
```

When troubleshooting platform behavior, consult the installed `man pkexec` and the [Polkit pkexec manual](https://polkit.pages.freedesktop.org/polkit/pkexec.1.html).
