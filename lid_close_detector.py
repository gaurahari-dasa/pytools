import ctypes
import win32con
import win32gui
import win32api
import winsound

WM_POWERBROADCAST = 0x0218
PBT_APMSUSPEND = 0x0004

class PowerEventMonitor:
    def __init__(self):
        self.className = "PowerEventMonitorWindow"
        self.hInstance = win32api.GetModuleHandle(None)
        self.wndClass = win32gui.WNDCLASS()
        self.wndClass.lpfnWndProc = self.wndProc
        self.wndClass.lpszClassName = self.className
        self.wndClass.hInstance = self.hInstance
        self.classAtom = win32gui.RegisterClass(self.wndClass)
        self.hWnd = win32gui.CreateWindow(
            self.classAtom,
            self.className,
            0, 0, 0, 0, 0,
            0, 0,
            self.hInstance,
            None
        )

    def wndProc(self, hWnd, msg, wParam, lParam):
        if msg == WM_POWERBROADCAST and wParam == PBT_APMSUSPEND:
            print("Lid closed - triggering beep")
            winsound.Beep(1000, 500)  # Frequency: 1000Hz, Duration: 500ms
        return win32gui.DefWindowProc(hWnd, msg, wParam, lParam)

    def run(self):
        print("Monitoring power events. Press Ctrl+C to exit.")
        while True:
            win32gui.PumpWaitingMessages()

if __name__ == "__main__":
    monitor = PowerEventMonitor()
    monitor.run()
