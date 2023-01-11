from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from plyer import notification


class MainWidget(BoxLayout):
    pass

class TopWidget(BoxLayout):
    num_sessions = ObjectProperty(None)
    session_time = ObjectProperty(None)
    break_time = ObjectProperty(None)
    time_string = StringProperty("00:00")
    remaining_sec = NumericProperty(0)
    session = NumericProperty(0)
    max_reps = None
    current_reps = None
    is_pomo_session = False
    minutes = 0
    seconds = 0
    status_text = StringProperty('')
    timer_color = ColorProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event = None
        self.status_text = 'S T A T U S'
        self.pomodoro_length = int(15 * 60)
        self.break_length = int(5 * 60)
        self.app = App.get_running_app()

    def on_submit(self):
        self.max_reps = int(self.num_sessions.text)
        self.current_reps = self.max_reps
        print(self.max_reps, self.current_reps)
        self.pomodoro_length = int(self.session_time.text) * 60
        self.remaining_sec = self.pomodoro_length
        self.break_length = int(self.break_time.text) * 60
        print(self.pomodoro_length, self.break_length)

    def on_timer_start(self):
        self.stop_timer()
        # print(self.current_reps)

        if self.is_pomo_session:
            self.start_timer(self.break_length)
            self.is_pomo_session = False
        else:
            self.start_timer(self.pomodoro_length)
            self.is_pomo_session = True
        self.toggle_status()

    def on_timer_stop(self):
        self.is_pomo_session = False
        self.current_reps = self.max_reps
        self.stop_timer()

    def toggle_status(self):
        self.session = self.max_reps - self.current_reps + 1
        toggle = ''
        if self.is_pomo_session:
            toggle = 'P O M O D O R O'
            self.timer_color = 122/255, 181/255, 74/255, 1
        else:
            toggle = 'B R E A K'
            self.timer_color = 118/255, 85/255, 201/255, 1
        self.status_text = f'{toggle}  S E S S I O N {self.session}/{self.max_reps}'



    def start_timer(self, duration_sec):
        self.remaining_sec = duration_sec
        self.event = Clock.schedule_interval(self.text_update, 1)

    def stop_timer(self):
        self.remaining_sec = self.pomodoro_length
        if self.event:
            self.event.cancel()

    def start_break(self):
        self.stop_timer()
        self.start_timer(self.break_length)

    def text_update(self, dt):
        self.remaining_sec -= 1
        if not self.remaining_sec:
            if self.current_reps > 1:
                if not self.is_pomo_session:
                    self.current_reps -= 1
                kwargs = {
                    'title': "Pomodoro",
                    'message': "timer stopped",
                }
                self.app.notify(kwargs)
                self.on_timer_start()
            else:
                self.stop_timer()
                print(self.current_reps)




    def on_remaining_sec(self, *args):
        self.minutes = int(self.remaining_sec // 60)
        self.seconds = int(self.remaining_sec % 60)
        self.time_string = f"{self.minutes}:{self.seconds:02}"




class TopInput(TextInput):
    pass
class ClockFace(BoxLayout):
    pass


class PomodoroApp(App):
    def build(self):
        return TopWidget()

    def notify(self, kwargs):
        kwargs['timeout'] = 10
        notification.notify(**kwargs)


PomodoroApp().run()