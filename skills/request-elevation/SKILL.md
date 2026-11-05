---
name: request-elevation
description: Request narrowly scoped command elevation for authorized macOS and Linux administration tasks. Use when an operation requires administrator or another user's OS privileges, including protected file changes, system service management, or recovery from a confirmed OS permission failure. Distinguish OS privileges from sandbox or agent approval before selecting a platform-specific authentication path.
disable-model-invocation: false
user-invocable: true
---

# Request Elevation

Elevate only a necessary, task-authorized OS operation through an execution path the environment permits. Keep each request and execution call limited to one reviewed operation; prepare and verify in separate calls.

## 1. Establish the Permission Boundary

Identify the resource, required target user, intended effect, and why ordinary user privileges are insufficient. If ordinary privileges suffice, execute without elevation and skip the platform procedures. Use `root` only when required. Preserve existing task authorization; clarify missing scope or effects that exceed it.

Distinguish OS permissions from sandbox or agent restrictions. For the latter, follow [Request Required Permissions and Continue](../../aside/tools/request-required-permissions-and-continue.md) through the environment's approval mechanism. OS elevation cannot replace that approval or bypass a rejection.

Complete this step when evidence establishes the boundary, required identity, authorized scope, and permitted execution path.

## 2. Load the Platform Procedure

Detect the OS of the host that will execute the command, including a remote host when applicable. Read only its reference before selecting or constructing an elevated invocation:

- **Linux:** read [Linux elevation](references/linux.md) for `pkexec` and the conditions for choosing `sudo`.
- **macOS:** read [macOS elevation](references/macos.md) for terminal authentication and system authentication dialogs.

Read [sudo execution](references/sudo.md) only when the platform procedure selects `sudo`. If a required utility or authentication interface is unavailable, report the prerequisite; do not install privilege tools or change authentication policy solely to obtain access.

Complete this step when the applicable procedure has been read and its executable, target-user support, and authentication prerequisites are verified.

## 3. Prepare One Reviewable Operation

- Use bare command names resolved through the PATH configured for the actual execution environment. Verify command availability there, and keep executable names bare in reviews and invocations rather than assuming installation paths. Inspect unfamiliar commands and symbolic links; exclude executables from repositories, downloads, or user-writable temporary directories.
- Fix the target user, literal arguments, absolute resource paths, and affected resources. Prefer an argument-vector API; otherwise quote each literal argument for every parser it crosses. Use `--` where the target utility supports it. Resolve target sets before approval rather than relying on wildcard, variable, or command expansion.
- Invoke the utility directly, except for the minimal authentication transport required by the platform reference. Keep command lists, pipelines, redirections, background execution, substitutions, and arbitrary shell/interpreter code out of the elevated operation. Do not disguise multiple operations as a script, task target, or wrapper. Inspect implicit hooks, plugins, and options that could execute additional commands.
- Prepare file content without elevation and review its diff. Verify source content, destination, and symbolic links before the privileged write; review again if they change. Use a direct file-writing utility rather than an elevated shell or heredoc.
- Use the selected mechanism's documented working-directory and environment behavior. Check command lookup in that execution context rather than assuming it inherits the caller's PATH. Investigate environment dependencies; do not restore caller-controlled variables or preserve the environment broadly to make elevation work.

Complete this step when the executable, arguments, target identity, resources, side effects, and any required authentication wrapper are fixed and inspectable.

## 4. Obtain Approval and Execute

Present the exact invocation, elevation reason, and what it will change or expose, including material interruption, data-loss risk, or recovery limits. Obtain any required approval for that invocation through the environment's mechanism. Exclude broad executable-prefix approvals and persistent access grants.

Let the user authenticate directly through the system interface or an interactive terminal they control. Never request, enter, store, log, or pipe an administrator password. Cached authentication or the absence of a prompt does not expand task authorization. Do not change Polkit rules, sudoers, executable privilege bits, or authentication settings to reduce prompts or authorize later commands.

Execute exactly the reviewed invocation. Changed arguments, executable, identity, or resource require a new scoped review and any required approval.

Complete this step when output and exit status are available, or cancellation, denial, or execution failure has been identified. A prompt or successful authentication alone does not prove execution.

## 5. Verify and Report

Verify the intended resource state in a separate, preferably unprivileged call. If verification needs elevation, request it as another single operation. A zero exit status supports command completion, not service health or completion of a wider workflow.

Use the selected reference and diagnostics to distinguish cancellation, authorization failure, and program failure. Stop the privileged operation after cancellation or denial; retry only with new user authorization or a verified prerequisite change. Do not automatically reprompt or switch tools to evade the result. Inspect possible partial effects before retrying an interrupted or uncertain operation.

Finish when verification supports the intended result. Otherwise report the exact blocker, non-sensitive diagnostics, confirmed and uncertain effects, and the next required action; continue unaffected work.
