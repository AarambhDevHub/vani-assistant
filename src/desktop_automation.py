"""Complete desktop automation system for Vani - All-in-one solution."""

import subprocess
import os
import psutil
import pyautogui
import time
import re
from pathlib import Path
from typing import Optional, List, Dict


class DesktopAutomation:
    """Complete desktop control system."""
    
    def __init__(self):
        # Safety
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        # Application commands
        self.apps = {
            'firefox': 'firefox',
            'chrome': 'google-chrome',
            'chromium': 'chromium-browser',
            'terminal': 'gnome-terminal',
            'files': 'nautilus',
            'calculator': 'gnome-calculator',
            'text editor': 'gedit',
            'code': 'code',
            'settings': 'gnome-control-center',
        }
        
        # Popular websites
        self.websites = {
            'youtube': 'youtube.com',
            'google': 'google.com',
            'gmail': 'gmail.com',
            'facebook': 'facebook.com',
            'twitter': 'twitter.com',
            'github': 'github.com',
        }
        
        print("✅ Desktop automation ready")
    
    def execute(self, command: str, lang: str = 'en') -> Optional[str]:
        """Execute desktop command."""
        cmd = command.lower().strip()
        
        # Remove punctuation
        cmd = cmd.rstrip('.!?,')
        
        # 1. Open website
        if self._has_website(cmd):
            return self._open_website(cmd, lang)
        
        # 2. Open application
        if self._is_open_app(cmd):
            return self._open_app(cmd, lang)
        
        # 3. Close application
        if self._is_close_app(cmd):
            return self._close_app(cmd, lang)
        
        # 4. System commands
        if 'screenshot' in cmd:
            return self._screenshot(lang)
        
        if 'battery' in cmd or 'system' in cmd:
            return self._system_info(lang)
        
        if 'volume' in cmd:
            return self._volume(cmd, lang)
        
        return None
    
    def _has_website(self, cmd: str) -> bool:
        """Check if command mentions a website."""
        indicators = list(self.websites.keys()) + [
            'website', '.com', 'browse', 'visit', 'go to'
        ]
        return any(word in cmd for word in indicators)
    
    def _open_website(self, cmd: str, lang: str) -> str:
        """Open website intelligently."""
        # Find website
        website = None
        for name, url in self.websites.items():
            if name in cmd:
                website = url
                break
        
        # Extract .com URLs
        if not website:
            match = re.search(r'([a-zA-Z0-9-]+\.(com|org|net|io))', cmd)
            if match:
                website = match.group(1)
        
        # Find browser
        browser = None
        if 'firefox' in cmd:
            browser = 'firefox'
        elif 'chrome' in cmd:
            browser = 'chrome'
        
        # Open it
        if website:
            try:
                if not website.startswith('http'):
                    website = f"https://{website}"
                
                if browser:
                    browser_cmd = self.apps.get(browser, browser)
                    subprocess.Popen([browser_cmd, website], 
                                   stdout=subprocess.DEVNULL, 
                                   stderr=subprocess.DEVNULL)
                else:
                    subprocess.Popen(['xdg-open', website],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
                
                print(f"✅ Opened {website}")
                
                if lang == 'hi':
                    return f"{website} खोल रहा हूं"
                elif lang == 'gu':
                    return f"{website} ખોલી રહ્યો છું"
                else:
                    return f"Opening {website}"
            except Exception as e:
                print(f"❌ Failed: {e}")
                return f"Could not open {website}"
        
        return "I couldn't find which website to open"
    
    def _is_open_app(self, cmd: str) -> bool:
        """Check if opening app."""
        return any(w in cmd for w in ['open', 'launch', 'start', 'run'])
    
    def _open_app(self, cmd: str, lang: str) -> str:
        """Open application."""
        # If it's a website, skip
        if self._has_website(cmd):
            return None
        
        # Find app
        app = None
        for name, cmd_str in self.apps.items():
            if name in cmd:
                app = name
                app_cmd = cmd_str
                break
        
        if app:
            try:
                subprocess.Popen([app_cmd],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
                time.sleep(0.5)
                print(f"✅ Opened {app}")
                
                if lang == 'hi':
                    return f"{app} खोल दिया"
                elif lang == 'gu':
                    return f"{app} ખોલ્યું"
                else:
                    return f"Opening {app}"
            except Exception as e:
                print(f"❌ Failed: {e}")
                return f"Could not open {app}"
        
        return "I couldn't find which application to open"
    
    def _is_close_app(self, cmd: str) -> bool:
        """Check if closing app."""
        return any(w in cmd for w in ['close', 'quit', 'exit', 'kill', 'stop'])
    
    def _close_app(self, cmd: str, lang: str) -> str:
        """Close application."""
        # Process name mappings
        proc_map = {
            'terminal': 'gnome-terminal',
            'firefox': 'firefox',
            'chrome': 'chrome',
            'files': 'nautilus',
            'calculator': 'gnome-calculator',
            'text editor': 'gedit',
            'code': 'code',
        }
        
        # Find what to close
        target = None
        proc_name = None
        
        for name, pname in proc_map.items():
            if name in cmd:
                target = name
                proc_name = pname
                break
        
        if proc_name:
            killed = False
            
            # Kill all matching processes
            for proc in psutil.process_iter(['name', 'cmdline']):
                try:
                    pinfo = proc.info
                    if pinfo['name'] and proc_name in pinfo['name'].lower():
                        proc.terminate()
                        killed = True
                    elif pinfo['cmdline'] and any(proc_name in str(arg).lower() for arg in pinfo['cmdline']):
                        proc.terminate()
                        killed = True
                except:
                    pass
            
            # Force kill after delay
            time.sleep(0.5)
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] and proc_name in proc.info['name'].lower():
                        proc.kill()
                        killed = True
                except:
                    pass
            
            if killed:
                print(f"✅ Closed {target}")
                
                if lang == 'hi':
                    return f"{target} बंद कर दिया"
                elif lang == 'gu':
                    return f"{target} બંધ કર્યું"
                else:
                    return f"Closed {target}"
            else:
                if lang == 'hi':
                    return f"{target} चालू नहीं है"
                elif lang == 'gu':
                    return f"{target} ચાલુ નથી"
                else:
                    return f"{target} is not running"
        
        return "I couldn't find which application to close"
    
    def _screenshot(self, lang: str) -> str:
        """Take screenshot."""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            path = os.path.join(str(Path.home()), 'Pictures', filename)
            
            pyautogui.screenshot(path)
            print(f"✅ Screenshot: {path}")
            
            if lang == 'hi':
                return f"स्क्रीनशॉट यहाँ सहेजा: {path}"
            elif lang == 'gu':
                return f"સ્ક્રીનશોટ અહીં સાચવ્યો: {path}"
            else:
                return f"Screenshot saved to {path}"
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
            return "Could not take screenshot"
    
    def _system_info(self, lang: str) -> str:
        """Get system info."""
        try:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            
            battery = None
            try:
                bat = psutil.sensors_battery()
                if bat:
                    battery = f"{bat.percent}% ({'charging' if bat.power_plugged else 'on battery'})"
            except:
                battery = "N/A"
            
            if lang == 'hi':
                info = f"CPU: {cpu}%\nमेमोरी: {mem}%\nबैटरी: {battery}"
            elif lang == 'gu':
                info = f"CPU: {cpu}%\nમેમરી: {mem}%\nબેટરી: {battery}"
            else:
                info = f"CPU: {cpu}%\nMemory: {mem}%\nBattery: {battery}"
            
            return info
        except Exception as e:
            print(f"❌ Failed: {e}")
            return "Could not get system info"
    
    def _volume(self, cmd: str, lang: str) -> str:
        """Control volume."""
        try:
            if 'up' in cmd or 'increase' in cmd:
                subprocess.run(['amixer', 'set', 'Master', '5%+'])
                return "Volume increased" if lang == 'en' else "आवाज़ बढ़ा दी"
            elif 'down' in cmd or 'decrease' in cmd:
                subprocess.run(['amixer', 'set', 'Master', '5%-'])
                return "Volume decreased" if lang == 'en' else "आवाज़ कम कर दी"
            elif 'mute' in cmd:
                subprocess.run(['amixer', 'set', 'Master', 'toggle'])
                return "Volume muted" if lang == 'en' else "आवाज़ बंद कर दी"
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        return "Volume command not recognized"
