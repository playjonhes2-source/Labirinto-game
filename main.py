import random
from collections import deque

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class MazeGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(12), spacing=dp(8), **kwargs)
        self.size_n = 11
        self.player = (1, 1)
        self.maze = []
        self.status = Label(text="Encontre a saída verde!", size_hint_y=None,
                            height=dp(42), font_size="18sp")
        self.add_widget(self.status)

        self.board = GridLayout(cols=self.size_n, spacing=dp(2), size_hint=(1, 1))
        self.add_widget(self.board)

        controls = GridLayout(cols=3, rows=2, spacing=dp(6), size_hint_y=None,
                              height=dp(112))
        controls.add_widget(Widget())
        controls.add_widget(self.make_button("▲", lambda: self.move(-1, 0)))
        controls.add_widget(Widget())
        controls.add_widget(self.make_button("◀", lambda: self.move(0, -1)))
        controls.add_widget(self.make_button("▼", lambda: self.move(1, 0)))
        controls.add_widget(self.make_button("▶", lambda: self.move(0, 1)))
        self.add_widget(controls)

        self.add_widget(self.make_button("Novo labirinto", self.new_game, height=46))
        Window.bind(on_key_down=self.on_key_down)
        self.new_game()

    def make_button(self, text, callback, height=dp(50)):
        btn = Button(text=text, font_size="20sp", size_hint_y=None, height=height)
        btn.bind(on_release=lambda *_: callback())
        return btn

    def new_game(self):
        # Gera um labirinto conectado usando busca em profundidade.
        n = self.size_n
        self.maze = [[1 for _ in range(n)] for _ in range(n)]
        start = (1, 1)
        self.maze[1][1] = 0
        stack = [start]
        while stack:
            r, c = stack[-1]
            options = []
            for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nr, nc = r + dr, c + dc
                if 1 <= nr < n - 1 and 1 <= nc < n - 1 and self.maze[nr][nc] == 1:
                    options.append((nr, nc, dr, dc))
            if options:
                nr, nc, dr, dc = random.choice(options)
                self.maze[r + dr // 2][c + dc // 2] = 0
                self.maze[nr][nc] = 0
                stack.append((nr, nc))
            else:
                stack.pop()

        # Saída no canto inferior direito, ligada ao corredor.
        self.maze[n - 2][n - 1] = 0
        self.maze[n - 2][n - 2] = 0
        self.exit = (n - 2, n - 1)
        self.player = start
        self.status.text = "Encontre a saída verde!"
        self.draw_board()

    def draw_board(self):
        self.board.clear_widgets()
        for r in range(self.size_n):
            for c in range(self.size_n):
                if (r, c) == self.player:
                    color = (0.15, 0.55, 1, 1)
                    symbol = "●"
                elif (r, c) == self.exit:
                    color = (0.15, 0.75, 0.3, 1)
                    symbol = "★"
                elif self.maze[r][c] == 1:
                    color = (0.12, 0.14, 0.18, 1)
                    symbol = ""
                else:
                    color = (0.88, 0.9, 0.92, 1)
                    symbol = ""
                cell = Button(text=symbol, background_normal="", background_color=color,
                              color=(1, 1, 1, 1), font_size="18sp")
                self.board.add_widget(cell)

    def move(self, dr, dc):
        if self.player == self.exit:
            return
        r, c = self.player
        nr, nc = r + dr, c + dc
        if 0 <= nr < self.size_n and 0 <= nc < self.size_n and self.maze[nr][nc] == 0:
            self.player = (nr, nc)
            if self.player == self.exit:
                self.status.text = "Parabéns! Você encontrou a saída!"
            self.draw_board()

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        mapping = {273: (-1, 0), 274: (1, 0), 276: (0, -1), 275: (0, 1)}
        if key in mapping:
            self.move(*mapping[key])
            return True
        return False


class LabirintoApp(App):
    def build(self):
        self.title = "Labirinto"
        return MazeGame()


if __name__ == "__main__":
    LabirintoApp().run()
