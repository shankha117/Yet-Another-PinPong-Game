import ast

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup


class PongGame(Widget):
    ball = ObjectProperty(None)
    player_left = ObjectProperty(None)
    player_right = ObjectProperty(None)
    MAX_SCORE = NumericProperty(20)
    speed = NumericProperty(9)

    def serve(self):

        self.ball.velocity = Vector(self.speed, 0).rotate(randint(0, 360))

    def stop_game(self):
        self.ball.velocity = Vector(0, 0)
        self.ball.center = self.center
        self.player_left.score = 0
        self.player_right.score = 0

    def update(self, dt):

        # Showing Game End

        if self.player_left.score >= self.MAX_SCORE:
            self.stop_game()
            GameEnd(self).ShowPopup("Player 1")
        if self.player_right.score >= self.MAX_SCORE:
            self.stop_game()
            GameEnd(self).ShowPopup("Player 2")

        # moving the ball by calling the move function
        self.ball.move()

        if self.ball.pos[0] < 0:
            self.ball.velocity_x *= -1
            self.ball.pos[0] = 0
            self.player_right.score += 1

        elif self.ball.pos[0] > self.width:
            self.ball.velocity_x *= -1
            self.ball.pos[0] = self.width
            self.player_left.score += 1

        # bounce back top and bottom
        if self.ball.y < 0 or self.ball.y > (self.height - self.ball.size[1]):
            self.ball.velocity_y *= -1

        # bounce back right
        if self.ball.x < 0:
            self.ball.velocity_x *= -1
            self.player_right.score += 1

        # bounce back left
        if self.ball.x > (self.width - self.ball.size[0]):
            self.ball.velocity_x *= -1
            self.player_left.score += 1

        self.player_left.bounce_ball(self.ball)
        self.player_right.bounce_ball(self.ball)

    def on_touch_move(self, touch):

        # left Player
        if touch.x < self.width * (1 / 4):
            if touch.y < 100:
                self.player_left.center_y = 100
            elif touch.y > (self.height - 100):
                self.player_left.center_y = self.height - 100
            else:
                self.player_left.center_y = touch.y

        # Right Player
        if touch.x > self.width * (3 / 4):
            if touch.y < 100:
                self.player_right.center_y = 100
            elif touch.y > (self.height - 100):
                self.player_right.center_y = self.height - 100
            else:
                self.player_right.center_y = touch.y


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # latest pos of the ball = Current Velocity + Current Position
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongBat(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            if abs(ball.velocity_x) <= 15:
                ball.velocity_x *= -1.2
            else:
                ball.velocity_x *= -1

        elif abs(ball.velocity_x) >= 15:

            sign = "-" if ball.velocity_x < 0 else "+"

            ball.velocity_x = ast.literal_eval(sign + "5")


class Popclass(FloatLayout):
    winner = ObjectProperty(None)

    def btn(self):
        GameEnd().restart()

# this is the Borg Class to hold the references of the Singleton Class GameEnd
class Borg:
    _shared_data = {"game_ref": None,"popup_ref":None}

    def __init__(self):
        self.__dict__ = self._shared_data


# this is my singleton Class which saves the instance of the Popup and The Game
# the class references are then used to contol the Game
class GameEnd(Borg):

    def __init__(self, *args):
        if args:
            self._shared_data["game_ref"] = args[0]

    def restart(self):
        self._shared_data["popup_ref"].dismiss()
        self._shared_data["game_ref"].serve()

    def ShowPopup(self, winner):

        show = Popclass()
        show.winner = winner
        popup_window = Popup(title=" Game Finished!  ", content=show, size_hint=(None, None), size=(400, 400),
                             auto_dismiss=True)
        self._shared_data["popup_ref"] = popup_window
        popup_window.open()


class PingPongApp(App):

    def build(self):
        game = PongGame()
        game.serve()
        fps = 90.0
        Clock.schedule_interval(game.update, 1.0 / fps)
        return game


if __name__ == '__main__':
    PingPongApp().run()
