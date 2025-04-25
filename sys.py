import json
import threading
import time
import pygetwindow as gw
import keyboard
import win32gui
import win32ui
import win32con
import tkinter as tk
from tkinter import simpledialog, messagebox
from pystray import Icon, Menu as TrayMenu, MenuItem
from PIL import Image

# Global dictionary to store hidden windows using hwnd as key.
# Each value is a dict: { "window": <pygetwindow object>, "title": <current title>, "icon": <tray icon> }
hidden_windows = {}
default_icon = Image.open("app_icon.png")
main_icon = None

def get_window_icon(hwnd):
    try:
        hicon = win32gui.SendMessage(hwnd, win32con.WM_GETICON, win32con.ICON_BIG, 0)
        if hicon == 0:
            hicon = win32gui.SendMessage(hwnd, win32con.WM_GETICON, win32con.ICON_SMALL, 0)
        if hicon == 0:
            hicon = win32gui.GetClassLong(hwnd, win32con.GCL_HICON)
        if hicon == 0:
            hicon = win32gui.GetClassLong(hwnd, win32con.GCL_HICONSM)

        if hicon:
            hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(hwnd))
            hdc_mem = hdc.CreateCompatibleDC()
            bmp = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(hdc, 38, 38)
            hdc_mem.SelectObject(bmp)
            hdc_mem.DrawIcon((0, 0), hicon)
            bmp_info = bmp.GetInfo()
            bmp_str = bmp.GetBitmapBits(True)
            icon = Image.frombuffer(
                'RGBA',
                (bmp_info['bmWidth'], bmp_info['bmHeight']),
                bmp_str, 'raw', 'BGRA', 0, 1
            )
            return icon
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while getting window icon: {e}")
        return None

def update_tray_title(icon,hwnd):
    """ Continuously monitor and update the tray icon title safely. """
    try:
        while hwnd in hidden_windows:
            new_title = win32gui.GetWindowText(hwnd)  # Get latest window title
            icon = hidden_windows[hwnd]["icon"]

            if icon.title != new_title:
                # Preserve icon settings
                current_image = icon.icon
                current_menu = icon.menu
                
                # Stop the old icon safely
                icon.stop()

                # Create a new icon with updated title
                new_icon = Icon(new_title, current_image, title=new_title, menu=current_menu)
                new_icon.run_detached()

                # Replace the old icon in hidden_windows
                hidden_windows[hwnd]["icon"] = new_icon
                hidden_windows[hwnd]["title"] = new_title # Update the title in the dict

            time.sleep(2)  # Reduce frequency to prevent excessive updates
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while updating tray icon title: {e}")

