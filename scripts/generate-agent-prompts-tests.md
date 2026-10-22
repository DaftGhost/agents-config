# 提示词生成向导：测试用例

本文是 [generate-agent-prompts.sh](generate-agent-prompts.sh) 的独立测试用例规格，功能与规则见 [generate-agent-prompts.md](generate-agent-prompts.md)。后续修改功能时，先更新用例，再据此修改实现和编写测试。

## 通用约定

除用例另有说明外均适用：

- 每个用例在隔离目录和隔离用户目录中，通过交互终端驱动向导；目标与 aside 的内容以 JSON 字符串表示。
- 默认夹具：共享指令为 `"# Base\nshared\n"`；普通目标 A、B、C 的内容为 `original`；aside 为 `"## Rule\nnew\n"`。默认追加结果为 `"original\n\n## Rule\nnew\n"`，默认替换结果为 `"# Base\nshared\n\n\n## Rule\nnew\n"`。
- 成功完成的运行退出状态为 `0`，被拒绝或失败的运行退出状态非零。
- 运行结束后不留预览、快照或准备中的临时输出。
- 被拒绝、跳过或写入失败的目标保持原始字节、存在状态和权限位。

## 1. 章节合并

通用条件：目标是可读写的 UTF-8 普通文件，每个用例只选一个 aside。操作：选择追加模式和该目标，选择 aside，核对预览后回答 `y`。预期：预览与写入后的目标内容均等于“输出”列。

| 编号 | 验证点 | 目标内容 | aside | 输出 |
| --- | --- | --- | --- | --- |
| TC-001 | 覆盖首次匹配的正文与子章节，保留后续重复标题 | `"Intro\n## Rule\nold\n### Child\nold child\n## Keep\nkeep\n## Rule\nsecond\n"` | `"## Rule\nnew\n### New child\nnew child\n"` | `"Intro\n## Rule\nnew\n### New child\nnew child\n## Keep\nkeep\n## Rule\nsecond\n"` |
| TC-002 | 匹配不要求父标题相同 | `"# Parent\n## Rule\nold\n# Next\nkeep\n"` | `"## Rule\nnew\n"` | `"# Parent\n## Rule\nnew\n# Next\nkeep\n"` |
| TC-003 | 名称相同、层级不同不覆盖 | `"# Rule\nkeep\n"` | `"## Rule\nnew\n"` | `"# Rule\nkeep\n\n## Rule\nnew\n"` |
| TC-004 | 标题名称区分大小写 | `"## rule\nkeep\n"` | `"## Rule\nnew\n"` | `"## rule\nkeep\n\n## Rule\nnew\n"` |
| TC-005 | 忽略标题两端空白与合法的关闭井号 | `"  ##   Rule \t ###  \nold\n## Keep\nkeep\n"` | `"## Rule\nnew\n"` | `"## Rule\nnew\n## Keep\nkeep\n"` |
| TC-006 | 没有前置空白的末尾井号属于标题文字 | `"## Rule#\nkeep\n"` | `"## Rule\nnew\n"` | `"## Rule#\nkeep\n\n## Rule\nnew\n"` |
| TC-007 | 反引号围栏内的标题和较短围栏不参与匹配 | `````"````\n## Rule\n```\n## Keep\n````\n## Rule\nold\n````\n## Rule\n```\n## Keep\n````\n## Last\nkeep\n"````` | `"## Rule\nnew\n"` | `````"````\n## Rule\n```\n## Keep\n````\n## Rule\nnew\n## Last\nkeep\n"````` |
| TC-008 | 波浪线围栏内的标题和较短围栏不参与匹配 | `"~~~~\n## Rule\n~~~\n## Keep\n~~~~\n## Rule\nold\n~~~~\n## Rule\n~~~\n## Keep\n~~~~\n## Last\nkeep\n"` | `"## Rule\nnew\n"` | `"~~~~\n## Rule\n~~~\n## Keep\n~~~~\n## Rule\nnew\n## Last\nkeep\n"` |
| TC-009 | 四个空格缩进的标题不参与匹配 | `"    ## Rule\n    example\n"` | `"## Rule\nnew\n"` | `"    ## Rule\n    example\n\n## Rule\nnew\n"` |
| TC-010 | 空目标文件与缺少末尾换行的 aside | `""` | `"## Rule\nnew"` | `"## Rule\nnew\n"` |
| TC-011 | 原文缺少末尾换行时补齐分隔 | `"original"` | `"## Rule\nnew"` | `"original\n\n## Rule\nnew\n"` |
| TC-012 | 未覆盖区域保留原始换行 | `"Intro\r\n## Rule\r\nold\r\n## Keep\r\nkeep\r\n"` | `"## Rule\nnew\n"` | `"Intro\r\n## Rule\nnew\n## Keep\r\nkeep\r\n"` |

