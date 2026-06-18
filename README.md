# TzQuant Investor Deck

面向专业投资人的商业计划书前端项目，采用编辑式设计语言，减少 AI/模板感。

## 本地预览

```bash
open index.html
```

或启动本地服务器（支持内网访问）：

```bash
python3 serve.py
# 自定义端口：python3 serve.py 9000
```

---

## GitHub 版本管理 + 公网部署完整教程

### 一、准备工作

1. 注册 [GitHub](https://github.com) 账号
2. 安装 Git：
   ```bash
   git --version
   ```
   如果没有安装，去 [git-scm.com](https://git-scm.com) 下载。

### 二、在 GitHub 创建仓库

1. 登录 GitHub，点击右上角 `+` → `New repository`
2. 填写仓库名，例如：`tzquant-bp`
3. 选择 **Public**（免费部署需要公开仓库）
4. 不要勾选 `Add a README file`（本地已有 README）
5. 点击 `Create repository`

### 三、本地初始化并推送代码

在终端进入项目目录：

```bash
cd /Users/zhangruige/Desktop/tzquant_bp

# 初始化 Git 仓库
git init

# 添加所有文件到暂存区
git add .

# 提交
git commit -m "Initial commit: TzQuant investor deck"

# 关联远程仓库（将下面的用户名换成你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/tzquant-bp.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 四、开启 GitHub Pages 公网部署

GitHub Pages 是免费的静态网站托管，最适合本项目。

1. 打开仓库页面，点击 `Settings`
2. 左侧菜单选择 `Pages`
3. 在 `Source` 下选择 `Deploy from a branch`
4. Branch 选择 `main`，文件夹选择 `/ (root)`
5. 点击 `Save`
6. 等待 1-3 分钟，页面会显示访问地址：
   ```
   https://YOUR_USERNAME.github.io/tzquant-bp/
   ```

### 五、后续更新流程

每次修改后执行：

```bash
git add .
git commit -m "更新内容描述"
git push origin main
```

GitHub Pages 会自动重新部署，通常 1 分钟内生效。

### 六、绑定自定义域名（可选）

1. 在域名服务商处添加 CNAME 记录：
   - 主机记录：`www` 或 `@`
   - 记录值：`YOUR_USERNAME.github.io`
2. 在项目根目录创建 `CNAME` 文件：
   ```bash
   echo "www.yourdomain.com" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```
3. 在 GitHub Pages 设置中勾选 `Enforce HTTPS`

### 七、其他部署方式

如果 GitHub Pages 访问较慢，也可以选择：

- **Vercel**：导入 GitHub 仓库即可自动部署，访问速度快
- **Netlify**：拖拽文件夹或连接 GitHub 仓库
- **Cloudflare Pages**：连接 GitHub 仓库，全球 CDN 加速

这些平台都支持自定义域名和 HTTPS。

---

## 设计特点

- **非 AI 感布局**：打破对称网格，使用编辑式排版
- **信息密度变化**：Hero 稀疏、产品/商业密集、traction 单句陈述
- **克制动效**：仅保留滚动渐入
- **全页统一 light 主题**，无中段反色翻转
- **真实图片占位**：`assets/hero.jpg`

## 文件结构

```
tzquant_bp/
├── index.html        # 页面结构
├── css/style.css     # 样式
├── js/main.js        # 微交互
├── assets/
│   ├── logo.svg      # 品牌标识
│   └── hero.jpg      # Hero 背景图
├── serve.py          # 本地服务器
├── start.sh          # 启动脚本
├── .gitignore        # Git 忽略文件
└── README.md         # 说明
```

## 替换素材

- `assets/hero.jpg`：替换为真实照片或品牌视觉图
- `index.html`：修改公司数据、团队介绍、融资金额、联系方式

## 许可证

示例内容仅供投资交流使用。
