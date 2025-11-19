"""Complete desktop automation system for Vani - All-in-one solution (Async)."""

import asyncio
import subprocess
import os
import psutil
import pyautogui
import time
import re
from pathlib import Path
from typing import Optional
from .logger import logger

class DesktopAutomation:
    """Complete desktop control system (Async)."""
    
    def __init__(self):
        # Safety
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
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
        
        self.websites = {
            'youtube': 'youtube.com',
            'google': 'google.com',
            'gmail': 'gmail.com',
            'facebook': 'facebook.com',
            'twitter': 'twitter.com',
            'github': 'github.com',
        }
        
        logger.info("✅ Desktop automation ready")
    
    def execute(self, command: str, lang: str = 'en') -> Optional[str]:
        """Execute desktop command (Synchronous wrapper for compatibility)."""
        # Note: This method is kept synchronous because it's called from synchronous parts of LLM handler
        # In a full async rewrite, this would be async.
        # For now, we'll use asyncio.run() or just run sync code if it's fast enough.
        # However, since LLM handler is now async, we should make this async too.
        # But LLM handler calls this. Let's make this async and update LLM handler call site.
        # Wait, LLM handler call site IS async now. So we can make this async.
        pass

    async def execute(self, command: str, lang: str = 'en') -> Optional[str]:
        """Execute desktop command (Async)."""
        cmd = command.lower().strip().rstrip('.!?,')
        
        # 1. Open website
        if self._has_website(cmd):
            return await self._open_website(cmd, lang)
        
        # 2. Open application
        if self._is_open_app(cmd):
            return await self._open_app(cmd, lang)
        
        # 3. Close application
        if self._is_close_app(cmd):
            return await self._close_app(cmd, lang)
        
        # 4. System commands
        if 'screenshot' in cmd:
            return await self._screenshot(lang)
        
        if 'battery' in cmd or 'system' in cmd:
            return await self._system_info(lang)
        
        if 'volume' in cmd:
            return await self._volume(cmd, lang)
        
        return None
    
    def _has_website(self, cmd: str) -> bool:
        indicators = list(self.websites.keys()) + ['website', '.com', 'browse', 'visit', 'go to']
        return any(word in cmd for word in indicators)
    
    async def _open_website(self, cmd: str, lang: str) -> str:
        website = None
        for name, url in self.websites.items():
            if name in cmd:
                website = url
                break
        
        if not website:
            match = re.search(r'([a-zA-Z0-9-]+\.(com|org|net|io))', cmd)
            if match:
                website = match.group(1)
        
        browser = None
        if 'firefox' in cmd:
            browser = 'firefox'
        elif 'chrome' in cmd:
            browser = 'chrome'
        
        if website:
            try:
                if not website.startswith('http'):
                    website = f"https://{website}"
                
                if browser:
                    browser_cmd = self.apps.get(browser, browser)
                    proc = await asyncio.create_subprocess_exec(
                        browser_cmd, website,
                        stdout=asyncio.subprocess.DEVNULL,
                        stderr=asyncio.subprocess.DEVNULL
                    )
                else:
                    proc = await asyncio.create_subprocess_exec(
                        'xdg-open', website,
                        stdout=asyncio.subprocess.DEVNULL,
                        stderr=asyncio.subprocess.DEVNULL
                    )
                
                logger.info(f"✅ Opened {website}")
                
                if lang == 'hi': return f"{website} खोल रहा हूं"
                elif lang == 'gu': return f"{website} ખોલી રહ્યો છું"
                else: return f"Opening {website}"
            except Exception as e:
                logger.error(f"❌ Failed: {e}")
                return f"Could not open {website}"
        
        return "I couldn't find which website to open"
    
    def _is_open_app(self, cmd: str) -> bool:
        return any(w in cmd for w in ['open', 'launch', 'start', 'run'])
    
    async def _open_app(self, cmd: str, lang: str) -> str:
        if self._has_website(cmd): return None
        
        app = None
        for name, cmd_str in self.apps.items():
            if name in cmd:
                app = name
                app_cmd = cmd_str
                break
        
        if app:
            try:
                await asyncio.create_subprocess_exec(
                    app_cmd,
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL
                )
                await asyncio.sleep(0.5)
                logger.info(f"✅ Opened {app}")
                
                if lang == 'hi': return f"{app} खोल दिया"
                elif lang == 'gu': return f"{app} ખોલ્યું"
                else: return f"Opening {app}"
            except Exception as e:
                logger.error(f"❌ Failed: {e}")
                return f"Could not open {app}"
        
        return "I couldn't find which application to open"
    
    def _is_close_app(self, cmd: str) -> bool:
        return any(w in cmd for w in ['close', 'quit', 'exit', 'kill', 'stop'])
    
    async def _close_app(self, cmd: str, lang: str) -> str:
        # Process killing is blocking, run in executor
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._close_app_sync, cmd, lang)

    def _close_app_sync(self, cmd: str, lang: str) -> str:
        proc_map = {
            'terminal': 'gnome-terminal',
            'firefox': 'firefox',
            'chrome': 'chrome',
            'files': 'nautilus',
            'calculator': 'gnome-calculator',
            'text editor': 'gedit',
            'code': 'code',
        }
        
        target = None
        proc_name = None
        
        for name, pname in proc_map.items():
            if name in cmd:
                target = name
                proc_name = pname
                break
        
        if proc_name:
            killed = False
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
            
            if killed:
                logger.info(f"✅ Closed {target}")
                if lang == 'hi': return f"{target} बंद कर दिया"
                elif lang == 'gu': return f"{target} બંધ કર્યું"
                else: return f"Closed {target}"
            else:
                if lang == 'hi': return f"{target} चालू नहीं है"
                elif lang == 'gu': return f"{target} ચાલુ નથી"
                else: return f"{target} is not running"
        
        return "I couldn't find which application to close"
    
    async def _screenshot(self, lang: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._screenshot_sync, lang)

    def _screenshot_sync(self, lang: str) -> str:
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            path = os.path.join(str(Path.home()), 'Pictures', filename)
            
            pyautogui.screenshot(path)
            logger.info(f"✅ Screenshot: {path}")
            
            if lang == 'hi': return f"स्क्रीनशॉट यहाँ सहेजा: {path}"
            elif lang == 'gu': return f"સ્ક્રીનશોટ અહીં સાચવ્યો: {path}"
            else: return f"Screenshot saved to {path}"
        except Exception as e:
            logger.error(f"❌ Screenshot failed: {e}")
            return "Could not take screenshot"
    
    async def _system_info(self, lang: str) -> str:
        try:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            
            battery = "N/A"
            try:
                bat = psutil.sensors_battery()
                if bat:
                    battery = f"{bat.percent}% ({'charging' if bat.power_plugged else 'on battery'})"
            except: pass
            
            if lang == 'hi': return f"CPU: {cpu}%\nमेमोरी: {mem}%\nबैटरी: {battery}"
            elif lang == 'gu': return f"CPU: {cpu}%\nમેમરી: {mem}%\nબેટરી: {battery}"
            else: return f"CPU: {cpu}%\nMemory: {mem}%\nBattery: {battery}"
        except Exception as e:
            logger.error(f"❌ Failed: {e}")
            return "Could not get system info"
    
    async def _volume(self, cmd: str, lang: str) -> str:
        try:
            if 'up' in cmd or 'increase' in cmd:
                await asyncio.create_subprocess_exec('amixer', 'set', 'Master', '5%+')
                return "Volume increased" if lang == 'en' else "आवाज़ बढ़ा दी"
            elif 'down' in cmd or 'decrease' in cmd:
                await asyncio.create_subprocess_exec('amixer', 'set', 'Master', '5%-')
                return "Volume decreased" if lang == 'en' else "आवाज़ कम कर दी"
            elif 'mute' in cmd:
                await asyncio.create_subprocess_exec('amixer', 'set', 'Master', 'toggle')
                return "Volume muted" if lang == 'en' else "आवाज़ बंद कर दी"
        except Exception as e:
            logger.error(f"❌ Failed: {e}")
        
        return "Volume command not recognized"