- **TC-013 选择顺序决定同名模块的最终内容**：目标为 `"Intro\n"`，三个 aside 依次为 `["## Rule\nfirst\n", "## Other\nother\n", "## Rule\nlast\n"]`。按此顺序合并并确认，再对所得文件以相同顺序合并一次。两次输出均为 `"Intro\n\n## Rule\nlast\n\n## Other\nother\n"`。
- **TC-014 重复追加不同章节时不改变分隔空行**：三个目标均为 `"Intro\n"`，各选两个 aside；第二个均为 `"## Second\nsecond\n"`，第一个分别为 `"## First\nfirst\n"`、`"## First\nfirst\n\n"`、`"## First\nfirst\r\n\r\n"`。确认第一次追加并记录输出，再以相同顺序重复追加。第一次输出包含前言和两个完整章节；第二次与各自第一次的输出一致。
- **TC-015 未选择 aside 不改变目标**：目标为无末尾换行的 `original`，记录字节与权限位。追加模式下 aside 输入空行。提示未选择 aside，不要求写入确认，退出状态 `0`，不留临时文件。
- **TC-016 非法 aside 结构拒绝全部写入**：三个子场景各有目标 A、B（`first original`、`second original`），aside 内容分别为 `"no heading"`、`"Intro\n## Rule\nbody\n"`、`"## Rule\nbody\n## Other\nbody\n"`。追加模式选择 A、B，等待预览生成。均报告章节结构错误，不进入写入阶段。
- **TC-017 目标或 aside 的围栏未关闭时拒绝写入**：场景一的目标为 ````"```\n## Rule\nexample\n"````；场景二的目标为 `"original\n"`，aside 为 ````"## Rule\n```\nexample\n"````。追加模式选择目标和 aside，等待预览生成。均报告未关闭围栏。

## 2. 目标选择、确认与写入

