from manim import *
from pathlib import Path
import subprocess
import wave

# ============================================================
# Erklärvideo: Brüche erweitern und kürzen
# Klasse 5, mit Denkpausen, Aufgaben und optionalem Ton
# ============================================================

AUDIO_DIR = Path(__file__).with_name("audio_brueche")
USE_AUDIO = True

TRANSCRIPT = {
    "01_intro": "Heute geht es um Brüche, die anders aussehen, aber denselben Anteil beschreiben. Du lernst, wie man Brüche erweitert und kürzt.",
    "02_halb": "Hier ist ein Halb. Die blaue Fläche zeigt genau die Hälfte des Balkens. Jetzt teilen wir jeden Teil noch einmal in zwei kleinere Teile. Aus ein Halb werden zwei Viertel. Der Anteil bleibt gleich groß.",
    "03_merke_erweitern": "Beim Erweitern wird das Ganze feiner eingeteilt. Zähler und Nenner werden mit derselben Zahl malgenommen. Diese Zahl steht über dem Gleichheitszeichen.",
    "04_denken_erweitern": "Denkpause. Aus zwei Dritteln soll ein Bruch mit Nenner sechs werden. Mit welcher Zahl wird erweitert? Überlege kurz. Schaue auf den Nenner: Aus drei soll sechs werden.",
    "05_loesung_erweitern": "Die Erweiterungszahl ist zwei. Drei mal zwei ist sechs. Deshalb rechnen wir auch oben mal zwei. Aus zwei Dritteln werden vier Sechstel.",
    "06_aufgabe1": "Jetzt bist du dran. Erweitere ein Drittel auf den Nenner sechs. Welche Zahl kommt oben in den neuen Bruch?",
    "07_aufgabe1_loesung": "Die Lösung ist zwei Sechstel. Der Nenner wurde mit zwei erweitert. Also wird auch der Zähler mit zwei erweitert.",
    "08_aufgabe2": "Nächste Aufgabe. Erweitere drei Viertel auf den Nenner zwölf. Denke zuerst: Mit welcher Zahl wird vier zu zwölf?",
    "09_aufgabe2_loesung": "Vier wird mit drei zu zwölf. Also wird auch drei mit drei malgenommen. Die Lösung ist neun Zwölftel.",
    "10_aufgabe3": "Noch eine Aufgabe. Erweitere zwei Fünftel mit der Zahl vier. Wie lautet der neue Bruch?",
    "11_aufgabe3_loesung": "Zwei mal vier ist acht. Fünf mal vier ist zwanzig. Also gilt: Zwei Fünftel sind acht Zwanzigstel.",
    "12_merke_kuerzen": "Beim Kürzen machen wir die Schreibweise einfacher. Kleine Teile werden zu größeren Teilen zusammengefasst. Zähler und Nenner werden durch dieselbe Zahl geteilt. Diese Zahl steht unter dem Gleichheitszeichen.",
    "13_denken_kuerzen": "Denkpause. Kürze sechs Achtel. Durch welche Zahl kann man sechs und acht teilen? Überlege kurz.",
    "14_loesung_kuerzen": "Sechs und acht kann man beide durch zwei teilen. Aus sechs Achteln werden drei Viertel. Der Anteil bleibt gleich groß.",
    "15_aufgabe4": "Jetzt du. Kürze vier Sechstel vollständig. Welche Zahl steht unter dem Gleichheitszeichen? Und wie lautet der neue Bruch?",
    "16_aufgabe4_loesung": "Vier und sechs werden durch zwei geteilt. Vier Sechstel sind zwei Drittel.",
    "17_aufgabe5": "Kürze zehn Fünfzehntel. Suche eine Zahl, durch die beide Zahlen teilbar sind.",
    "18_aufgabe5_loesung": "Zehn und fünfzehn werden durch fünf geteilt. Die Lösung ist zwei Drittel.",
    "19_aufgabe6": "Kürze zwölf Achtzehntel möglichst stark. Denke an die größte gemeinsame Zahl, durch die beide teilbar sind.",
    "20_aufgabe6_loesung": "Zwölf und achtzehn sind beide durch sechs teilbar. Zwölf Achtzehntel sind zwei Drittel.",
    "21_fehler": "Achtung Fehler. Wenn oben und unten verschiedene Zahlen benutzt werden, bleibt der Anteil nicht gleich. Man muss oben und unten immer dieselbe Zahl verwenden.",
    "22_abschluss": "Merke dir: Beim Erweitern steht die Erweiterungszahl über dem Gleichheitszeichen. Beim Kürzen steht die Kürzungszahl unter dem Gleichheitszeichen. Der Anteil bleibt gleich groß."
}


