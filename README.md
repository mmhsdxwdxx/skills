# mmhsdxwdxx/skills

可组合、可检查、可持续演进的个人 Agent Skills 合集。

这个仓库受 [mattpocock/skills](https://github.com/mattpocock/skills) 启发，但针对中文工作流、Codex、Windows 和跨 Agent 安装进行了调整。每个 skill 都保持小而独立；仓库负责分类、发现、版本、校验和安装。

## 安装

使用 [skills.sh](https://skills.sh/) 安装全部或选择单个 skill：

```bash
npx skills@latest add mmhsdxwdxx/skills
npx skills@latest add mmhsdxwdxx/skills --skill create-cn-official-pdf
```

维护者在本机开发时，可把仓库中的 skill 链接到 Agent 的本地目录，之后执行 `git pull` 即可更新：

```powershell
.\scripts\link-skills.ps1
```

```bash
./scripts/link-skills.sh
```

## 已发布 Skills

### 公文与办公

#### Model-invoked

- **[create-cn-official-pdf](./skills/official/create-cn-official-pdf/SKILL.md)** — 按 GB/T 9704—2012 排版、生成和验收中国党政机关公文 PDF。
- **[draft-cn-official-document](./skills/official/draft-cn-official-document/SKILL.md)** — 选文种、定方向、起草并预检公文内容，产出可移交渲染的 JSON。

## 体系约定

- `skills/official/`：正式发布的公文、政务与办公技能。
- `skills/engineering/`：正式发布的软件工程技能。
- `skills/productivity/`：正式发布的通用生产力技能。
- `skills/in-progress/`：尚在验证的草稿，不进入发布清单。
- `skills/deprecated/`：保留历史但不再安装。
- `docs/<bucket>/<skill>.md`：面向人的选择指南；`SKILL.md` 是给 Agent 执行的运行手册。
- `.agents/`：仓库治理、调用模式和维护约定。
- `.claude-plugin/`：Claude Code 插件兼容清单。
- `agents/openai.yaml`：每个 skill 的 Codex 展示与调用策略。

每个 skill 只能属于一种调用模式：

- **Model-invoked**：模型在任务匹配时可以自动调用；`description` 必须写清触发边界。
- **User-invoked**：只有用户显式调用；`agents/openai.yaml` 必须设置 `policy.allow_implicit_invocation: false`。

## 维护

新增或修改 skill 前阅读 [AGENTS.md](./AGENTS.md)。提交前运行：

```bash
python scripts/validate_skills.py
```

版本使用 Changesets 管理：

```bash
npm install
npx changeset
```

## 设计原则

1. 小而可组合：一个 skill 解决一个稳定问题。
2. 触发边界清晰：避免多个 skill 对同一请求争抢。
3. 标准与实现分离：详细知识放 `references/`，稳定动作放 `scripts/`。
4. 可验证：脚本必须实测，视觉产物必须渲染检查。
5. 可移植：不提交凭据、真实印章、个人数据或本机绝对路径。

## License

[MIT](./LICENSE)
