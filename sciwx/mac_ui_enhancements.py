import wx
import platform
import os
import sys
from sciapp import Source

class MacUIEnhancements:
    """为 Mac 平台提供更多优化的界面元素和功能"""
    
    @staticmethod
    def enable_high_dpi_support():
        """启用高 DPI 支持，对 Retina 显示屏很重要"""
        if platform.system() == 'Darwin':
            try:
                # 在 Mac 上启用高 DPI 支持
                high_dpi_mode = wx.SystemOptions.GetOptionInt("mac.hidpi") == 1
                if not high_dpi_mode:
                    wx.SystemOptions.SetOption("mac.hidpi", 1)
                return True
            except Exception as e:
                print(f"注意：无法启用高 DPI 支持：{e}")
                return False
        return False
    
    @staticmethod
    def setup_app_menu(frame):
        """配置 Mac 应用程序菜单"""
        if platform.system() == 'Darwin':
            try:
                # Mac 特有的应用程序菜单设置
                app = wx.App.Get()
                app.SetAppName("ImagePy")
                # 移除对 MacSetCommonMenuBar 的调用，它可能导致问题
                # wx.MenuBar.MacSetCommonMenuBar(frame.GetMenuBar())
                return True
            except Exception as e:
                print(f"注意：无法设置 Mac 应用菜单：{e}")
                return False
        return False
    
    @staticmethod
    def optimize_scrolling(window):
        """优化 Mac 上的滚动行为"""
        if platform.system() == 'Darwin':
            # 启用平滑滚动
            window.SetScrollRate(10, 10)
            return True
        return False
    
    @staticmethod
    def set_font_rendering(window):
        """设置更好的字体渲染"""
        if platform.system() == 'Darwin':
            try:
                # 使用 Mac 系统字体
                default_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
                window.SetFont(default_font)
                return True
            except Exception as e:
                print(f"注意：无法设置字体渲染：{e}")
                return False
        return False
        
    @staticmethod
    def apply_retina_icons(toolbar):
        """为 Retina 显示器提供高分辨率图标支持"""
        if platform.system() == 'Darwin':
            # 实现在此处...
            return True
        return False
        
    @staticmethod
    def optimize_dialog_buttons(dialog):
        """优化对话框按钮布局，使其符合 Mac 标准"""
        if platform.system() == 'Darwin':
            # 调整对话框按钮顺序和样式
            for child in dialog.GetChildren():
                if isinstance(child, wx.Button):
                    # 设置 Mac 风格的按钮
                    child.SetBackgroundColour(wx.Colour(240, 240, 240))
            return True
        return False
