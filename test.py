#!/usr/bin/env python3
 
import multiprocessing as mp
import time
 
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
 
 
def really_looong_operation(state):
    """
    Do something that will block your app for a long time
    """
    # tick every 200 milliseconds
    tick = 0.2
    state.value = 0
    for k in range(100):
        # In real life this might be invert a huge matrix or whatever...
        time.sleep(tick)
        state.value = k + 1
    # Final activity...
    time.sleep(2*tick)
 
 
class PBarDemo(Gtk.Window):
 
    def __init__(self):
        super().__init__(title="Progressing...")
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(10)
 
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.add(vbox)
         
        self.pbar = Gtk.ProgressBar()
        self.pbar.set_show_text(True)
        vbox.pack_start(self.pbar, True, True, 0)
 
        self.switch = Gtk.Switch()
        self.switch.connect("notify::active", self.on_start_stop)
        vbox.pack_start(self.switch, True, True, 0)
 
        self.tid = None
        self.proc = None
        self.state = mp.Value('i', 0)
        # Guarantee the start state
        self._stop()
     
    def _stop(self):
        # Guarantee that everything is in "stop mode"
        if self.tid is not None:
            GObject.source_remove(self.tid)
         
        if self.proc is not None and self.proc.is_alive():
            self.proc.terminate()
        self.tid = None
        self.proc = None
        self.pbar.set_fraction(0.0)
        self.pbar.set_text('Ready...')
 
    def on_start_stop(self, switch, prop):
        # Check this is the right property
        if prop.name != "active":
            return
         
        self._stop()
        if not switch.get_active():
            return
        # Launch the activity... depending of what you want to do,
        # it might be better to use a pool of workers or other tricks
        self.proc = mp.Process(target=really_looong_operation, args=(self.state,))
        self.proc.start()
        # And the timer that update the progressbar
        self.tid = GObject.timeout_add(250, self.running, None)
        self.pbar.set_text("0%")
 
    def running(self, ignored):
        value = self.state.value
        if value >= 100:
            # Stop working at 100%
            self.proc.join()
            self._stop()
            self.switch.set_active(False)
            # Return false to stop the timer
            return False
        else:
            frac = value / 100
            self.pbar.set_fraction(frac)
            self.pbar.set_text(f"{frac:.0%}")
 
            # Return True so this timer is considered active
            return True
 
 
if __name__ == '__main__':
    win = PBarDemo()
    win.show_all()
    Gtk.main()