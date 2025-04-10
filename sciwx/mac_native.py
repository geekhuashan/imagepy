import wx
import wx.lib.agw.aui as aui
import platform
import os
import sys

class MacNativeUI:
    """启用 Mac 原生 UI 风格的类"""
    
    @staticmethod
    def enable_native_ui():
        """启用 Mac 原生界面风格"""
        if platform.system() != 'Darwin':
            return False
            
        try:
            # 使用 wxPython 内置的设置启用原生外观
            # 设置 Mac 特有的选项以获得更原生的外观
            wx.SystemOptions.SetOption("mac.window-plain-transition", 1)
            wx.SystemOptions.SetOption("mac.textcontrol-use-spell-checker", 1)
            wx.SystemOptions.SetOption("mac.dialog-toolbar-icon-size", 1)  # 使用小图标
            wx.SystemOptions.SetOption("mac.always-show-scrollbars", 0)  # 只在需要时显示滚动条
            
            # 如果平台支持，启用原生高 DPI 支持
            wx.SystemOptions.SetOption("mac.hidpi", 1)
            
            # 禁用原本可能使界面看起来非 Mac 化的选项
            wx.SystemOptions.SetOption("msw.remap", 0)  # 禁用 Windows 特有的重映射
            wx.SystemOptions.SetOption("msw.notebook.themed-background", 0)
            
            return True
        except Exception as e:
            print(f"启用 Mac 原生界面风格时出错: {e}")
            return False
    
    @staticmethod
    def apply_to_frame(frame):
        """将 Mac 原生风格应用到窗口"""
        if platform.system() != 'Darwin':
            return False
            
        try:
            # 设置窗口样式标志，使用更原生的 Mac 窗口
            # 移除可能影响原生外观的样式
            style = frame.GetWindowStyle()
            style &= ~wx.BORDER_NONE
            style |= wx.BORDER_DEFAULT
            frame.SetWindowStyle(style)
            
            # 设置标题栏为半透明（仅适用于某些 macOS 版本）
            frame.EnableFullScreenView(True)  # 启用全屏视图（macOS 风格）
            
            # 为窗口设置最小大小，防止过小导致界面变形
            frame.SetMinSize(wx.Size(800, 600))
            
            return True
        except Exception as e:
            print(f"应用 Mac 原生窗口风格时出错: {e}")
            return False
    
    @staticmethod
    def fix_button_appearance(button):
        """修复按钮外观，使其更符合 Mac 风格"""
        if platform.system() != 'Darwin':
            return False
            
        try:
            # 移除可能导致按钮看起来不像 Mac 原生按钮的样式
            style = button.GetWindowStyle()
            # 移除可能存在的样式
            style &= ~wx.BORDER_NONE
            style &= ~wx.BORDER_SIMPLE
            # 添加默认边框样式
            style |= wx.BORDER_DEFAULT
            button.SetWindowStyle(style)
            
            return True
        except Exception as e:
            print(f"修复按钮外观时出错: {e}")
            return False
    
    @staticmethod
    def setup_mac_menu(frame):
        """设置 Mac 风格的菜单"""
        if platform.system() != 'Darwin':
            return False
            
        try:
            app = wx.App.Get()
            # 设置应用名称，用于 "应用程序" 菜单
            app.SetAppName("ImagePy")
            
            # 在 Mac 上，wx 会自动处理常见的 Mac 菜单项
            # 如"关于"、"首选项"等
            
            return True
        except Exception as e:
            print(f"设置 Mac 菜单时出错: {e}")
            return False
            
    @staticmethod
    def fix_controls_for_mac(parent):
        """递归修复所有控件使其符合 Mac 风格"""
        if platform.system() != 'Darwin':
            return False
            
        try:
            for child in parent.GetChildren():
                # 根据控件类型应用 Mac 原生风格
                
                if isinstance(child, wx.Button):
                    MacNativeUI.fix_button_appearance(child)
                    
                # 修复标签页控件
                if isinstance(child, wx.Notebook) or isinstance(child, wx.aui.AuiNotebook):
                    # 确保使用默认风格
                    style = child.GetWindowStyle()
                    child.SetWindowStyleFlag(style | wx.TAB_TRAVERSAL)
                
                # 修复文本控件
                if isinstance(child, wx.TextCtrl):
                    # 启用拼写检查等 Mac 特性
                    if 'SetSpellCheckingEnabled' in dir(child):
                        child.SetSpellCheckingEnabled(True)
                
                # 递归处理子控件
                if hasattr(child, 'GetChildren'):
                    MacNativeUI.fix_controls_for_mac(child)
                    
            return True
        except Exception as e:
            print(f"修复 Mac 控件时出错: {e}")
            return False