- **TC-018 默认替换模式处理普通文件、链接及新路径**：A 为普通文件 `old`，B 为指向 `linked original` 文件的链接，C 及其父目录不存在；aside 编号 `1` 为默认 aside，`2` 为 `"## Other\nother\n"`。模式输入空行，选择 A、B、C，aside 输入 `2,1`，核对预览后依次回答 `y`、`Y`、`y`。三个目标均为 `"# Base\nshared\n\n\n## Other\nother\n\n\n## Rule\nnew\n"`，权限 `0644`；B 变为普通文件，原指向文件仍为 `linked original`；C 及其父目录创建成功。
- **TC-019 替换模式未选择 aside 时只写入共享指令**：替换模式选择 A，aside 输入空行，回答 `y`。预览和目标均为 `"# Base\nshared\n"`，没有额外分隔空行。
- **TC-020 每个追加目标单独预览并保留权限**：A 为 `"first\n## Rule\nold\n## Keep\nkeep\n"`，权限 `0640`；B 为 `"second\n"`；aside 为 `"## Rule\nnew\n### Child\nnew child\n"`。追加模式选择 A、B，检查两份预览后分别回答 `y`。A 保留前言与 Keep，Rule 全段更新；B 保留前言，并在一个分隔空行后追加整个 aside；预览不含共享指令；A 权限仍为 `0640`；写入内容与各自预览一致。
- **TC-021 拒绝追加保持原文，且不阻止后续目标**：A、B 分别为无末尾换行的 `declined original`、`approved original`。追加模式，对 A 回答 `n`，对 B 回答 `y`。A 不变并报告跳过；B 为 `"approved original\n\n## Rule\nnew\n"`。
- **TC-022 追加跳过各类链接和不存在的路径**：A 是指向 `linked original` 文件的链接，B 指向不存在的文件，C 指向已有目录，D 不存在。追加模式选择 A、B、C、D。逐项给出跳过原因，不询问写入确认；A、B、C 仍为原链接，A 指向的文件不变，D 不创建。
- **TC-023 跳过路径、拒绝文件和确认文件混合处理**：A 不存在，B、C 分别为 `declined original`、`approved original`。追加模式选择 A、B、C，A 自动跳过，对 B 回答 `n`，对 C 回答 `y`。A 不创建，B 不变，C 为 `"approved original\n\n## Rule\nnew\n"`；每个预览和写入对应正确路径。
- **TC-024 替换模式拒绝首个目标不影响后续创建**：A 为 `original`，B 不存在。替换模式选择 A、B，不选 aside；对 A 回答 `n`，对 B 回答 `y`。A 不变；B 创建，内容为 `"# Base\nshared\n"`。
- **TC-025 确认提示只接受单个 y 或 Y**：追加模式，各子场景的确认回答分别为 `y`、`Y`、空行、`yes`、` y `。只有 `y`、`Y` 写入默认追加结果，其余回答保留 `original`。
- **TC-026 预览后正文变化时拒绝覆盖**：追加模式显示完整预览后，将 A 改为 `edited while reviewing`，再回答 `y`。报告目标在审核后变化，A 仍为 `edited while reviewing`。
- **TC-027 预览后目标类型变化或消失时拒绝写入**：另有内容为 `keep` 的独立文件。追加模式显示完整预览后，三个独立场景分别将 A 改成指向该文件的链接、删除 A、改成目录，再回答 `y`。新链接与 `keep` 文件不变，已删除的目标不重建，新目录不被替换。
- **TC-028 两种模式都可以在没有 Python 的环境运行**：环境中有 Bash 和必要的文件工具，找不到 `python3`。先以追加模式运行，退出后以替换模式对同一目标运行并确认写入。目标先后为默认追加结果、默认替换结果；两种模式都不调用 Python 或其他脚本解释器。
- **TC-029 中断确认时清理预览与快照**：追加模式生成预览后、确认前，两个独立场景分别发送 `SIGINT`、`SIGTERM`。退出状态分别为 `130`、`143`，A 仍为 `original`。

## 3. 输入校验与失败场景

