
from manim import *
import numpy as np
 
# ---------- Paleta ----------
C_F = BLUE          # f(x)
C_FF = YELLOW       # F(x), antiderivada
C_AREA = GREEN      # área positiva
C_NEG = RED         # área negativa
C_TXT = WHITE
 
 
class IntegralAntiderivadas(Scene):
    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def titulo(self, texto, formula=None, color=C_TXT):
        partes = [Text(texto, font_size=36, color=color, weight=BOLD)]
        if formula:
            partes.append(MathTex(formula, font_size=44, color=color))
        return VGroup(*partes).arrange(RIGHT, buff=0.3).to_edge(UP)
 
    def en_pantalla(self, m, margen=0.4):
        max_w = config.frame_width - 2 * margen
        if m.width > max_w:
            m.scale_to_fit_width(max_w)
        lim_x = config.frame_width / 2 - margen
        lim_y = config.frame_height / 2 - margen
        if m.get_right()[0] > lim_x:
            m.shift(LEFT * (m.get_right()[0] - lim_x))
        if m.get_left()[0] < -lim_x:
            m.shift(RIGHT * (-lim_x - m.get_left()[0]))
        if m.get_bottom()[1] < -lim_y:
            m.shift(UP * (-lim_y - m.get_bottom()[1]))
        return m
 
    def limpiar(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.3)
 
    # ------------------------------------------------------------------
    # Escena principal
    # ------------------------------------------------------------------
    def construct(self):
        self.seccion_portada()
        self.seccion_antiderivada()
        self.seccion_integral_area()
        self.seccion_auto()
        self.seccion_teorema()
        self.seccion_ejemplo_1()
        self.seccion_ejemplo_seno()
        self.seccion_area_con_signo()
        self.seccion_tips()
        self.seccion_resumen()
 
    # ------------------------------------------------------------------
    # 0. Portada y pregunta central
    # ------------------------------------------------------------------
    def seccion_portada(self):
        titulo = Text("Calcular una integral\nmediante antiderivadas",
                      font_size=52, weight=BOLD, line_spacing=0.9)
        titulo.set_color_by_gradient(BLUE, GREEN)
        sub = Text("Teorema Fundamental del Cálculo", font_size=28, color=GRAY_B)
        sub.next_to(titulo, DOWN, buff=0.5)
 
        self.play(Write(titulo), run_time=2)
        self.play(FadeIn(sub, shift=UP * 0.3))
        self.wait(1.5)
        self.play(FadeOut(titulo), FadeOut(sub))
 
        pregunta = Text("Pregunta central:", font_size=34, color=YELLOW)
        pregunta.to_edge(UP, buff=1.2)
        q = Text("¿Por qué una integral definida puede\ncalcularse como F(b) − F(a)?",
                 font_size=38, line_spacing=0.9)
        q.next_to(pregunta, DOWN, buff=0.6)
        formula = MathTex(r"\int_a^b f(x)\,dx", "=", "F(b)-F(a)", font_size=64)
        formula[0].set_color(C_F)
        formula[2].set_color(C_FF)
        formula.next_to(q, DOWN, buff=0.9)
 
        self.play(FadeIn(pregunta, shift=DOWN * 0.3))
        self.play(Write(q), run_time=2)
        self.wait(0.5)
        self.play(Write(formula), run_time=2)
        self.wait(2)
        self.limpiar()
 
    # ------------------------------------------------------------------
    # 1. ¿Qué es una antiderivada?
    # ------------------------------------------------------------------
    def seccion_antiderivada(self):
        titulo = self.titulo("1. ¿Qué es una antiderivada?")
        self.play(Write(titulo))
 
        # Definición
        defin = MathTex(r"F'(x) = f(x)", font_size=60)
        defin[0][0:4].set_color(C_FF)
        defin[0][5:].set_color(C_F)
        self.play(Write(defin))
        self.wait(1)
 
        flecha_txt = VGroup(
            MathTex(r"F(x) = x^2", color=C_FF),
            MathTex(r"\xrightarrow{\ \text{derivar}\ }", font_size=44),
            MathTex(r"f(x) = 2x", color=C_F),
        ).arrange(RIGHT, buff=0.5)
        self.play(defin.animate.scale(0.7).next_to(titulo, DOWN, buff=0.4))
        flecha_txt.next_to(defin, DOWN, buff=0.6)
        self.play(FadeIn(flecha_txt, shift=UP * 0.3))
        self.wait(1.5)
 
        invers = Text("Integrar = ‘deshacer’ la derivada", font_size=30, color=GRAY_B)
        invers.next_to(flecha_txt, DOWN, buff=0.5)
        self.play(FadeIn(invers))
        self.wait(1.5)
        self.play(FadeOut(defin), FadeOut(flecha_txt), FadeOut(invers))
 
        # Infinitas antiderivadas: x^2, x^2+1.5, x^2-1
        axes = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-2, 6, 1],
            x_length=6.5, y_length=4.5,
            axis_config={"include_numbers": True, "font_size": 22},
        ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.6)
        self.play(Create(axes))
 
        constantes = [0, 1.5, -1]
        colores = [YELLOW, ORANGE, TEAL]
        curvas, etiquetas = [], []
        for c, col in zip(constantes, colores):
            g = axes.plot(lambda x, c=c: x ** 2 + c, color=col, x_range=[-2.2, 2.2])
            curvas.append(g)
            signo = "+" if c >= 0 else "-"  # ASCII: LaTeX no acepta U+2212
            etiquetas.append(MathTex(rf"x^2 {signo} {abs(c)}" if c != 0 else r"x^2",
                                     color=col, font_size=32))
 
        # Panel derecho: etiquetas + mensaje (2 líneas) + F(x)+C, todo en un bloque
        panel = VGroup(*etiquetas).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        texto = Text("¡Todas tienen la misma\nderivada: 2x!",
                     font_size=26, color=YELLOW, line_spacing=0.9)
        nota = MathTex(r"F(x)+C", font_size=48, color=YELLOW)
        derecha = VGroup(panel, texto, nota).arrange(DOWN, buff=0.5)
        derecha.move_to(RIGHT * 3.9 + DOWN * 0.3)
        self.en_pantalla(derecha)
 
        for g, e in zip(curvas, etiquetas):
            self.play(Create(g), FadeIn(e, shift=LEFT * 0.2), run_time=1.2)
        self.play(FadeIn(texto))
 
        # Tangentes en x = 1 con pendiente 2 (paralelas)
        d = axes.c2p(1, 2) - axes.c2p(0, 0)
        d = d / np.linalg.norm(d)
        tangentes = VGroup()
        for c, col in zip(constantes, colores):
            p = axes.c2p(1, 1 + c)
            tangentes.add(Line(p - d * 0.9, p + d * 0.9, color=WHITE, stroke_width=4))
            tangentes.add(Dot(p, color=col))
        self.play(Create(tangentes), run_time=2)
        self.wait(1)
 
        self.play(Write(nota))
        self.wait(2)
        self.limpiar()
 
    # ------------------------------------------------------------------
    # 2. La integral definida como área (sumas de Riemann)
    # ------------------------------------------------------------------
    def seccion_integral_area(self):
        titulo = self.titulo("2. La integral definida = área con signo")
        self.play(Write(titulo))
 
        axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 7, 1],
            x_length=6.5, y_length=4.5,
            axis_config={"include_numbers": True, "font_size": 22},
        ).shift(LEFT * 2.3 + DOWN * 0.7)
        graf = axes.plot(lambda x: 2 * x, color=C_F, x_range=[0, 3.4])
        etiqueta = MathTex("f(x)=2x", color=C_F, font_size=34).next_to(
            axes.c2p(3.4, 6.8), UP, buff=0.1)
        self.play(Create(axes), Create(graf), FadeIn(etiqueta))
 
        dxs = [1.0, 0.5, 0.25, 0.1]
        rects = axes.get_riemann_rectangles(
            graf, x_range=[0, 3], dx=dxs[0],
            input_sample_type="left", color=[GREEN, TEAL], fill_opacity=0.7,
            stroke_width=1)
        self.play(Create(rects))
        info = MathTex(r"\sum f(x_i)\,\Delta x", font_size=40)
        info.to_edge(RIGHT, buff=0.9).shift(UP * 1.5)
        n_txt = Text("rectángulos: 3", font_size=26)
        n_txt.next_to(info, DOWN, buff=0.4)
        self.play(Write(info), FadeIn(n_txt))
        self.wait(1)
 
        for dx in dxs[1:]:
            nuevo = axes.get_riemann_rectangles(
                graf, x_range=[0, 3], dx=dx,
                input_sample_type="left", color=[GREEN, TEAL], fill_opacity=0.7,
                stroke_width=1)
            n_nuevo = Text(f"rectángulos: {int(round(3 / dx))}", font_size=26)
            n_nuevo.move_to(n_txt)
            self.play(Transform(rects, nuevo), Transform(n_txt, n_nuevo), run_time=1.5)
            self.wait(0.4)
 
        area = axes.get_area(graf, x_range=(0, 3), color=C_AREA, opacity=0.6)
        self.play(FadeOut(rects), FadeIn(area))
 
        integral = MathTex(r"\int_0^3 2x\,dx", font_size=52, color=C_AREA)
        integral.next_to(n_txt, DOWN, buff=0.7)
        self.play(Write(integral))
        regla = VGroup(
            Text("Sobre el eje: área  +", font_size=24, color=C_AREA),
            Text("Bajo el eje: área  −", font_size=24, color=C_NEG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(integral, DOWN, buff=0.6)
        self.en_pantalla(regla)
        self.play(FadeIn(regla))
        self.wait(2)
        self.limpiar()
 
    # ------------------------------------------------------------------
    # 3. Intuición: velocidad y posición
    # ------------------------------------------------------------------
    def seccion_auto(self):
        titulo = self.titulo("3. Intuición: velocidad y posición")
        self.play(Write(titulo))
 
        izq = VGroup(
            MathTex("f(x)", color=C_F, font_size=48),
            Text("velocidad", font_size=28, color=C_F),
        ).arrange(DOWN, buff=0.2)
        der = VGroup(
            MathTex("F(x)", color=C_FF, font_size=48),
            Text("posición", font_size=28, color=C_FF),
        ).arrange(DOWN, buff=0.2)
        izq.move_to(LEFT * 3.2 + UP * 1.6)
        der.move_to(RIGHT * 3.2 + UP * 1.6)
        flecha = Arrow(der.get_left(), izq.get_right(), buff=0.3, color=WHITE)
        lbl = Text("derivar", font_size=22).next_to(flecha, UP, buff=0.1)
        self.play(FadeIn(izq), FadeIn(der))
        self.play(GrowArrow(flecha), FadeIn(lbl))
        self.wait(1)
 
        # Recta numérica con un "auto" (punto)
        recta = NumberLine(x_range=[0, 10, 1], length=10,
                           include_numbers=True, font_size=24).shift(DOWN * 0.8)
        self.play(Create(recta))
        a_val, b_val = 2, 8
        punto_a = Dot(recta.n2p(a_val), color=GREEN)
        punto_b = Dot(recta.n2p(b_val), color=RED)
        lbl_a = MathTex("F(a)", color=GREEN, font_size=34).next_to(punto_a, UP, buff=0.3)
        lbl_b = MathTex("F(b)", color=RED, font_size=34).next_to(punto_b, UP, buff=0.3)
 
        auto = Dot(recta.n2p(a_val), radius=0.16, color=YELLOW)
        self.play(FadeIn(punto_a), FadeIn(lbl_a), FadeIn(auto))
        self.play(auto.animate.move_to(recta.n2p(b_val)), run_time=3, rate_func=smooth)
        self.play(FadeIn(punto_b), FadeIn(lbl_b))
 
        brace = BraceBetweenPoints(recta.n2p(a_val), recta.n2p(b_val), direction=DOWN)
        brace.shift(DOWN * 0.5)
        dist = MathTex(r"\text{distancia} = F(b)-F(a)", font_size=40, color=YELLOW)
        dist.next_to(brace, DOWN, buff=0.2)
        self.play(GrowFromCenter(brace), Write(dist))
        self.wait(1)
 
        eq = MathTex(r"\int_a^b f(x)\,dx", "=", r"F(b)-F(a)", font_size=48)
        eq[0].set_color(C_F)
        eq[2].set_color(C_FF)
        eq.to_edge(DOWN, buff=0.4)
        self.play(Write(eq))
        self.wait(2)
        self.limpiar()
 
    # ------------------------------------------------------------------
    # 4. El teorema y la cancelación de la constante C
    # ------------------------------------------------------------------
    def seccion_teorema(self):
        titulo = self.titulo("4. Teorema Fundamental del Cálculo", color=YELLOW)
        self.play(Write(titulo))
 
        caja = MathTex(r"\int_a^b f(x)\,dx = F(b)-F(a)", font_size=62)
        cond = MathTex(r"\text{si } F'(x)=f(x)", font_size=40, color=GRAY_B)
        cond.next_to(caja, DOWN, buff=0.4)
        marco = SurroundingRectangle(caja, color=YELLOW, buff=0.35)
        self.play(Write(caja))
        self.play(Create(marco), FadeIn(cond))
        self.wait(2)
        self.play(FadeOut(marco), FadeOut(cond),
                  caja.animate.scale(0.7).next_to(titulo, DOWN, buff=0.5))
 
        sub = Text("¿Por qué no importa la constante C?", font_size=30, color=ORANGE)
        sub.next_to(caja, DOWN, buff=0.7)
        self.play(FadeIn(sub))
 
        paso1 = MathTex(r"[F(b)+C]-[F(a)+C]", font_size=52)
        paso2 = MathTex(r"F(b)+C-F(a)-C", font_size=52)
        paso3 = MathTex(r"F(b)-F(a)", font_size=52, color=C_FF)
        for p in (paso1, paso2, paso3):
            p.next_to(sub, DOWN, buff=0.8)
        self.play(Write(paso1))
        self.wait(1)
        self.play(TransformMatchingTex(paso1, paso2))
        self.wait(0.5)
        # tachamos las C
        self.play(paso2.animate.set_color(WHITE))
        self.play(TransformMatchingTex(paso2, paso3))
        self.play(Indicate(paso3))
        self.wait(1)
 
        ok = Text("La C se cancela ✔", font_size=30, color=GREEN)
        ok.next_to(paso3, DOWN, buff=0.5)
        self.play(FadeIn(ok))
        self.wait(1.5)
        self.limpiar()
 
        # Procedimiento
        titulo2 = self.titulo("Procedimiento en 4 pasos")
        self.play(Write(titulo2))
        pasos = VGroup(
            VGroup(Text("1.", color=YELLOW), Text("Identifica f(x), a y b")),
            VGroup(Text("2.", color=YELLOW), Text("Encuentra una antiderivada F(x)")),
            VGroup(Text("3.", color=YELLOW), Text("Evalúa F(b) y F(a)")),
            VGroup(Text("4.", color=YELLOW), Text("Resta:  F(b) − F(a)")),
        )
        for fila in pasos:
            fila.arrange(RIGHT, buff=0.3)
            fila.scale(0.9)
        pasos.arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to(ORIGIN)
        for fila in pasos:
            self.play(FadeIn(fila, shift=RIGHT * 0.4), run_time=0.8)
            self.wait(0.4)
        notacion = MathTex(r"\int_a^b f(x)\,dx = \Big[F(x)\Big]_a^b = F(b)-F(a)",
                           font_size=44, color=YELLOW).to_edge(DOWN, buff=0.7)
        self.play(Write(notacion))
        self.wait(2)
        self.limpiar()
 
    # ------------------------------------------------------------------
    # 5. Ejemplo 1: ∫0^3 2x dx
    # ------------------------------------------------------------------
    def seccion_ejemplo_1(self):
        titulo = self.titulo("Ejemplo 1:", r"\int_0^3 2x\,dx")
        self.play(Write(titulo))
 
        axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 7, 1],
            x_length=5.5, y_length=4.2,
            axis_config={"include_numbers": True, "font_size": 22},
        ).to_edge(LEFT, buff=0.7).shift(DOWN * 0.5)
        graf = axes.plot(lambda x: 2 * x, color=C_F, x_range=[0, 3.4])
        area = axes.get_area(graf, x_range=(0, 3), color=C_AREA, opacity=0.6)
        self.play(Create(axes), Create(graf))
        self.play(FadeIn(area))
 
        pasos = VGroup(
            MathTex(r"\int_0^3 2x\,dx", font_size=46),
            MathTex(r"F(x)=x^2", font_size=46, color=C_FF),
            MathTex(r"=F(3)-F(0)", font_size=46),
            MathTex(r"=3^2-0^2", font_size=46),
            MathTex(r"=9", font_size=60, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        pasos.to_edge(RIGHT, buff=1.0).shift(DOWN * 0.2)
        for p in pasos:
            self.play(Write(p), run_time=1)
            self.wait(0.4)
 
        # Verificación geométrica con un triángulo
        tri = Polygon(axes.c2p(0, 0), axes.c2p(3, 0), axes.c2p(3, 6),
                      color=WHITE, stroke_width=4)
        verif = MathTex(r"\tfrac{3\cdot 6}{2}=9", font_size=36, color=WHITE)
        verif.next_to(axes, DOWN, buff=0.1)
        verif.shift(RIGHT * 0.3)
        self.play(Create(tri))
        self.play(Write(verif))
        self.play(Indicate(pasos[-1]))
        chk = Text("¡Coincide con el área\ndel triángulo!", font_size=24,
                   color=GREEN, line_spacing=0.9)
        chk.next_to(pasos, DOWN, buff=0.4)
        self.en_pantalla(chk)
        self.play(FadeIn(chk))
        self.wait(2)
        self.limpiar()
 
    # ------------------------------------------------------------------
    # 6. Ejemplo 2: ∫0^π sen(x) dx
    # ------------------------------------------------------------------
    def seccion_ejemplo_seno(self):
        titulo = self.titulo("Ejemplo 2:", r"\int_0^{\pi} \operatorname{sen}(x)\,dx")
        self.play(Write(titulo))
 
        axes = Axes(
            x_range=[0, 3.5, 1], y_range=[-0.5, 1.5, 0.5],
            x_length=6, y_length=3.5,
            axis_config={"include_numbers": True, "font_size": 22},
        ).to_edge(LEFT, buff=0.7).shift(DOWN * 0.5)
        graf = axes.plot(lambda x: np.sin(x), color=C_F, x_range=[0, 3.4])
        area = axes.get_area(graf, x_range=(0, PI), color=C_AREA, opacity=0.6)
        pi_lbl = MathTex(r"\pi", font_size=30).next_to(axes.c2p(PI, 0), DOWN, buff=0.1)
        self.play(Create(axes), Create(graf))
        self.play(FadeIn(area), FadeIn(pi_lbl))
 
        pasos = VGroup(
            MathTex(r"F(x)=-\cos x", font_size=44, color=C_FF),
            MathTex(r"F(\pi)=-\cos\pi = 1", font_size=44),
            MathTex(r"F(0)=-\cos 0 = -1", font_size=44),
            MathTex(r"F(\pi)-F(0)=1-(-1)", font_size=44),
            MathTex(r"=2", font_size=62, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        pasos.to_edge(RIGHT, buff=0.7).shift(DOWN * 0.2)
        for p in pasos:
            self.play(Write(p), run_time=1)
            self.wait(0.4)
        self.play(Indicate(pasos[-1]))
        self.wait(2)
        self.limpiar()
 
    # ------------------------------------------------------------------
    # 7. Área con signo: ∫-1^1 x dx = 0
    # ------------------------------------------------------------------
    def seccion_area_con_signo(self):
        titulo = self.titulo("Ejemplo 3: área con signo,", r"\int_{-1}^{1} x\,dx")
        self.play(Write(titulo))
 
        axes = Axes(
            x_range=[-2, 2, 1], y_range=[-1.5, 1.5, 1],
            x_length=6, y_length=3.6,
            axis_config={"include_numbers": True, "font_size": 22},
        ).to_edge(LEFT, buff=0.7).shift(DOWN * 0.5)
        graf = axes.plot(lambda x: x, color=C_F, x_range=[-1.5, 1.5])
        neg = axes.get_area(graf, x_range=(-1, 0), color=C_NEG, opacity=0.6)
        pos = axes.get_area(graf, x_range=(0, 1), color=C_AREA, opacity=0.6)
        self.play(Create(axes), Create(graf))
        self.play(FadeIn(neg))
        self.play(FadeIn(pos))
 
        l_neg = MathTex("-\\tfrac12", color=C_NEG, font_size=36).move_to(axes.c2p(-0.7, -0.25))
        l_pos = MathTex("+\\tfrac12", color=C_AREA, font_size=36).move_to(axes.c2p(0.7, 0.25))
        self.play(Write(l_neg), Write(l_pos))
 
        pasos = VGroup(
            MathTex(r"F(x)=\tfrac{x^2}{2}", font_size=46, color=C_FF),
            MathTex(r"F(1)-F(-1)", font_size=46),
            MathTex(r"=\tfrac12-\tfrac12", font_size=46),
            MathTex(r"=0", font_size=64, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        pasos.to_edge(RIGHT, buff=1.0).shift(DOWN * 0.1)
        for p in pasos:
            self.play(Write(p), run_time=1)
            self.wait(0.4)
 
        msg = Text("La integral puede ser negativa o cero,\nno es siempre un área ‘positiva’",
                   font_size=22, color=YELLOW, line_spacing=0.9)
        msg.next_to(pasos, DOWN, buff=0.5)
        self.en_pantalla(msg)
        self.play(FadeIn(msg))
        self.wait(2.5)
        self.limpiar()
 
    # ------------------------------------------------------------------
    # 8. Tips y errores comunes
    # ------------------------------------------------------------------
    def seccion_tips(self):
        titulo = self.titulo("Tips y errores comunes", color=ORANGE)
        self.play(Write(titulo))
 
        tips = VGroup(
            Text("✔  Verifica tu antiderivada derivándola", font_size=28, color=GREEN),
            Text("✔  Usa paréntesis al evaluar negativos", font_size=28, color=GREEN),
            Text("✔  Siempre  F(b) − F(a),  nunca al revés", font_size=28, color=GREEN),
            Text("✔  En integrales definidas no necesitas C", font_size=28, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        tips.next_to(titulo, DOWN, buff=0.6).to_edge(LEFT, buff=1.0)
        for t in tips:
            self.play(FadeIn(t, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(1)
 
        err = Text("Errores típicos", font_size=30, color=RED)
        err.next_to(tips, DOWN, buff=0.5).align_to(tips, LEFT)
        self.play(FadeIn(err))
 
        e1 = VGroup(
            MathTex(r"\int x^3\,dx = x^4", color=RED, font_size=36),
            MathTex(r"\to", font_size=36),
            MathTex(r"\tfrac{x^4}{4}", color=GREEN, font_size=36),
        ).arrange(RIGHT, buff=0.3)
        e2 = VGroup(
            MathTex(r"\int \sin x\,dx = \cos x", color=RED, font_size=36),
            MathTex(r"\to", font_size=36),
            MathTex(r"-\cos x", color=GREEN, font_size=36),
        ).arrange(RIGHT, buff=0.3)
        errores = VGroup(e1, e2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        errores.next_to(err, DOWN, buff=0.3).align_to(tips, LEFT)
        self.play(FadeIn(e1, shift=UP * 0.2))
        self.play(FadeIn(e2, shift=UP * 0.2))
        self.wait(3)
        self.limpiar()
 
    # ------------------------------------------------------------------
    # 9. Resumen final
    # ------------------------------------------------------------------
    def seccion_resumen(self):
        titulo = self.titulo("Resumen", color=YELLOW)
        self.play(Write(titulo))
 
        frase = Text(
            "Si conoces una función F cuya derivada es f,\n"
            "el área bajo f entre a y b es simplemente\n"
            "cuánto cambió F.",
            font_size=34, line_spacing=1.0)
        frase.move_to(UP * 0.7)
        formula = MathTex(r"\int_a^b f(x)\,dx", "=", "F(b)-F(a)", font_size=70)
        formula[0].set_color(C_F)
        formula[2].set_color(C_FF)
        formula.next_to(frase, DOWN, buff=0.8)
        marco = SurroundingRectangle(formula, color=YELLOW, buff=0.3)
 
        self.play(Write(frase), run_time=3)
        self.play(Write(formula), run_time=2)
        self.play(Create(marco))
        self.wait(1)
 
        fin = Text("¡Gracias!", font_size=40, color=GREEN)
        fin.to_edge(DOWN, buff=0.7)
        self.play(FadeIn(fin, shift=UP * 0.3))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])
 