def ensure_audio_files():
    """Erzeugt lokale WAV-Dateien mit espeak, falls sie noch fehlen."""
    AUDIO_DIR.mkdir(exist_ok=True)
    for key, text in TRANSCRIPT.items():
        out = AUDIO_DIR / f"{key}.wav"
        if out.exists():
            continue
        try:
            subprocess.run(
                ["espeak", "-v", "de", "-s", "140", "-w", str(out), text],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            # Fallback: keine Audiodatei. Das Video bleibt renderbar.
            pass


def audio_duration(path):
    try:
        with wave.open(str(path), "rb") as wav:
            frames = wav.getnframes()
            rate = wav.getframerate()
            return frames / float(rate)
    except Exception:
        return 0.0


class BruecheErweiternKuerzenMitAudio(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        if USE_AUDIO:
            ensure_audio_files()

        self.szene_01_intro()
        self.szene_02_halb_zu_viertel()
        self.szene_03_merke_erweitern()
        self.szene_04_denkpause_erweitern()
        self.szene_05_aufgabe_erweitern_ein_drittel()
        self.szene_06_aufgabe_erweitern_drei_viertel()
        self.szene_07_aufgabe_erweitern_zwei_fuenftel()
        self.szene_08_merke_kuerzen()
        self.szene_09_denkpause_kuerzen()
        self.szene_10_aufgabe_kuerzen_vier_sechstel()
        self.szene_11_aufgabe_kuerzen_zehn_fuenfzehntel()
        self.szene_12_aufgabe_kuerzen_zwoelf_achtzehntel()
        self.szene_13_fehler()
        self.szene_14_abschluss()

    # ------------------------------------------------------------
    # Grundfunktionen
    # ------------------------------------------------------------

    def speak(self, key, extra_wait=0.0):
        """Spielt den gesprochenen Text ab und gibt die Audiodauer zurück."""
        path = AUDIO_DIR / f"{key}.wav"
        duration = audio_duration(path)
        if USE_AUDIO and path.exists():
            self.add_sound(str(path))
        if extra_wait > 0:
            self.wait(extra_wait)
        return duration

    def clear_scene(self):
        """Entfernt nach jeder Szene alle Mobjects."""
        if len(self.mobjects) > 0:
            self.play(FadeOut(*self.mobjects), run_time=0.6)
        self.clear()
        self.wait(0.2)

    def titel(self, text, size=38):
        t = Text(text, font_size=size, color=BLACK)
        t.to_edge(UP, buff=0.35)
        return t

    def untertitel(self, text, size=25):
        txt = Text(text, font_size=size, color=BLACK, line_spacing=0.9)
        txt.to_edge(DOWN, buff=0.4)
        return txt

    def bruch_label(self, zaehler, nenner, size=48):
        return MathTex(rf"\frac{{{zaehler}}}{{{nenner}}}", font_size=size, color=BLACK)

    def gleichung_erweitern(self, z1, n1, faktor, z2, n2, size=56):
        return MathTex(
            rf"\frac{{{z1}}}{{{n1}}} \overset{{{faktor}}}{{=}} \frac{{{z2}}}{{{n2}}}",
            font_size=size,
            color=BLACK,
        )

    def gleichung_kuerzen(self, z1, n1, faktor, z2, n2, size=56):
        return MathTex(
            rf"\frac{{{z1}}}{{{n1}}} \underset{{{faktor}}}{{=}} \frac{{{z2}}}{{{n2}}}",
            font_size=size,
            color=BLACK,
        )

    def bruch_balken(self, zaehler, nenner, breite=5.0, hoehe=0.65):
        """Gleich langer Balken mit verschiedener Einteilung."""
        gruppe = VGroup()
        teil_breite = breite / nenner

        for i in range(zaehler):
            rect = Rectangle(
                width=teil_breite,
                height=hoehe,
                stroke_width=0,
                fill_color=BLUE,
                fill_opacity=0.65,
            )
            rect.move_to(LEFT * breite / 2 + RIGHT * (teil_breite / 2 + i * teil_breite))
            gruppe.add(rect)

        rahmen = Rectangle(
            width=breite,
            height=hoehe,
            stroke_color=BLACK,
            stroke_width=2,
            fill_opacity=0,
        )
        gruppe.add(rahmen)

        for i in range(1, nenner):
            x = -breite / 2 + i * teil_breite
            linie = Line([x, -hoehe / 2, 0], [x, hoehe / 2, 0], color=BLACK, stroke_width=2)
            gruppe.add(linie)

        return gruppe

    def fragezeichen_balken(self, nenner, breite=5.0, hoehe=0.65):
        balken = self.bruch_balken(0, nenner, breite, hoehe)
        frage = Text("?", font_size=44, color=BLACK)
        frage.move_to(balken.get_center())
        return VGroup(balken, frage)

    def balken_mit_label(self, zaehler, nenner):
        label = self.bruch_label(zaehler, nenner)
        balken = self.bruch_balken(zaehler, nenner)
        return VGroup(label, balken).arrange(DOWN, buff=0.25)

    def aufgaben_layout(self, titeltext, links, rechts_nenner, prompt_text):
        titel = self.titel(titeltext)
        links_gruppe = self.balken_mit_label(*links)
        rechts_gruppe = VGroup(
            MathTex(rf"\frac{{?}}{{{rechts_nenner}}}", font_size=48, color=BLACK),
            self.fragezeichen_balken(rechts_nenner),
        ).arrange(DOWN, buff=0.25)
        links_gruppe.move_to(LEFT * 3.0 + UP * 0.65)
        rechts_gruppe.move_to(RIGHT * 3.0 + UP * 0.65)
        pfeil = Arrow(LEFT * 1.25 + UP * 0.55, RIGHT * 1.25 + UP * 0.55, color=BLACK, buff=0.1)
        prompt = self.untertitel(prompt_text, size=25)
        return titel, links_gruppe, rechts_gruppe, pfeil, prompt

    # ------------------------------------------------------------
    # Szenen
    # ------------------------------------------------------------

    def szene_01_intro(self):
        titel = self.titel("Brüche erweitern und kürzen")
        gross = Text("Gleicher Anteil – andere Schreibweise", font_size=34, color=BLUE)
        gross.move_to(UP * 0.4)
        beispiele = MathTex(
            r"\frac{1}{2}=\frac{2}{4}=\frac{3}{6}",
            font_size=58,
            color=BLACK,
        )
        beispiele.move_to(DOWN * 0.7)

        self.speak("01_intro")
        self.play(Write(titel))
        self.play(FadeIn(gross), run_time=0.8)
        self.play(Write(beispiele), run_time=1.2)
        self.wait(2.5)
        self.clear_scene()

    def szene_02_halb_zu_viertel(self):
        titel = self.titel("Ein Anteil kann gleich bleiben")
        links = self.balken_mit_label(1, 2)
        rechts = self.balken_mit_label(2, 4)
        links.move_to(LEFT * 3.0 + UP * 0.65)
        rechts.move_to(RIGHT * 3.0 + UP * 0.65)
        pfeil = Arrow(LEFT * 1.25 + UP * 0.55, RIGHT * 1.25 + UP * 0.55, color=BLACK, buff=0.1)
        gleichung = self.gleichung_erweitern(1, 2, 2, 2, 4)
        gleichung.move_to(DOWN * 1.05)
        text = self.untertitel("Die blaue Fläche bleibt gleich groß.")

        self.speak("02_halb")
        self.play(Write(titel))
        self.play(FadeIn(links), run_time=0.8)
        self.wait(1.0)
        self.play(GrowArrow(pfeil), run_time=0.5)
        self.play(TransformFromCopy(links, rechts), run_time=1.2)
        self.wait(0.8)
        self.play(Write(gleichung), FadeIn(text), run_time=1.0)
        self.wait(3.0)
        self.clear_scene()

    def szene_03_merke_erweitern(self):
        titel = self.titel("Erweitern")
        regel = Text("Zähler und Nenner werden mit derselben Zahl malgenommen.", font_size=28, color=BLACK)
        position = Text("Die Erweiterungszahl steht über dem Gleichheitszeichen.", font_size=28, color=BLACK)
        formel = MathTex(r"\frac{a}{b}\overset{n}{=}\frac{a\cdot n}{b\cdot n}", font_size=56, color=BLACK)
        gruppe = VGroup(regel, position, formel).arrange(DOWN, buff=0.55).move_to(DOWN * 0.1)

        self.speak("03_merke_erweitern")
        self.play(Write(titel))
        self.play(FadeIn(regel), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(position), run_time=0.8)
        self.wait(0.5)
        self.play(Write(formel), run_time=1.0)
        self.wait(3.0)
        self.clear_scene()

    def szene_04_denkpause_erweitern(self):
        titel, links, rechts_frage, pfeil, prompt = self.aufgaben_layout(
            "Denkpause: Zwei Drittel erweitern",
            (2, 3),
            6,
            "Welche Zahl gehört über das Gleichheitszeichen?",
        )
        frage = MathTex(r"\frac{2}{3}\overset{?}{=}\frac{?}{6}", font_size=56, color=BLACK)
        frage.move_to(DOWN * 1.0)

        self.speak("04_denken_erweitern")
        self.play(Write(titel))
        self.play(FadeIn(links), GrowArrow(pfeil), FadeIn(rechts_frage), run_time=1.2)
        self.play(Write(frage), FadeIn(prompt), run_time=1.0)
        self.wait(5.0)

        loesung_rechts = self.balken_mit_label(4, 6)
        loesung_rechts.move_to(rechts_frage.get_center())
        gleichung = self.gleichung_erweitern(2, 3, 2, 4, 6)
        gleichung.move_to(DOWN * 1.0)
        self.speak("05_loesung_erweitern")
        self.play(Transform(rechts_frage, loesung_rechts), Transform(frage, gleichung), run_time=1.2)
        self.wait(3.0)
        self.clear_scene()

    def szene_05_aufgabe_erweitern_ein_drittel(self):
        titel, links, rechts_frage, pfeil, prompt = self.aufgaben_layout(
            "Aufgabe 1: Erweitere",
            (1, 3),
            6,
            "Denke erst selbst nach. Danach erscheint die Lösung.",
        )
        gleichung_frage = MathTex(r"\frac{1}{3}\overset{?}{=}\frac{?}{6}", font_size=56, color=BLACK).move_to(DOWN * 1.0)

        self.speak("06_aufgabe1")
        self.play(Write(titel), FadeIn(links), GrowArrow(pfeil), FadeIn(rechts_frage), run_time=1.2)
        self.play(Write(gleichung_frage), FadeIn(prompt), run_time=0.8)
        self.wait(5.0)

        rechts_loesung = self.balken_mit_label(2, 6).move_to(rechts_frage.get_center())
        gleichung = self.gleichung_erweitern(1, 3, 2, 2, 6).move_to(DOWN * 1.0)
        self.speak("07_aufgabe1_loesung")
        self.play(Transform(rechts_frage, rechts_loesung), Transform(gleichung_frage, gleichung), run_time=1.2)
        self.wait(3.0)
        self.clear_scene()

    def szene_06_aufgabe_erweitern_drei_viertel(self):
        titel, links, rechts_frage, pfeil, prompt = self.aufgaben_layout(
            "Aufgabe 2: Erweitere",
            (3, 4),
            12,
            "Tipp: Schaue zuerst auf den Nenner.",
        )
        gleichung_frage = MathTex(r"\frac{3}{4}\overset{?}{=}\frac{?}{12}", font_size=56, color=BLACK).move_to(DOWN * 1.0)

        self.speak("08_aufgabe2")
        self.play(Write(titel), FadeIn(links), GrowArrow(pfeil), FadeIn(rechts_frage), run_time=1.2)
        self.play(Write(gleichung_frage), FadeIn(prompt), run_time=0.8)
        self.wait(5.0)

        rechts_loesung = self.balken_mit_label(9, 12).move_to(rechts_frage.get_center())
        gleichung = self.gleichung_erweitern(3, 4, 3, 9, 12).move_to(DOWN * 1.0)
        self.speak("09_aufgabe2_loesung")
        self.play(Transform(rechts_frage, rechts_loesung), Transform(gleichung_frage, gleichung), run_time=1.2)
        self.wait(3.0)
        self.clear_scene()

    def szene_07_aufgabe_erweitern_zwei_fuenftel(self):
        titel = self.titel("Aufgabe 3: Erweitere mit 4")
        links = self.balken_mit_label(2, 5).move_to(LEFT * 3.0 + UP * 0.65)
        rechts_frage = VGroup(
            MathTex(r"\frac{?}{20}", font_size=48, color=BLACK),
            self.fragezeichen_balken(20),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.0 + UP * 0.65)
        pfeil = Arrow(LEFT * 1.25 + UP * 0.55, RIGHT * 1.25 + UP * 0.55, color=BLACK, buff=0.1)
        gleichung_frage = MathTex(r"\frac{2}{5}\overset{4}{=}\frac{?}{20}", font_size=56, color=BLACK).move_to(DOWN * 1.0)
        prompt = self.untertitel("Rechne oben und unten mit 4.")

        self.speak("10_aufgabe3")
        self.play(Write(titel), FadeIn(links), GrowArrow(pfeil), FadeIn(rechts_frage), run_time=1.2)
        self.play(Write(gleichung_frage), FadeIn(prompt), run_time=0.8)
        self.wait(5.0)

        rechts_loesung = self.balken_mit_label(8, 20).move_to(rechts_frage.get_center())
        gleichung = self.gleichung_erweitern(2, 5, 4, 8, 20).move_to(DOWN * 1.0)
        self.speak("11_aufgabe3_loesung")
        self.play(Transform(rechts_frage, rechts_loesung), Transform(gleichung_frage, gleichung), run_time=1.2)
        self.wait(3.0)
        self.clear_scene()

    def szene_08_merke_kuerzen(self):
        titel = self.titel("Kürzen")
        regel = Text("Zähler und Nenner werden durch dieselbe Zahl geteilt.", font_size=28, color=BLACK)
        position = Text("Die Kürzungszahl steht unter dem Gleichheitszeichen.", font_size=28, color=BLACK)
        formel = MathTex(r"\frac{a}{b}\underset{n}{=}\frac{a:n}{b:n}", font_size=56, color=BLACK)
        gruppe = VGroup(regel, position, formel).arrange(DOWN, buff=0.55).move_to(DOWN * 0.1)

        self.speak("12_merke_kuerzen")
        self.play(Write(titel))
        self.play(FadeIn(regel), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(position), run_time=0.8)
        self.wait(0.5)
        self.play(Write(formel), run_time=1.0)
        self.wait(3.0)
        self.clear_scene()

    def szene_09_denkpause_kuerzen(self):
        titel = self.titel("Denkpause: Sechs Achtel kürzen")
        links = self.balken_mit_label(6, 8).move_to(LEFT * 3.0 + UP * 0.65)
        rechts_frage = VGroup(
            MathTex(r"\frac{?}{?}", font_size=48, color=BLACK),
            self.fragezeichen_balken(4),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.0 + UP * 0.65)
        pfeil = Arrow(LEFT * 1.25 + UP * 0.55, RIGHT * 1.25 + UP * 0.55, color=BLACK, buff=0.1)
        gleichung_frage = MathTex(r"\frac{6}{8}\underset{?}{=}\frac{?}{?}", font_size=56, color=BLACK).move_to(DOWN * 1.0)
        prompt = self.untertitel("Durch welche Zahl kannst du 6 und 8 teilen?")

        self.speak("13_denken_kuerzen")
        self.play(Write(titel), FadeIn(links), GrowArrow(pfeil), FadeIn(rechts_frage), run_time=1.2)
        self.play(Write(gleichung_frage), FadeIn(prompt), run_time=0.8)
        self.wait(5.0)

        rechts_loesung = self.balken_mit_label(3, 4).move_to(rechts_frage.get_center())
        gleichung = self.gleichung_kuerzen(6, 8, 2, 3, 4).move_to(DOWN * 1.0)
        self.speak("14_loesung_kuerzen")
        self.play(Transform(rechts_frage, rechts_loesung), Transform(gleichung_frage, gleichung), run_time=1.2)
        self.wait(3.0)
        self.clear_scene()

    def szene_10_aufgabe_kuerzen_vier_sechstel(self):
        titel = self.titel("Aufgabe 4: Kürze vollständig")
        links = self.balken_mit_label(4, 6).move_to(LEFT * 3.0 + UP * 0.65)
        rechts_frage = VGroup(
            MathTex(r"\frac{?}{?}", font_size=48, color=BLACK),
            self.fragezeichen_balken(3),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.0 + UP * 0.65)
        pfeil = Arrow(LEFT * 1.25 + UP * 0.55, RIGHT * 1.25 + UP * 0.55, color=BLACK, buff=0.1)
        gleichung_frage = MathTex(r"\frac{4}{6}\underset{?}{=}\frac{?}{?}", font_size=56, color=BLACK).move_to(DOWN * 1.0)
        prompt = self.untertitel("Welche Zahl steht unter dem Gleichheitszeichen?")

        self.speak("15_aufgabe4")
        self.play(Write(titel), FadeIn(links), GrowArrow(pfeil), FadeIn(rechts_frage), run_time=1.2)
        self.play(Write(gleichung_frage), FadeIn(prompt), run_time=0.8)
        self.wait(5.0)

        rechts_loesung = self.balken_mit_label(2, 3).move_to(rechts_frage.get_center())
        gleichung = self.gleichung_kuerzen(4, 6, 2, 2, 3).move_to(DOWN * 1.0)
        self.speak("16_aufgabe4_loesung")
        self.play(Transform(rechts_frage, rechts_loesung), Transform(gleichung_frage, gleichung), run_time=1.2)
        self.wait(3.0)
        self.clear_scene()

    def szene_11_aufgabe_kuerzen_zehn_fuenfzehntel(self):
        titel = self.titel("Aufgabe 5: Kürze")
        links = self.balken_mit_label(10, 15).move_to(LEFT * 3.0 + UP * 0.65)
        rechts_frage = VGroup(
            MathTex(r"\frac{?}{?}", font_size=48, color=BLACK),
            self.fragezeichen_balken(3),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.0 + UP * 0.65)
        pfeil = Arrow(LEFT * 1.25 + UP * 0.55, RIGHT * 1.25 + UP * 0.55, color=BLACK, buff=0.1)
        gleichung_frage = MathTex(r"\frac{10}{15}\underset{?}{=}\frac{?}{?}", font_size=56, color=BLACK).move_to(DOWN * 1.0)
        prompt = self.untertitel("Suche eine gemeinsame Teilerzahl.")

        self.speak("17_aufgabe5")
        self.play(Write(titel), FadeIn(links), GrowArrow(pfeil), FadeIn(rechts_frage), run_time=1.2)
        self.play(Write(gleichung_frage), FadeIn(prompt), run_time=0.8)
        self.wait(5.0)

        rechts_loesung = self.balken_mit_label(2, 3).move_to(rechts_frage.get_center())
        gleichung = self.gleichung_kuerzen(10, 15, 5, 2, 3).move_to(DOWN * 1.0)
        self.speak("18_aufgabe5_loesung")
        self.play(Transform(rechts_frage, rechts_loesung), Transform(gleichung_frage, gleichung), run_time=1.2)
        self.wait(3.0)
        self.clear_scene()

    def szene_12_aufgabe_kuerzen_zwoelf_achtzehntel(self):
        titel = self.titel("Aufgabe 6: Kürze möglichst stark")
        links = self.balken_mit_label(12, 18).move_to(LEFT * 3.0 + UP * 0.65)
        rechts_frage = VGroup(
            MathTex(r"\frac{?}{?}", font_size=48, color=BLACK),
            self.fragezeichen_balken(3),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.0 + UP * 0.65)
        pfeil = Arrow(LEFT * 1.25 + UP * 0.55, RIGHT * 1.25 + UP * 0.55, color=BLACK, buff=0.1)
        gleichung_frage = MathTex(r"\frac{12}{18}\underset{?}{=}\frac{?}{?}", font_size=56, color=BLACK).move_to(DOWN * 1.0)
        prompt = self.untertitel("Welche möglichst große Zahl passt?")

        self.speak("19_aufgabe6")
        self.play(Write(titel), FadeIn(links), GrowArrow(pfeil), FadeIn(rechts_frage), run_time=1.2)
        self.play(Write(gleichung_frage), FadeIn(prompt), run_time=0.8)
        self.wait(6.0)

        rechts_loesung = self.balken_mit_label(2, 3).move_to(rechts_frage.get_center())
        gleichung = self.gleichung_kuerzen(12, 18, 6, 2, 3).move_to(DOWN * 1.0)
        self.speak("20_aufgabe6_loesung")
        self.play(Transform(rechts_frage, rechts_loesung), Transform(gleichung_frage, gleichung), run_time=1.2)
        self.wait(3.0)
        self.clear_scene()

    def szene_13_fehler(self):
        titel = self.titel("Fehler vermeiden")
        falsch = MathTex(r"\frac{6}{8}=\frac{6:2}{8:4}=\frac{3}{2}", font_size=54, color=BLACK)
        falsch.move_to(UP * 1.25)
        kreuz = VGroup(
            Line(LEFT * 0.45 + UP * 0.45, RIGHT * 0.45 + DOWN * 0.45, color=RED, stroke_width=7),
            Line(LEFT * 0.45 + DOWN * 0.45, RIGHT * 0.45 + UP * 0.45, color=RED, stroke_width=7),
        )
        kreuz.next_to(falsch, RIGHT, buff=0.45)
        hinweis = Text("Oben und unten müssen dieselbe Zahl benutzen.", font_size=28, color=BLACK)
        hinweis.move_to(DOWN * 0.05)
        richtig = self.gleichung_kuerzen(6, 8, 2, 3, 4)
        richtig.move_to(DOWN * 1.25)

        self.speak("21_fehler")
        self.play(Write(titel))
        self.play(Write(falsch), run_time=0.9)
        self.wait(1.0)
        self.play(Create(kreuz), FadeIn(hinweis), run_time=0.8)
        self.wait(1.2)
        self.play(Write(richtig), run_time=1.0)
        self.wait(4.0)
        self.clear_scene()

    def szene_14_abschluss(self):
        titel = self.titel("Merke")
        erweitern = MathTex(r"\frac{a}{b}\overset{n}{=}\frac{a\cdot n}{b\cdot n}", font_size=48, color=BLACK)
        kuerzen = MathTex(r"\frac{a}{b}\underset{n}{=}\frac{a:n}{b:n}", font_size=48, color=BLACK)
        text1 = Text("Erweitern: Zahl über dem Gleichheitszeichen", font_size=27, color=BLACK)
        text2 = Text("Kürzen: Zahl unter dem Gleichheitszeichen", font_size=27, color=BLACK)
        text3 = Text("Der Anteil bleibt gleich groß.", font_size=38, color=BLUE)
        gruppe = VGroup(erweitern, text1, kuerzen, text2, text3).arrange(DOWN, buff=0.42).move_to(DOWN * 0.05)

        self.speak("22_abschluss")
        self.play(Write(titel))
        self.play(Write(erweitern), FadeIn(text1), run_time=1.0)
        self.wait(0.8)
        self.play(Write(kuerzen), FadeIn(text2), run_time=1.0)
        self.wait(0.8)
        self.play(FadeIn(text3), run_time=0.8)
        self.wait(4.0)
        self.clear_scene()
