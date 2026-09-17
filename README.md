# Flow at Soft Interfaces

Zaicheng Zhang’s English-only research homepage at Beihang University, built with HTML and CSS. No JavaScript, dependencies, external fonts, language switch, or interactive menus.

网站地址：[zaichengzhang.github.io](https://zaichengzhang.github.io/)。发布仓库：[zaichengzhang/zaichengzhang.github.io](https://github.com/zaichengzhang/zaichengzhang.github.io)，使用 `main` 分支根目录。

## 页面内容

页面仅保留研究简介、Research、Preprints 和 Publications。邮箱、Google Scholar 链接及单位信息位于个人介绍下方，顶部 Contact 导航直接定位到这里。沿用暖白、墨蓝和少量陶土色，保留一张科研示意图；手机导航直接显示，不需要展开菜单。

```text
academic-homepage/
├── index.html               # 全部英文内容
├── assets/
│   ├── css/style.css        # 页面样式和移动端布局
│   └── images/
│       ├── favicon.svg
│       ├── soft-interface-v4.png # 上下流线不对称、较柔和的科研概念图
│       └── IMAGE_NOTES.md     # 图像生成说明和完整提示词
├── CONTENT_SOURCES.md       # 论文与个人资料的核对来源
├── .nojekyll
├── .gitignore
└── README.md
```

## 修改内容

姓名、单位、邮箱和 Google Scholar 链接已填写。主页现收录已核实的 23 篇独立文章：20 篇正式文章（含一篇法文综述性文章）和 3 篇预印本。预印本单列在 Preprints，按首次公开日期倒序；正式文章列在 Publications，按最终期刊出版年份分组倒序，同年按已知出版日期排序。两部分独立倒序编号，标题链接到 DOI 或 arXiv。已合并同一工作的预印本与期刊版本。Google Scholar 暂时无法直接读取；当前文章清单的覆盖范围、来源和核对限制见 `CONTENT_SOURCES.md`。

全部内容都在 `index.html` 中，可直接编辑，无需维护翻译或运行脚本。更新姓名或研究范围时，也请同步修改文件开头的标题和网页描述。

### 更新论文

每个 `section class="publication-year"` 是一个年份分组，其中 `ol class="publication-list"` 的每个 `li` 对应一篇文章，依次包含标题链接、作者和期刊信息。可复制一个已有条目，再替换为经核对的真实记录。作者顺序保持原文顺序，自己的姓名以 `<strong>Zaicheng Zhang</strong>` 显示为墨蓝色粗体。两部分分别从最新文章倒数编号，编号互不混用；新增或移动文章后，更新相应年份列表的 `start` 值。预印本只出现在 Preprints，期刊信息行明确标为 `Preprint`。每次更新都逐篇检查 Preprints 中的全部文章，不能只检查本月新加入的条目。核实正式期刊版本后，将文章移入 Publications，替换标题、作者、日期、期刊、卷页或文章号和 DOI，移除原预印本条目，并调整年份和编号；已上线的正式 Early Access / Online First 文章可按正式发表处理，尚无卷页时仅显示已确认信息。仅被接收、投稿状态变化或 arXiv 版本更新，不等于正式发表。访问受阻或匹配不明确时保留预印本并记录待核查原因；Preprints 为空时可隐藏该区域和导航链接。

### 首页图片

当前图片为 `assets/images/soft-interface-v4.png`，已用内置图像生成工具重新修整为较细、平滑、两端渐隐的流线，去掉箭头，保留上下不对称形态，以及柔和的灰青、墨蓝和铜色。它是大体表达近界面流动约束的概念图，不是实验图像、数值流场或定量变形解。生成说明与完整修改提示词见 `assets/images/IMAGE_NOTES.md`。

## 本地预览

双击 `index.html`，直接用浏览器打开即可。如果已打开旧版，请刷新页面。所有页面内容均为英文，本说明保留中文以便维护。

## GitHub Pages 部署

以下步骤根据 GitHub 官方文档核对于 **2026-09-14**。不需要 Jekyll、Node.js 或包管理器。

### 方法 A：通过 GitHub 网页上传

1. 登录 GitHub，新建仓库，名称为 **`username.github.io`**，其中 `username` 换成你的 GitHub 用户名；用户名含大写字母时仓库名使用小写。使用 GitHub Free 时选择 **Public**。
2. 打开仓库，通过 **Add file → Upload files** 上传解压后 `academic-homepage` **文件夹内的内容**。`index.html` 必须直接位于仓库根目录，不要多套一层文件夹，也不要只上传 ZIP。
3. 确认 `.nojekyll` 一并上传。它是空的隐藏文件；macOS Finder 可用 `Command + Shift + .` 显示隐藏文件。如果网页上传没有带上它，可在 GitHub 中通过 **Add file → Create new file** 新建名为 `.nojekyll` 的空文件并提交。`.gitignore` 可同样上传。
4. 进入 **Settings → Pages → Build and deployment**：Source 选择 **Deploy from a branch**；Branch 选择 **main**；目录选择 **/ (root)**；点击 **Save**。
5. 等待 GitHub 完成部署，在 Pages 设置中打开显示的网站地址：`https://username.github.io/`。首次发布和后续更新可能需要约 10 分钟。
6. 以后修改文件并提交至 `main`，网站会自动更新。可在仓库 **Actions** 中查看部署状态。

如将文件放入其他名称的项目仓库，页面也兼容 `https://username.github.io/repository/` 形式的子路径，因为资源使用相对路径。

如果之前已经上传过旧版，可删除不再使用的 `assets/js/main.js`、三个 `research-*.svg` 文件及旧图 `soft-interface.png`，并覆盖本项目中的同名文件。不要删除你自行添加的论文、照片或其他资料。

官方参考：[创建 GitHub Pages 站点](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)、[配置发布来源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。