def hide_window(window_to_hide=None):
    try:
        if window_to_hide:
            original_title = window_to_hide.title
            hwnd = win32gui.FindWindow(None, original_title)
            if not hwnd:
                messagebox.showerror("Error", "Window not found or already hidden.")
                return
            # Hide the window (using pygetwindow and win32gui)
            window_to_hide.hide()
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
            
            # Use the hwnd as the key.
            hidden_windows[hwnd] = {"window": window_to_hide, "title": original_title}
            
            # Retrieve the window icon.
            icon_image = get_window_icon(hwnd)
            if icon_image:
                icon_image = icon_image.convert('RGBA')
                tray_icon = Icon(original_title, icon_image, title=original_title)
            else:
                tray_icon = Icon(original_title, default_icon, title=original_title)
            
            tray_icon.menu = TrayMenu(
                MenuItem(f"Restore {original_title}", lambda: restore_window(window_to_hide, tray_icon), default=True),
            )
            tray_icon.run_detached()
            hidden_windows[hwnd]["icon"] = tray_icon
            
            # Start a background thread to update the tray icon title.
            threading.Thread(target=update_tray_title, args=(tray_icon, hwnd), daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while hiding window: {e}")

def restore_window(window_to_restore, icon):
    try:
        hwnd_to_restore = None
        # Identify the hwnd corresponding to the window object.
        for hwnd, data in list(hidden_windows.items()):
            if data["window"] == window_to_restore:
                hwnd_to_restore = hwnd
                icon = data["icon"]
                break
        if hwnd_to_restore is None:
            return
        # Show the window again.
        win32gui.ShowWindow(hwnd_to_restore, win32con.SW_SHOW)
        window_to_restore.activate()
        window_to_restore.maximize()
        try:
            icon.stop()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while stopping tray icon: {e}")
        # Remove the window from our hidden_windows dict.
        if hwnd_to_restore in hidden_windows:
            del hidden_windows[hwnd_to_restore]
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while restoring window: {e}")
        icon.stop()

def hide_active_window():
    active_window = gw.getActiveWindow()
    hide_window(active_window)

def update_shortcut():
    global shortcut
    try:
        new_shortcut = simpledialog.askstring("Shortcut", "Enter the new shortcut (e.g., Ctrl+Shift+H):")
        if not new_shortcut:
            return
        with open('shortcut.json', 'w') as file:
            json.dump({"shortcut": new_shortcut}, file)
        keyboard.remove_hotkey(shortcut)  # Remove old shortcut
        keyboard.add_hotkey(new_shortcut, hide_active_window)  # Add new one
        shortcut = new_shortcut  # Update the global shortcut variable
        messagebox.showinfo("Shortcut Updated", "The new shortcut has been updated.")
    except ValueError:
        messagebox.showerror("Error", "Invalid shortcut format. Please use a valid format like Ctrl+Shift+H.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Shortcut file not found. Please create it first.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Error decoding JSON. Please check the file format.")
    except KeyboardInterrupt:
        messagebox.showerror("Error", "Keyboard interrupt. Please try again.")
    except PermissionError:
        messagebox.showerror("Error", "Permission denied. Please check your file permissions.")
    except OSError:
        messagebox.showerror("Error", "OS error. Please check your system settings.")
    except TypeError:
        messagebox.showerror("Error", "Invalid type. Please check the input.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while updating shortcut: {e}")
def show_shortcut():
    try:
        with open('shortcut.json', 'r') as file:
            shortcut_data = json.load(file)
            current_shortcut = shortcut_data.get('shortcut')
            messagebox.showinfo("Shortcut", f"The current shortcut is: {current_shortcut}")
    except FileNotFoundError:
        messagebox.showerror("Error", "Shortcut file not found. Please create it first.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Error decoding JSON. Please check the file format.")
    except KeyboardInterrupt:
        messagebox.showerror("Error", "Keyboard interrupt. Please try again.")
    except PermissionError:
        messagebox.showerror("Error", "Permission denied. Please check your file permissions.")
    except OSError:
        messagebox.showerror("Error", "OS error. Please check your system settings.")
    except TypeError:
        messagebox.showerror("Error", "Invalid type. Please check the input.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading shortcut: {e}")

def restore_all_windows():
    error={}
    for hwnd, window_data in list(hidden_windows.items()):
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
            window_data["window"].restore()
            window_data["window"].activate()
            window_data["icon"].stop()
            del hidden_windows[hwnd]
        except Exception as e:
            error[hwnd] = e
    final_error_string = ""
    for hwnd, error in error.items():
        title=hidden_windows[hwnd]["title"]
        final_error_string += f"Error with {title}: {error}\n"
    if final_error_string:
        messagebox.showerror("Error", f"An error occurred while restoring windows: {final_error_string}")

def exit_application():
    restore_all_windows()
    try:
        root.destroy()
    except:
        pass
    main_icon.stop()

def list_windows():
    global root
    root = tk.Tk()
    root.geometry("1080x500")
    root.title("List of Windows")
    tk.Label(root, text="List of Windows").grid(row=0, column=0)
    yscrollbar = tk.Scrollbar(root)  
    yscrollbar.grid(row=1, column=1, sticky=tk.N+tk.S)
    xscrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    xscrollbar.grid(row=2, column=0, sticky=tk.W+tk.E+tk.N)
    listbox = tk.Listbox(root, fg="black", bg="white", font=("Arial", 15), selectmode=tk.SINGLE, relief=tk.RIDGE, borderwidth=2,)
    for window in gw.getAllWindows():
        if window.title != "":
            listbox.insert(tk.END, window.title)
    def update_list():
        listbox.delete(0, tk.END)
        for window in gw.getAllWindows():
            if window.title != "" and window.title != "List of Windows":
                listbox.insert(tk.END, window.title)
    listbox.bind("<Double-Button-1>", lambda x: hide_window(gw.getWindowsWithTitle(listbox.get(listbox.curselection()[0]))[0]), add="+")
    listbox.bind("<Double-Button-1>", lambda x: update_list(), add="+")
    listbox.grid(row=1, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
    listbox.config(yscrollcommand=yscrollbar.set)
    listbox.config(xscrollcommand=xscrollbar.set)
    yscrollbar.config(command=listbox.yview)
    xscrollbar.config(command=listbox.xview)
    tk.Label(root, text="Double click on the window to hide it.").grid(row=3, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
    tk.Button(root, text="Close App", command=exit_application).grid(row=3, column=0, sticky=tk.W)
    tk.Button(root, text="Close Window", command=main_click).grid(row=3, column=0, sticky=tk.E)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.mainloop()

def main_click():
    try:
        root.destroy()
    except:
        list_windows()

def create_main_tray():
    global main_icon
    main_icon = Icon("System Tray Application", main_icon_image, title="System Tray Application")
    main_icon.menu = TrayMenu(
        MenuItem("List Windows", main_click, default=True),
        MenuItem("Update Shortcut", update_shortcut),
        MenuItem("Restore All Windows", restore_all_windows),
        MenuItem("Show Shortcut", show_shortcut),
        MenuItem("Exit", exit_application)
    )
    main_icon.run()

# Load main tray icon image
main_icon_image = Image.open("main_icon.png")
try:
    with open('shortcut.json', 'r') as file:
        shortcut_data = json.load(file)
        shortcut = shortcut_data.get('shortcut')
except Exception as e:
    shortcut = "Ctrl+Shift+H"
    messagebox.showerror("Error", f"Error While Reading Shortcut current is Ctrl+Shift+H: {e}")

keyboard.add_hotkey(shortcut, hide_active_window)
create_main_tray()
