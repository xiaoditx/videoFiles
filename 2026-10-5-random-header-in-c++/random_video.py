from manim import *
import os
import re 

# ---------- 字体 ----------
CN_FONT = "Microsoft YaHei"
CODE_FONT = "Consolas"

# ---------- 时长参数 ----------
PER_CHAR = 0.16      # 每个中文字符的阅读时长
MIN_WAIT = 0.9       # 单行最少等待
MAX_WAIT = 4.0       # 单行最多等待

def reading_time(text, extra=0.4):
    """根据文字长度估算等待时长"""
    n = len(text)
    t = extra + n * PER_CHAR
    return max(MIN_WAIT, min(MAX_WAIT, t))


class RandomVideo(Scene):

    # ------------------------------------------------------------------
    # 基础工具
    # ------------------------------------------------------------------
    def make_text(self, text, size=32, color=WHITE):
        return Text(text, font=CN_FONT, font_size=size, color=color)

    def make_code(self, text, size=22, color=YELLOW):
        return Text(text, font=CODE_FONT, font_size=size, color=color)

    def clear_all(self, run_time=0.5):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)

    # ------------------------------------------------------------------
    # 段落：逐行淡入，时长按行长度自适应
    # ------------------------------------------------------------------
    def show_paragraph(self, lines, size=30, color=WHITE, buff=0.45,
                       center=ORIGIN, extra_wait=0.8):
        if isinstance(lines, str):
            lines = [lines]
        group = VGroup(*[self.make_text(l, size=size, color=color) for l in lines])
        group.arrange(DOWN, buff=buff).move_to(center)

        for m, line in zip(group, lines):
            self.play(FadeIn(m, shift=UP * 0.15), run_time=0.4)
            self.wait(reading_time(line))

        if extra_wait:
            self.wait(extra_wait)
        return group

    def has_chinese(self, s):
        return bool(re.search(r'[\u4e00-\u9fff]', s))

    # ------------------------------------------------------------------
    # 代码块：带底框，逐行出现
    # ------------------------------------------------------------------
    def show_code(self, lines, size=22, color=YELLOW, center=ORIGIN,
                  line_wait=0.5, extra_wait=1.2):
        if isinstance(lines, str):
            lines = [lines]

        group = VGroup()
        for line in lines:
            font = CN_FONT if self.has_chinese(line) else CODE_FONT
            fsize = size + 2 if self.has_chinese(line) else size
            group.add(Text(line, font=font, font_size=fsize, color=color))

        group.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(center)

        bg = SurroundingRectangle(
            group, color=GRAY, buff=0.3,
            corner_radius=0.1, stroke_width=1.2,
        )
        bg.set_fill(BLACK, opacity=0.35)

        self.play(FadeIn(bg), run_time=0.3)
        for m in group:
            self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.3)
            self.wait(line_wait)

        if extra_wait:
            self.wait(extra_wait)
        return VGroup(bg, group)

    # ------------------------------------------------------------------
    # 上下大字（用于"没有"/"有"这类强调）
    # ------------------------------------------------------------------
    def show_emphasis(self, top_text, big_text, big_color=RED,
                      top_size=38, big_size=100, big_wait=1.5):
        top = self.make_text(top_text, size=top_size)
        top.move_to(UP * 1.6)
        big = self.make_text(big_text, size=big_size, color=big_color)
        big.move_to(DOWN * 0.6)

        self.play(FadeIn(top, shift=UP * 0.3), run_time=0.6)
        self.wait(reading_time(top_text))
        self.play(FadeIn(big, scale=1.6), run_time=0.8)
        self.wait(big_wait)

    # ------------------------------------------------------------------
    # 主流程
    # ------------------------------------------------------------------
    def construct(self):

        # ============ 1. 标题 ============
        title = self.make_text("计算机中有真随机吗？", size=58, color=YELLOW)
        underline = Line(
            title.get_corner(DL) + DOWN * 0.2,
            title.get_corner(DR) + DOWN * 0.2,
            color=YELLOW, stroke_width=2,
        )
        self.play(Write(title), run_time=1.4)
        self.play(Create(underline), run_time=0.6)
        self.wait(1.8)
        self.clear_all()

        # ============ 2. 没有 ============
        self.show_emphasis("很多人会告诉你", "没有", RED)
        self.clear_all()

        # ============ 3. 有 ============
        self.show_emphasis("但今天我要告诉你", "有", GREEN)
        self.clear_all()

        # ============ 4. TRNG 介绍 ============
        top = self.make_text("它的实现，依赖于一个设备", size=36)
        top.move_to(UP * 2.2)
        mid = self.make_text("真随机发生器（TRNG）", size=52, color=YELLOW)
        mid.move_to(UP * 0.6)
        bot = self.make_text(
            "这个设备早已被安装到了大多数的现代 PC / 移动设备中",
            size=26, color=GRAY_B,
        )
        bot.move_to(DOWN * 2.2)

        self.play(FadeIn(top, shift=UP * 0.3), run_time=0.6)
        self.wait(reading_time("它的实现，依赖于一个设备"))
        self.play(Write(mid), run_time=1.0)
        self.wait(reading_time("真随机发生器（TRNG）", extra=0.6))
        self.play(FadeIn(bot, shift=UP * 0.2), run_time=0.6)
        self.wait(reading_time("这个设备早已被安装到了大多数的现代 PC / 移动设备中"))
        self.clear_all()

        # ============ 5. TRNG 原理 ============
        self.show_paragraph([
            "TRNG 通过量化人类无法控制的物理现象来获取真随机数据",
            "包括电子噪声、放射衰变、光子噪声、混沌系统等等",
            "其原理偏向物理，我们不过多赘述",
        ], size=30)
        self.clear_all()

        # ============ 6. 传统 C/C++ 代码 ============
        intro = self.make_text("传统 C/C++ 开发采用下面的代码获取随机数：", size=28)
        intro.to_edge(UP, buff=0.9)
        self.play(FadeIn(intro, shift=UP * 0.2), run_time=0.5)
        self.wait(reading_time("传统 C/C++ 开发采用下面的代码获取随机数："))

        self.show_code([
            "const int seed = 1000;",
            "srand(seed);",
            "int rand_value = rand();",
        ], center=DOWN * 0.5, extra_wait=1.0)
        self.clear_all()

        # ============ 7. 固定种子问题 ============
        self.show_paragraph([
            "这个代码存在一个问题，就是固定种子",
            "这导致，程序每次启动，获取的随机数序列是一致的",
            "我们完全可以倒推种子预测下一个随机数",
        ], size=30)
        self.clear_all()

        # ============ 8. 用时间做种子 ============
        self.show_paragraph([
            "于是，程序员们选择采用不固定的种子进行初始化",
            "最常见的做法就是：时间",
        ], size=30, center=UP * 2.4, extra_wait=0.4)

        self.show_paragraph(
            ["还是取随机数"],
            size=28, center=UP * 1.2, extra_wait=0.2,
        )

        self.show_code([
            "srand(time(NULL));",
            "int rand_value = rand();",
        ], center=DOWN * 0.3, extra_wait=0.6)

        note = self.make_text("于是程序的随机值在每次启动时就有了区别",
                              size=26, color=GRAY_B)
        note.move_to(DOWN * 2.5)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(reading_time("于是程序的随机值在每次启动时就有了区别"))
        self.clear_all()

        # ============ 9. 依旧不安全 ============
        self.show_paragraph([
            "但这依旧不安全",
            "C/C++ 的标准规定了 rand 可以取到 0 到 RAND_MAX 内的任意整数",
            "但是没有规定随机算法，交由编译器实现决定",
            "因此不能保证其安全",
            "大多数的实现也确实不安全",
            "多采用了线性同余生成器（LCG）",
            "逆推极其简单",
        ], size=28, buff=0.4)
        self.clear_all()

        # ============ 10. C++ random 头 ============
        self.show_paragraph([
            "为此，C++ 引入了 random 头来实现更好的随机数获取质量",
            "我们可以使用其中提供的“随机数设备”生成真随机",
        ], size=30, center=UP * 2.4, extra_wait=0.4)

        self.show_code([
            "std::random_device rd;",
            "auto rand_value = rd();",
        ], center=DOWN * 0.3, extra_wait=1.2)
        self.clear_all()

        # ============ 11. 退化策略 ============
        self.show_paragraph([
            "真随机设备依赖于 TRNG，但有的旧设备或低端设备没有装配",
            "因此 random_device 提供了退化策略",
            "下面我们以 MinGW 的实现为例，讲讲退化策略",
        ], size=30)
        self.clear_all()

        # ============ 12. 退化流程 ============
        self.show_paragraph([
            "实现首先会尝试使用 RDRAND/RDSEED 硬件指令获取随机数",
            "这是有 TRNG 的理想情况",
            "当 TRNG 无法使用时，实现会尝试使用 Windows 的 rand_s API",
            "这个 API 是密码学安全的，通常比较可靠",
            "当 rand_s 也失败时，实现最后退化到线性同余生成器",
            "可以理解为 srand(time(NULL)) 后用 rand 获取了一个随机数",
            "这个流程起码在 MinGW 提供的 g++ 15.2.0 上成立，旧版可能有所不同",
        ], size=26, buff=0.35)
        self.clear_all()

        # ============ 13. 速度对比（含图片） ============
        # 第一段文字：单独浮现
        line1 = VGroup(
            self.make_text("随机数设备虽然在大多数现代设备上都能取到真随机", size=30),
            self.make_text("但它依赖记录物理现象，速度较慢", size=30),
        ).arrange(DOWN, buff=0.4).move_to(UP * 2.9)

        self.play(FadeIn(line1, shift=UP * 0.2), run_time=0.8)
        self.wait(reading_time("随机数设备虽然在大多数现代设备上都能取到真随机，但它依赖记录物理现象，速度较慢"))

        # 第二段文字：构造但先不显示
        line2 = VGroup(
            self.make_text(
                "下面两张截图展示了随机数设备与 rand 各取 500000000 次随机数的时间差异",
                size=22, color=GRAY_B,
            ),
            self.make_text(
                "（Windows 10, Dev C++ 集成环境编译）",
                size=22, color=GRAY_B,
            ),
        ).arrange(DOWN, buff=0.25).move_to(UP * 1.6)

        # 加载图片（图片必须用 Group，不能用 VGroup）
        images = Group()
        if os.path.exists("a.png"):
            images.add(ImageMobject("a.png"))
        if os.path.exists("b.png"):
            images.add(ImageMobject("b.png"))

        if len(images) > 0:
            for img in images:
                img.set(width=7.5)

            images.arrange(DOWN, buff=0.25)
            images.move_to(DOWN * 1.8)

            frame = SurroundingRectangle(images, color=GRAY, buff=0.15,
                                         stroke_width=1)

            # line2 + 边框 + 图片 同时浮现
            self.play(
                FadeIn(line2, shift=UP * 0.2),
                FadeIn(frame),
                FadeIn(images, shift=UP * 0.3),
                run_time=1.2,
            )
            self.wait(5.0)
        else:
            ph = VGroup()
            for label in ["a.png", "b.png"]:
                r = Rectangle(width=4.5, height=1.3, color=GRAY)
                r.set_fill(GRAY, opacity=0.15)
                t = Text(f"[ {label} ]", font=CN_FONT,
                         font_size=24, color=GRAY)
                ph.add(VGroup(r, t))
            ph.arrange(DOWN, buff=0.3).move_to(DOWN * 1.8)

            self.play(
                FadeIn(line2, shift=UP * 0.2),
                Create(ph),
                run_time=1.2,
            )
            self.wait(3.0)

        self.clear_all()

        # ============ 14. 混合方案 ============
        self.show_paragraph([
            "因此，在一些安全性不是特别重要但又要防止随机算法被轻易倒推的领域，",
            "大多采用下面的方案：",
            "先使用随机数设备获取真随机数字",
            "再初始化高质量伪随机算法引擎从而获得随机的随机数",
        ], size=28, buff=0.4)
        self.clear_all()

        # ============ 15. mt19937 示例 ============
        self.show_paragraph(
            ["我们来看个例子："],
            size=32, center=UP * 3.0, extra_wait=0.2,
        )

        self.show_code([
            "std::random_device rd;",
            "std::mt19937 gen(rd());",
            "std::cout << gen();",
        ], center=UP * 0.8, extra_wait=0.6)

        self.show_paragraph([
            "这个例子中，使用真随机初始化了一个 mt19937 对象",
            "这个对象就是使用了“梅森旋转算法”的算法引擎",
            "这种算法在质量、速度上的平衡相对其算法更优",
            "若想要根据需求选择其他算法，可自行查阅 reference",
        ], size=24, color=GRAY_B, center=DOWN * 2.6, buff=0.3,
           extra_wait=0.6)
        self.clear_all()

        # ============ 16. mt19937 不安全提醒 ============
        warn = self.make_text("需要注意的是，mt19937 不是密码学安全",
                              size=36, color=RED)
        warn.move_to(UP * 2.4)
        self.play(FadeIn(warn, shift=UP * 0.3), run_time=0.6)
        self.wait(reading_time("需要注意的是，mt19937 不是密码学安全"))

        self.show_paragraph([
            "密码、令牌、会话 ID 等场景还是请直接使用操作系统提供的 CSPRNG",
            "如 Linux 的 getrandom()、Windows 的 BCryptGenRandom",
            "如果你想，可以尝试自行实现 CSPRNG，不过并不建议",
        ], size=26, center=DOWN * 0.5, buff=0.35, extra_wait=1.0)
        self.clear_all()

        # ============ 17. 分布引入 ============
        self.show_paragraph([
            "random 不止提供了真随机和高质算法",
            "它还提供了另一样东西：分布",
        ], size=40, center=DOWN * 0.5, buff=0.35, extra_wait=1.0)
        self.clear_all()
        
        self.show_paragraph([
            "C/C++ 中，随机数的区间是固定的",
            "比如 rand 的区间是 0 到 RAND_MAX 闭区间",
            "即使是 random_device、mt19937 都是固定区间取值",
            "但我们有时只想取得一定区间的数值",
            "比如 1 到 6 闭区间的任意整数",
            "传统 C/C++ 的做法是取随机后取余数",
            "于是就写成",
        ], size=26, buff=0.32, center=UP * 0.8, extra_wait=0.2)

        self.show_code([
            "int a = (rand() % 6) + 1;",
        ], center=DOWN * 2.8, extra_wait=1.2)
        self.clear_all()

        # ============ 18. 取模偏差 ============
        self.show_paragraph(
            ["这导致了一个问题：即使随机数概率均匀，取余数的结果也是分布不均的"],
            size=28, center=UP * 3.0, extra_wait=0.4,
        )

        self.show_paragraph([
            "让我们假设 RAND_MAX = 32767",
            "那么 rand() 有 32768 个可能值",
            "我们对其取 10 的余数，可以推出：",
        ], size=26, center=UP * 1.2, buff=0.35, extra_wait=0.3)

        self.show_code([
            "32768 = 10 * 3276 + 8",
            "余数 0~7 各出现 3277 次",
            "余数 8~9 各出现 3276 次",
        ], center=DOWN * 1.2, extra_wait=0.4)

        self.show_paragraph([
            "因此每个余数的概率不完全相等",
            "偏差很小，但确实存在",
        ], size=26, color=GRAY_B, center=DOWN * 3.2, buff=0.3,
           extra_wait=0.8)
        self.clear_all()

        # ============ 19. uniform_int_distribution ============
        self.show_paragraph([
            "random 提供的分布正好解决了这一问题",
            "比较常用的一个，是整数分布 std::uniform_int_distribution",
            "我们可以采用这样的方式让取到的随机数均匀地分布到 [1,6] 内：",
        ], size=26, center=UP * 2.6, buff=0.35, extra_wait=0.3)

        self.show_code([
            "std::random_device rd;",
            "std::mt19937 gen(rd());",
            "std::uniform_int_distribution<int> dist(1, 6);",
            "std::cout << dist(gen);",
        ], size=22, center=DOWN * 0.15, extra_wait=0.5)   # 原 DOWN * 0.6

        self.show_paragraph([
            "分布的通常实现是“拒绝采样”",
            "也就是仍然是取模的算法但会先抛弃多余的部分",
            "用上面 [0, RAND_MAX] 分布放到 [0, 9] 的例子",
            "就是直接舍弃最后 8 个数字",
        ], size=24, color=GRAY_B, center=DOWN * 2.7,       # 原 DOWN * 3.2
           buff=0.25, extra_wait=0.8)                       # 原 buff=0.28
        self.clear_all()

        # ============ 20. 冰山之下的分布（表格） ============
        q1 = self.show_paragraph(
            ["你可能会说：那这个功能也不是很厉害啊"],
            size=40, center=UP, extra_wait=0.2,
        )
        self.play(FadeOut(q1), run_time=0.3)

        wrong = self.make_text("错", size=72, color=RED)
        wrong.move_to(ORIGIN)
        self.play(FadeIn(wrong, scale=1.8), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(wrong), run_time=0.4)

        self.show_paragraph([
            "std::uniform_int_distribution 只是冰山一角",
            "random 还提供了大量其他分布，这里列出一些常用的",
        ], size=26, center=UP * 2.8, buff=0.35)

        # ---- 表格 ----
        headers = ["分布", "参数", "意义"]
        rows = [
            ["std::uniform_real_distribution", "a,b", "[a,b) 范围内的实数"],
            ["std::bernoulli_distribution", "p", "成功概率为 p 的伯努利分布"],
            ["std::binomial_distribution", "n,p", "成功概率为 p 的 n 重伯努利实验的成功次数"],
            ["std::negative_binomial_distribution", "k,p", "达到 k 次成功前的失败次数"],
            ["std::geometric_distribution", "p", "第一次成功前的失败次数"],
            ["std::normal_distribution", "a,b", "均值为 a，标准差为 b 的正态分布"],
        ]

        # 列 x 位置：第 0 列加宽，第 1、2 列右移
        col_x = [-6.7, -1.5, 1.4]
        row_h = 0.55

        table = VGroup()

        # 表头
        head_y = 0.0
        for j, h in enumerate(headers):
            t = Text(h, font=CN_FONT, font_size=22, color=YELLOW)
            t.move_to([col_x[j], head_y, 0], aligned_edge=LEFT)
            table.add(t)

        # 分隔线（加宽）
        sep = Line(
            [-6.8, head_y - row_h * 0.55, 0],
            [ 6.8, head_y - row_h * 0.55, 0],
            color=GRAY, stroke_width=1.2,
        )
        table.add(sep)

        # 数据行
        for i, row in enumerate(rows):
            y = head_y - (i + 1) * row_h
            # 第 0 列：代码字体，字号缩到 14
            t0 = Text(row[0], font=CODE_FONT, font_size=14)
            t0.move_to([col_x[0], y, 0], aligned_edge=LEFT)
            table.add(t0)
            # 第 1 列：中文/符号
            t1 = Text(row[1], font=CN_FONT, font_size=17)
            t1.move_to([col_x[1], y, 0], aligned_edge=LEFT)
            table.add(t1)
            # 第 2 列：中文
            t2 = Text(row[2], font=CN_FONT, font_size=16)
            t2.move_to([col_x[2], y, 0], aligned_edge=LEFT)
            table.add(t2)

        table.move_to(DOWN * 0.5)

        self.play(FadeIn(table, shift=UP * 0.3), run_time=1.2)
        self.wait(5.0)
        self.clear_all()
        # ============ 21. 重写对比 ============
        self.show_paragraph(
            ["现在，让我们来重写取随机数"],
            size=34, center=UP * 3.2, extra_wait=0.3,
        )

        # 左：传统写法
        left_title = self.make_text("传统写法", size=26, color=RED)
        left_title.move_to([-3.5, 0.7, 0])                       # 2.2 - 1.5
        left_code = VGroup(
            self.make_code("srand(time(NULL));", size=18),
            self.make_code("int a = (rand() % 6) + 1;", size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        left_code.move_to([-3.5, -0.3, 0])                       # 1.2 - 1.5
        left_bg = SurroundingRectangle(left_code, color=RED, buff=0.25,
                                       corner_radius=0.1, stroke_width=1)
        left_bg.set_fill(BLACK, opacity=0.35)

        # 右：random 写法
        right_title = self.make_text("random 写法", size=26, color=GREEN)
        right_title.move_to([2.5, 0.7, 0])                       # 2.2 - 1.5
        right_code = VGroup(
            self.make_code("std::random_device rd;", size=18),
            self.make_code("std::mt19937 gen(rd());", size=18),
            self.make_code("std::uniform_int_distribution<int> dist(1, 6);", size=18),
            self.make_code("int a = dist(gen);", size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        right_code.move_to([2.5, -0.65, 0])                      # 1.0 - 0.15 - 1.5
        right_bg = SurroundingRectangle(right_code, color=GREEN, buff=0.25,
                                        corner_radius=0.1, stroke_width=1)
        right_bg.set_fill(BLACK, opacity=0.35)

        self.play(FadeIn(left_title), FadeIn(left_bg), run_time=0.4)
        for m in left_code:
            self.play(FadeIn(m, shift=RIGHT * 0.15), run_time=0.25)
            self.wait(0.35)

        self.wait(0.5)

        self.play(FadeIn(right_title), FadeIn(right_bg), run_time=0.4)
        for m in right_code:
            self.play(FadeIn(m, shift=RIGHT * 0.15), run_time=0.25)
            self.wait(0.35)

        self.wait(2.0)
        self.clear_all()

        # ============ 22. 结尾 ============
        end1 = self.make_text("至此，我们取到了", size=34)
        end2 = self.make_text("分布均匀、速度较快、较难预测", size=52, color=YELLOW)
        end3 = self.make_text("的随机数", size=34)

        end1.move_to(UP * 1.6)
        end2.move_to(ORIGIN)
        end3.move_to(DOWN * 1.4)

        self.play(FadeIn(end1, shift=UP * 0.3), run_time=0.5)
        self.wait(0.5)
        self.play(Write(end2), run_time=1.2)
        self.wait(1.0)
        self.play(FadeIn(end3, shift=UP * 0.3), run_time=0.5)
        self.wait(3.0)