- **TC-030 非交互输入被拒绝**：以管道或普通文件作为标准输入启动向导。提示必须在交互终端运行，不进入目标选择，不修改任何目标。
- **TC-031 模式与编号非法时重新询问**：aside 为 `"## First\nfirst\n"`、`"## Second\nsecond\n"`。模式依次输入 `3`、`2`；目标选择依次输入空行、`0`、`x`、`5`，再提供 A 的绝对路径并以空行结束；aside 依次输入 `3`、`x`、`1`；最后拒绝写入。每个非法输入都在当前阶段要求重新输入，合法输入进入下一阶段，A 不变。
- **TC-032 预设目标及 all 的范围**：四个预设路径各有内容为 `original` 的普通文件。追加模式下两个独立场景的目标分别输入 `2,1`、`all`，对每个目标拒绝写入。场景一依次预览 Codex、Claude；场景二按 Claude、Codex、Shared agents、DSH 的顺序预览，不询问自定义路径；所有目标不变。
- **TC-033 自定义路径校验与结束输入**：A 为普通文件，B 为目录，C 为非普通且非链接的路径，D 为普通文件。追加模式选择自定义目标，依次输入空行、`notes.md`、以 `/` 结尾的路径、B、C、D 下的子路径、A 的绝对路径、空行；随后不选 aside。第一次空行和所有非法路径都要求继续输入；接受 A 后，空行结束路径输入；所有路径不变。
- **TC-034 展开用户目录路径且去除重复选择**：用户目录中有 `notes.md`（`original`）；aside 编号 `1` 为 `"## First\nfirst\n"`，`2` 为 `"## Second\nsecond\n"`。追加模式自定义输入 `~/notes.md` 和同一文件的绝对路径，aside 输入 `2,1,2`，确认。目标只预览、确认和写入一次，aside 按 2、1 的顺序各处理一次；目标为 `"original\n\n## Second\nsecond\n\n## First\nfirst\n"`。
- **TC-035 源文件路径不能作为目标**：选择自定义目标，依次输入共享指令的绝对路径、一个已发现 aside 的绝对路径、A 的绝对路径和空行，随后拒绝写入 A。两个源路径被拒绝，只有 A 进入目标列表；源文件和 A 的字节不变。
- **TC-036 替换模式缺少共享指令时拒绝运行**：仓库副本缺少 `.agents/AGENTS.md`。交互启动，模式选择 `1`。报告共享指令不存在，目标不变。
- **TC-037 读取或 UTF-8 解码失败时不写入目标**：三个独立场景分别为 aside 无法读取、B 含非法字节 `0xFF`、aside 含非法字节 `0xFF`。追加模式选择 A、B 和该 aside，让失败发生在预览生成阶段。报告读取或编码错误，A、B 保持原始字节。
- **TC-038 待创建目标在确认后出现时拒绝替换**：A 不存在，B 已存在。替换模式选择 A、B，不选 aside；确认创建 A，在 B 的确认提示处暂停，另建 A 并写入 `concurrent content`，再拒绝写入 B。写入阶段报告 A 已出现；A 仍为 `concurrent content`，B 不变。
- **TC-039 替换符号链接失败时恢复原链接**：A 是指向 `linked original` 文件的链接；可令向 A 安装临时输出的移动操作失败，而原链接的移开与恢复可正常完成。替换模式选择 A，不选 aside，确认；原链接移开后，让安装输出失败一次。报告写入失败；A 恢复为原链接，指向的文件仍为 `linked original`。
- **TC-040 链接恢复也失败时保留恢复位置**：前置同 TC-039，但可分别令安装输出与恢复链接的移动操作失败。确认替换，让两者连续失败。报告原链接保留的路径，该路径仍是原链接，指向的文件不变；不删除可供人工恢复的链接。
- **TC-041 多个目标中的后续写入失败**：可令 B 的输出安装失败。追加模式选择 A、B、C，全部确认，A 完成写入后让 B 的安装失败。报告 B 失败，不声称全部完成；A 为默认追加结果，B、C 仍为 `original`。
- **TC-042 全部仓库 aside 可以重复合并**：各 aside 均为单个主标题加子章节；将共享指令复制到隔离目录的普通目标并记录前缀字节。追加模式选择全部发现的 aside，确认写入并记录结果，再以相同选择和顺序重复一次。共享指令前缀保留，全部 aside 章节存在，第二次结果与第一次逐字节一致。
- **TC-043 阶段进度与结束汇总完整**：终端支持 ANSI 清屏。以替换模式选择 A、不选 aside，逐阶段确认写入。依次展示 `Stage 1/4` 至 `Stage 4/4`，切换阶段时清屏；最终汇总 A 的写入结果，A 为 `"# Base\nshared\n"`。
- **TC-044 单个脚本支持两种模式，加载函数不启动交互**：隔离目录只有向导脚本、共享指令和 aside，A 为 `"## Rule\nold\n"`。先在无交互终端的环境中用 Bash `source` 加载向导，检查 A 和目录内容；再通过交互终端依次以追加和替换模式选择 A 和 aside，核对预览并确认。加载时正常返回，不出现提示、不创建临时文件、不修改 A；追加后 A 为 `"## Rule\nnew\n"`，替换后为默认替换结果。
