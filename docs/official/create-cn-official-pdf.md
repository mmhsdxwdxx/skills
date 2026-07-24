# create-cn-official-pdf

## 快速开始

```bash
npx skills@latest add mmhsdxwdxx/skills --skill create-cn-official-pdf
```

[源码](https://github.com/mmhsdxwdxx/skills/tree/main/skills/official/create-cn-official-pdf)

## 功能说明

将公文内容转换为符合 GB/T 9704—2012 基线的可打印 PDF，并将字体替代、印章缺失、附件不完整等问题显式写入验收报告。它不只是套用“仿宋三号”，而是同时控制 A4 版心、行字网格、红头、标题层级、落款、版记与单双页页码。

## 适用场景

可由用户显式调用 `$create-cn-official-pdf`；当任务涉及通知、请示、报告、函、批复、纪要、红头文件或公文 PDF 核验时，模型亦可自动调用。

## 前置条件

脚本运行需安装 Python 依赖（`reportlab`、`pypdf`，渲染可选 `PyMuPDF`），见技能目录下的 `requirements.txt`。正式印发还须在本机备有获得授权的准确字体，以及合法的机关版头与印章素材。本技能不会生成或仿造印章；缺少方正小标宋时，仅产出附带警告的草稿。

## 标准、地方规则与工程换算

本技能将三者分层记录：国家标准为基线，有效的上级或本机关模板优先，28.8、29 或 30 磅等行距值仅为实现 22 行版心的工程参数，不冒充全国统一条文。

## 验收标准

- PDF 为标准 A4，文字可搜索，字体资源可审计。
- 每页均已渲染为图片并完成目视检查。
- 版式偏差与素材缺口未被静默隐藏。

## 体系定位

这是 `official` 分类下的基础渲染与验收能力。后续可在同一分类增设公文起草、合法性审核、政策解读与机关模板适配等技能，并保持触发边界互不重叠。
