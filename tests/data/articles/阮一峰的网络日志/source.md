阮一峰的网络日志 » [首页](http://www.ruanyifeng.com/blog/) »
[档案](http://www.ruanyifeng.com/blog/archives.html)

[![](https://wangbase.com/blogimg/asset/202107/bg2021072117.png)
](/feed.html?utm_source= "订阅Feed")

- 上一篇：[科技爱好者周刊（第 3](http://www.ruanyifeng.com/blog/2025/04/weekly-issue-345.html "科技爱好者周刊（第 345 期）：HDMI 2.2 影音可能到头了")
- 下一篇：[巨头的新战场：AI 编](http://www.ruanyifeng.com/blog/2025/04/trae-mcp.html "巨头的新战场：AI 编程 IDE（暨 字节 Trae 调用 MCP 教程）")

分类：

- [开发者手册](http://www.ruanyifeng.com/blog/developer/)

- [⇐](http://www.ruanyifeng.com/blog/2025/04/weekly-issue-345.html "科技爱好者周刊（第 345 期）：HDMI 2.2 影音可能到头了")
- [⇒](http://www.ruanyifeng.com/blog/2025/04/trae-mcp.html "巨头的新战场：AI 编程 IDE（暨 字节 Trae 调用 MCP 教程）")

# 办公类 AI 初探：扣子空间

作者： [阮一峰](http://www.ruanyifeng.com)

日期： [2025年4月21日](http://www.ruanyifeng.com/blog/2025/04/)

## 一、AI 的风口

问问大家，AI 产品的风口是什么？

我的意思是，什么样的产品有最大的机会。

现在的 AI 多如过江之鲫，大部分都是昙花一现，走不远。

在我看来，最有机会的产品，既不是面向普通大众的问答类 AI，或者内容生成 AI，也不是面向开发者（API 用户）的编程 AI。

**真正的风口是办公类 AI** 。

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025041901.webp)

企业和个人的办公市场巨大无比，而且有真金白银。

谁能把 AI 引入文档、会议、决策......，谁就会吃到肉。就像 Office 软件是商业软件之王一样，企业级办公 AI 也一定会是 AI 的销售之王。

## 二、办公类 AI 的现状

不过，办公类 AI 眼下寥寥无几。不要说赢得市场，就连想得起名字的产品都不多。

究其原因，一是 AI 现阶段的能力，还达不到企业级软件的安全、稳定、准确、高效。

二是办公类 AI 到底是什么样的产品形态，大家还在摸索。

我一直非常关注这个领域，对于新出现的办公类 AI 有着强烈的兴趣。

下面介绍一个新产品"[扣子空间](https://space.coze.cn/)"，我这些天一直在试用。大家看看，它怎么用 AI 完成办公任务。

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025041902.webp)

## 三、扣子空间

先说一下，[扣子](https://www.coze.cn/home)（coze.cn）是一个国内的平台，提供基于浏览器的低代码环境，来搭建 AI
应用，有免费额度。

我一直是它的用户，以前还写过文章，介绍它的[工作流模式](https://www.ruanyifeng.com/blog/2024/10/coze.html)：在图形化界面上，用鼠标编排
AI 工作流，生成独立应用。

![](https://cdn.beekka.com/blogimg/asset/202410/bg2024102708.webp)

工作流模式号称不需要编码，小白也能用，但用户最好有编程基础，所以还是有一点点门槛。

于是，扣子现在又推出了"扣子空间"，真正零基础，无门槛完成任务。

它的最大特点是，**内部自动调用各种 Agent（智能体），不需要用户介入，就能完成各种任务** 。你可以把它想象成一个"Agent 的自动调用器"。

对于用户来说，因为有了底层的 Agent 能力，它不仅可以回答问题，还能解决问题（任务），从而成为你的办公助手和工作搭子。

正如它的宣传语："和 Agent 一起开始你的工作"。

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025041903.webp)

注意，它现在需要邀请码，可以去扣子公众号和扣子空间官网（space.coze.cn）领取。

## 四、界面

扣子空间的网址是 [space.coze.cn](https://space.coze.cn/)，点进去就可以使用。

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025042005.webp)

界面很简单，左侧是任务列表，右侧是一个对话框，用来输入新任务。

执行任务要求时，默认是"探索模式"，AI 自动完成各个步骤，速度较快。

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025041905.webp)

你也可以改成"规划模式"，显示 AI 思考的中间步骤，便于随时调整。

除此以外，就没有需要设置的地方了，很符合直觉。

## 五、任务示例

下面是我的一些使用实例，都是办公类的任务。

大家看看，它完成得怎么样，像不像一个精通各种技能的实习生。

### 5.1 撰写研究报告

最常见的办公任务，肯定是撰写文档。我让 AI 撰写下面的研究报告。

> 我需要一篇研究报告，关于上海茶饮行业近几年的发展情况，以及投资机会的分析，包括行业发展、热门产品等信息。

注意，文档类的任务最好指定输出格式，否则生成的内容以 Markdown 格式展示在对话页上，不方便利用。

我一般是在提示词最后，加上这样一句。

> 同时做一个可视化的网页。

开始运行后，它就会分解任务，按步完成。

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025042006.webp)

最后，它给出生成的 markdown 文件和网页文件。

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025042007.webp)

你可以在新窗口打开网页预览。下面就是它生成的网页，图文并茂，有数据也有论述。

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025042008.webp)

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025042009.webp)

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025042010.webp)

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025042011.webp)

整个报告分成四个部分，可以根据需要增减，自己使用或交差，总体上没有问题。

### 5.2 多种输出格式

前面说过，扣子空间内置了各种 Agent。

除了生成网页的 Agent，还有生成 Office 文档、PDF、飞书文档的 Agent，都可以用，下面是一个例子。

> 帮我比较一下T3、滴滴出行、高德，作为新手网约车司机，在重庆跑，哪个平台最推荐，并说明详细原因，输出一份飞书文档。

由于飞书文档是带有布局的，实际生成时，也是从文字报告生成网页，然后系统提示你将网页内容复制到飞书。

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025042012.webp)

如果输出 PDF 文件或幻灯片 PPT 文件，系统会直接给出文件下载。

> 我正在编排行程，目的是安徽皖南地区，包括黄山和当地的其他风景点，请详细研究行程、交通路线、景点介绍、门票、住宿和当地饮食等信息，形成一份完整的行程安排，以
> PPT 形式展示。

它生成了一个28页的 PPT 文件，下载后，完全可以直接上台演示。

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025042116.webp)

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025042117.webp)

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025042118.webp)

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025042119.webp)

