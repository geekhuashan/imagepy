import wx
import wx.lib.agw.aui as aui
import platform
import os

class MacStyle:
    """为 Mac 平台提供优化的样式和界面元素"""
    
    @staticmethod
    def apply_to_frame(frame):
        """应用 Mac 风格到主框架"""
        # 确认是否为 Mac 平台
        if platform.system() != 'Darwin':
            return
            
        # 设置更合适的字体
        default_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        frame.SetFont(default_font)
        
        # 使用 Mac 标准的窗口样式
        frame.SetBackgroundColour(wx.Colour(240, 240, 240))
        
        # 优化 AUI 管理器样式
        if hasattr(frame, 'auimgr'):
            art_provider = MacAuiDockArt()
            frame.auimgr.SetArtProvider(art_provider)
            
        return True
    
    @staticmethod
    def apply_to_toolbar(toolbar):
        """应用 Mac 风格到工具栏"""
        if platform.system() != 'Darwin':
            return
            
        toolbar.SetBackgroundColour(wx.Colour(240, 240, 240))
        return True
    
    @staticmethod
    def get_mac_icon_path(icon_name):
        """获取适用于 Mac 的图标路径"""
        # 这里可以返回专门为 Mac 设计的高分辨率图标
        pass


class MacAuiDockArt(aui.AuiDefaultDockArt):
    """自定义 AUI Dock 样式，使其更符合 Mac 风格"""
    def __init__(self):
        aui.AuiDefaultDockArt.__init__(self)
        
        # 设置颜色和细节以匹配 Mac 风格
        self.SetColour(aui.AUI_DOCKART_BACKGROUND_COLOUR, wx.Colour(240, 240, 240))
        self.SetColour(aui.AUI_DOCKART_SASH_COLOUR, wx.Colour(220, 220, 220))
        self.SetColour(aui.AUI_DOCKART_ACTIVE_CAPTION_COLOUR, wx.Colour(70, 130, 180))
        self.SetColour(aui.AUI_DOCKART_ACTIVE_CAPTION_TEXT_COLOUR, wx.WHITE)
        self.SetColour(aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR, wx.Colour(200, 200, 200))
        self.SetColour(aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR, wx.Colour(50, 50, 50))
        
        # 设置边框宽度和其他尺寸
        self.SetMetric(aui.AUI_DOCKART_PANE_BORDER_SIZE, 1)
        self.SetMetric(aui.AUI_DOCKART_SASH_SIZE, 3)
        self.SetMetric(aui.AUI_DOCKART_CAPTION_SIZE, 22)  # 稍微降低标题栏高度
        
        # 设置其他字体
        caption_font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(aui.AUI_DOCKART_CAPTION_FONT, caption_font)
