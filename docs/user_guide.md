# Auto-Scholar 用户指南

## 快速开始

### 1. 环境配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# LLM_API_KEY=your-api-key-here
```

### 2. 启动服务

```bash
# 后端
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000

# 前端（新终端）
cd frontend && npm install && npm run dev
```

### 3. 访问应用

打开浏览器访问 http://localhost:3000

## 使用流程

### Step 1: 输入研究主题

在左侧控制台输入你的研究主题，例如：
- "transformer architecture in natural language processing"
- "深度学习在医学影像中的应用"

### Step 2: 选择数据源

可选择搜索的论文数据库：
- **Semantic Scholar** (默认) - 最全面的元数据
- **arXiv** - 预印本，最新研究
- **PubMed** - 生物医学领域

### Step 3: 审核候选论文

系统会搜索并展示候选论文列表。你可以：
- 查看论文标题、作者、年份、摘要
- 勾选要纳入综述的论文
- 点击"确认选择"继续

### Step 4: 等待生成

系统会：
1. 提取每篇论文的核心贡献
2. 生成结构化文献综述
3. 进行引用验证（QA 检查）

### Step 5: 查看和导出

- 在右侧工作区查看生成的综述
- 悬停引用 [N] 查看论文详情
- 点击"导出"下载 Markdown 或 Word 文档

## 常见问题

### Q: 生成的综述是中文还是英文？

取决于你选择的输出语言。在输入框下方可以切换：
- **English** - 生成英文综述
- **中文** - 生成中文综述

### Q: 为什么搜索结果很少？

可能原因：
1. 关键词过于具体 → 尝试更宽泛的主题
2. 数据源限制 → 尝试启用多个数据源
3. API 限流 → 稍后重试

### Q: 引用格式可以修改吗？

导出时可选择引用格式：
- **APA** - 心理学、社会科学
- **MLA** - 人文学科
- **IEEE** - 工程、计算机科学
- **GB/T 7714** - 中国国家标准

### Q: 生成超时怎么办？

如果出现"研究超时"错误：
1. 减少批准的论文数量（建议 3-5 篇）
2. 检查网络连接
3. 稍后重试

### Q: 可以继续之前的研究吗？

可以。点击左侧"历史记录"查看之前的研究会话，点击即可恢复。

### Q: 如何进行多轮对话？

生成综述后，可以在输入框继续提问，例如：
- "请补充关于 attention 机制的内容"
- "请用更学术的语言重写第二段"

系统会基于已有内容进行更新。

## 故障排除

### 错误: "LLM_API_KEY environment variable is required"

**原因**: 未配置 API Key

**解决**:
```bash
# 方法 1: 设置环境变量
export LLM_API_KEY=your-api-key-here

# 方法 2: 编辑 .env 文件
echo "LLM_API_KEY=your-api-key-here" >> .env
```

### 错误: "Connection refused" 或 "Network error"

**原因**: 后端服务未启动

**解决**:
```bash
# 确保后端正在运行
uvicorn backend.main:app --reload --port 8000
```

### 错误: "Rate limit exceeded"

**原因**: API 调用频率过高

**解决**:
1. 等待 1-2 分钟后重试
2. 如果使用 Semantic Scholar，考虑申请 API Key

### 前端显示空白

**原因**: 前端构建失败或端口冲突

**解决**:
```bash
cd frontend
rm -rf .next node_modules
npm install
npm run dev
```

## 性能优化建议

1. **论文数量**: 建议每次批准 3-5 篇论文，过多会增加处理时间
2. **数据源选择**: 如果只需要特定领域，选择单一数据源更快
3. **网络环境**: 稳定的网络连接可减少超时风险

## 联系支持

如遇到其他问题，请：
1. 查看 [GitHub Issues](https://github.com/your-repo/auto-scholar/issues)
2. 提交新 Issue 并附上错误日志
