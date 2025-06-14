from pywinauto import Application
import time

# Start Notepad (Windows only)
app = Application(backend="uia").start("notepad.exe")

# Wait for the Notepad window to be ready
dlg = app.window(title_re=".*Notepad")
dlg.wait("ready", timeout=10)

# Type some text into the editor
test_message = "Hello, pywinauto!"
dlg.Edit.type_keys(test_message, with_spaces=True)

# Give it a moment to update
time.sleep(1)

# Read the text back from the editor
current_text = dlg.Edit.window_text()
print("Text read from Notepad:", current_text)

# Close Notepad without saving
dlg.close()
app.kill()