### 5.3 表格能力

办公类的 AI，一定要有表格处理能力。

> 请生成一个表格，包含上证50指数成分股，及其最新的收盘价。

默认情况下，表格生成后，会显示在网页上。

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025041914.webp)

系统还会给出一个 csv 文件，供下载。

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025041915.webp)

如果想要完备的电子表格功能，可以把 csv 文件导入电子表格软件。

### 5.4 其他功能

扣子空间内置的 Agent 很多，还可以调用高德地图、生成网页游戏等等。

> 请生成一个互动式的学习网站，帮我学习 CSS 的 oklch 颜色函数。

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025041916.webp)

上面是网页小游戏的例子，下面是调用地图的例子。

> 用高德地图分析一下上海外滩地区所有瑞幸咖啡的门店选址，做成一个可视化的网页给我。

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025042013.webp)

如果内置的 Agent 不足以满足需求，你还可以设置让它接入各种 MCP，扩展能力。

### 5.5 专家系统

最后，它还自带了专家系统，也就是高级的专业知识库，提供深度的分析能力。

目前，内置了两个专家系统：用户研究专家和 A 股观察助手。

![](https://cdn.beekka.com/blogimg/asset/202504/bg2025041918.webp)

前者用来用户问卷调查、访谈、生成分析报告；后者用来分析自选股和大盘，提供研究分析报告。

深度的分析和处理任务，需要特定的专业知识，可以试试它们。

## 六、总结

经过初步的试用，我对扣子空间评价很好，**非常好用的办公助手和 AI 实习生** ，确实能够提高办公效率。

我觉得，它的设计思路很正确，自动调用各种 Agent，既能扩展各种能力，又能消除了上手难度，同时具备深度研究（deep research）能力。

更难得的是，它的完成度相当不错，没遇到明显的 bug，可以用于实际的办公。

总之，作为办公类的 AI 产品，它的"工作搭子"的模式，我觉得可用也可行。

后面，办公类 AI 产品相信会大量涌现，鉴于它的重要性，我还会介绍和评测更多。

（完）

### 文档信息

- 版权声明：自由转载-非商用-非衍生-保持署名（[创意共享3.0许可证](http://creativecommons.org/licenses/by-nc-nd/3.0/deed.zh)）
- 发表日期： 2025年4月21日

## 相关文章

- **2025.04.22:[巨头的新战场：AI 编程 IDE（暨 字节 Trae 调用 MCP 教程）](http://www.ruanyifeng.com/blog/2025/04/trae-mcp.html)**

一、引言 本周，我要加写一篇文章。

- **2025.03.03:[Trae 国内版出来了，真的好用吗？](http://www.ruanyifeng.com/blog/2025/03/trae.html)**

年初一月份，我就看到新闻，字节面向海外发布了一款 AI IDE，叫做 Trae。

- **2025.01.16:[AI 搞定微信小程序](http://www.ruanyifeng.com/blog/2025/01/tencent-cloud-copilot.html)**

一、前言 AI 生成代码，早不是新鲜事了，但是 AI 生成微信小程序，似乎还不多见。

- **2024.12.02:[AI 应用无代码开发教程：工作流模式详解](http://www.ruanyifeng.com/blog/2024/12/no-code-ai-tutorial.html)**

一、引言 一个月前，我写了一篇《AI 开发的捷径：工作流模式》，引起了很多读者的兴趣。

## 广告[（购买广告位）](/support.html)

[云手机](https://www.geelark.cn/?utm_source=ruanyifeng.com&utm_medium=banner&utm_campaign=campaign20250305 "云手机")

[![云手机](https://cdn.beekka.com/blogimg/asset/202503/bg2025030512.webp)
](https://www.geelark.cn/?utm_source=ruanyifeng.com&utm_medium=banner&utm_campaign=campaign20250305 "云手机")

## 留言（6条）

Ashitaka 说：

看了老师的文档有一段时间了，从来没有评论过，今天看到这个，去公众号申请了邀请码，看完文档感觉很不错，我也想尝试下国内的Ai智能体,希望能有不错的体验。

2025年4月21日 11:41 | [#](http://www.ruanyifeng.com/blog/2025/04/coze-space.html#comment-446666) | 引用

Levid 说：

缺个邀请码~~~

2025年4月21日 11:46 | [#](http://www.ruanyifeng.com/blog/2025/04/coze-space.html#comment-446667) | 引用

秦先生 说：

和Manus一样

2025年4月21日 14:21 | [#](http://www.ruanyifeng.com/blog/2025/04/coze-space.html#comment-446669) | 引用

coolwaterld 说：

试了一下，专业领域的知识有限，生成的ppt比较空洞，没有逻辑硬伤，但是文字是片汤话，干货少。

2025年4月21日 15:27 | [#](http://www.ruanyifeng.com/blog/2025/04/coze-space.html#comment-446670) | 引用

zzsqwq 说：

阮老师这边好多字节的广告

2025年4月21日 16:43 | [#](http://www.ruanyifeng.com/blog/2025/04/coze-space.html#comment-446671) | 引用

Kevin's Space 说：

它的巨大优势是对中文互联网的深度支持。
劣势是脑子不好使，是的，DeepSeek也不好使

2025年4月21日 23:15 | [#](http://www.ruanyifeng.com/blog/2025/04/coze-space.html#comment-446674) | 引用

## 我要发表看法

您的留言 （HTML标签部分可用）

您的大名：

«-必填

电子邮件：

«-必填，不公开

个人网址：

«-我信任你，不会填写广告链接

记住个人信息？

**正在发表您的评论，请稍候**

«\- 点击按钮

![微信扫描](https://www.wangbase.com/blogimg/asset/202001/bg2020013101.jpg)

[Weibo](http://weibo.com/ruanyf "微博") | [Twitter](https://twitter.com/ruanyf "Twitter") | [GitHub](https://github.com/ruanyf "GitHub")

Email: [[email protected]](/cdn-cgi/l/email-
protection#8ef7e7e8ebe0e9a0fcfbefe0cee9e3efe7e2a0ede1e3 "电子邮件")

_[2025年4月21日]: 2025-04-21T10:50:46+08:00
_[2025年4月21日 11:41]: April 21, 2025 11:41 AM
_[2025年4月21日 11:46]: April 21, 2025 11:46 AM
_[2025年4月21日 14:21]: April 21, 2025 2:21 PM
_[2025年4月21日 15:27]: April 21, 2025 3:27 PM
_[2025年4月21日 16:43]: April 21, 2025 4:43 PM \*[2025年4月21日 23:15]: April 21, 2025 11:15 PM
