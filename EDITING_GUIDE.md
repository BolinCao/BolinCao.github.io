# 学术主页快速修改指南

这个网站只有两个主要页面：

- 英文主页：`_pages/about.md`
- 中文主页：`_pages/about-zh.md`

英文主页发布在 `https://bolincao.github.io/`，中文主页发布在 `https://bolincao.github.io/zh/`。两个页面顶部的语言按钮可以互相切换。

## 最快的修改方法

1. 打开 GitHub 仓库：`https://github.com/BolinCao/BolinCao.github.io`
2. 点击需要修改的文件，例如 `_pages/about.md`。
3. 点击右上角铅笔图标 **Edit this file**。
4. 直接修改文字。
5. 点击 **Commit changes** 保存。
6. GitHub Pages 通常会在几分钟内自动更新网站。

修改英文内容时，同步修改 `_pages/about-zh.md` 中对应的中文内容，避免两种语言的信息不一致。

## 添加一篇论文

在两个主页文件的 `Publications` 或 `学术论文` 标题下，复制一条现有编号条目，替换作者、年份、标题和期刊信息。Markdown 格式示例：

```markdown
1. Cao, B., ... (2026). Article title. *Journal Name, 10*(2), 1–10.
```

论文较多时不需要手动修改所有编号；保持每条以 `1.` 开头，网页会自动连续编号。

## 修改个人信息或链接

- 姓名、简介、学校、论文和奖项：修改两个 `about` 文件。
- 网站标题、头像、Google Scholar、GitHub 等：修改 `_config.yml`。
- 中英文切换导航：修改 `_data/navigation.yml`。
- 页面颜色、间距和字体：修改 `assets/css/main.scss`。

## 注意事项

- 文件顶部两行 `---` 之间的内容是网页配置，不要随意删除。
- 英文主页的 `permalink: /` 和中文主页的 `permalink: /zh/` 不要修改。
- 保存后如果网页没有立即变化，等待几分钟后刷新浏览器。
