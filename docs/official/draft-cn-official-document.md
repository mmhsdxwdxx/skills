# draft-cn-official-document

## 快速开始

```bash
npx skills@latest add mmhsdxwdxx/skills --skill draft-cn-official-document
```

[源码](https://github.com/mmhsdxwdxx/skills/tree/main/skills/official/draft-cn-official-document)

## 功能说明

起草中国党政机关公文的内容：依据《党政机关公文处理工作条例》从十五种法定文种中选定，确定行文方向，组织结构，把控措辞与标点，做内容预检，并产出可直接移交 `$create-cn-official-pdf` 渲染的 JSON。本技能负责“写”，不负责“排”。

## 适用场景

可由用户显式调用 `$draft-cn-official-document`；当任务涉及起草、拟稿、写通知/请示/报告/函/纪要、公文写作、措辞或内容结构化时，模型亦可自动调用。若用户只要求对已成稿内容排版出 PDF，应改用 `$create-cn-official-pdf`。

## 前置条件

无需特殊字体或印章素材。起草依据《党政机关公文处理工作条例》与现行国标对文种、行文、语言的规定（见 `references/`）；引用的政策、法规、名称、日期须可核实，不可杜撰。预检脚本仅需 Python 标准库。

## 文种、方向与预检

- 文种：从十五种法定文种中按用途选定，不以模板形似为准。
- 方向：上行、下行、平行/不相隶属、公开发布、会议纪要，对应不同的主送、签发与抄送要求。
- 预检：`scripts/check_draft.py` 自动检查结构（schema、`〔〕`括号、请示单主送、报告不夹带请示、日期不补零、标题层级不跳级）；政策时效、管辖权、会签完备性等需人工对照清单复核。

## 与渲染器的衔接

产出的 JSON 即与 `$create-cn-official-pdf` 的契约：须含 `format`（`general`/`upward`/`letter`/`order`/`minutes`），上行文须含签发人；`seal_image` 留空，除非用户提供授权印章。字体、页边距、版心等排版参数由渲染器负责。

## 验收标准

- 文种与行文方向正确，符合法定用途。
- 请示一文一事一主送；报告未夹带请示事项。
- 文号用 `〔〕`，日期不补零，标点全角，标题层级有序。
- 事实与引用可核实；`check_draft.py` 无未决告警。

## 体系定位

这是 `official` 分类下的内容起草能力，与 `$create-cn-official-pdf`（排版与验收）通过 JSON 衔接，触发边界互不重叠（写 vs 排）。后续可增设合法性审核、政策解读与机关模板适配等技能。
