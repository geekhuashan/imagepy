import wx
import wx.lib.agw.aui as aui
import platform
import os
import sys

class MacStyle:
    """为 Mac 平台提供优化的样式和界面元素"""
    
    # 定义 Mac 专属颜色方案
    COLORS = {
        'window_bg': wx.Colour(246, 246, 246),       # 窗口背景色
        'control_bg': wx.Colour(240, 240, 240),      # 控件背景色
        'panel_bg': wx.Colour(236, 236, 236),        # 面板背景色
        'toolbar_bg': wx.Colour(246, 246, 246),      # 工具栏背景色
        'button_hover': wx.Colour(228, 228, 228),    # 按钮悬停色
        'button_press': wx.Colour(210, 210, 210),    # 按钮按下色
        'selection_bg': wx.Colour(64, 156, 255),     # 选中背景色
        'selection_border': wx.Colour(0, 122, 255),  # 选中边框色
        'heading_color': wx.Colour(80, 80, 80),      # 标题文本色
        'text_color': wx.Colour(50, 50, 50),         # 正文文本色
        'link_color': wx.Colour(0, 112, 201),        # 链接颜色
        'separator': wx.Colour(218, 218, 218),       # 分隔线颜色
    }
    
    # 定义尺寸和布局常量
    METRICS = {
        'button_radius': 4,         # 按钮圆角半径
        'control_padding': 4,       # 控件内边距
        'toolbar_item_margin': 6,   # 工具栏项目间距
        'panel_margin': 8,          # 面板间距
    }
    
    @staticmethod
    def apply_to_frame(frame):
        """应用 Mac 风格到主框架"""
        # 确认是否为 Mac 平台
        if platform.system() != 'Darwin':
            return False
            
        try:
            # 设置更现代的 Mac 字体
            default_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            frame.SetFont(default_font)
            
            # 使用 Mac 标准的窗口样式
            frame.SetBackgroundColour(MacStyle.COLORS['window_bg'])
            
            # 优化 AUI 管理器样式
            if hasattr(frame, 'auimgr'):
                art_provider = MacAuiDockArt()
                frame.auimgr.SetArtProvider(art_provider)
                
            # 适配高 DPI 显示
            frame.EnableFullScreenView(True)
            
            # 优化所有子控件
            MacStyle._style_children(frame)
                
            return True
        except Exception as e:
            print(f"应用 Mac 风格时发生错误: {e}")
            return False
    
    @staticmethod
    def _style_children(parent):
        """递归设置所有子控件的风格"""
        for child in parent.GetChildren():
            # 根据控件类型设置风格
            if isinstance(child, wx.Panel):
                child.SetBackgroundColour(MacStyle.COLORS['panel_bg'])
                child.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            
            elif isinstance(child, wx.Button):
                # 按钮美化
                child.SetBackgroundColour(MacStyle.COLORS['control_bg'])
                child.SetForegroundColour(MacStyle.COLORS['text_color'])
                child.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            
            elif isinstance(child, wx.StaticText):
                # 文本美化
                child.SetForegroundColour(MacStyle.COLORS['text_color'])
                child.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            
            # 递归处理子控件
            if hasattr(child, 'GetChildren'):
                MacStyle._style_children(child)
    
    @staticmethod
    def apply_to_toolbar(toolbar):
        """应用 Mac 风格到工具栏"""
        if platform.system() != 'Darwin':
            return False
            
        try:
            # 设置工具栏背景颜色
            toolbar.SetBackgroundColour(MacStyle.COLORS['toolbar_bg'])
            
            # 为工具栏按钮设置样式
            for child in toolbar.GetChildren():
                if isinstance(child, wx.BitmapButton):
                    # 使按钮圆角化
                    # 注意: 在 wxPython 中需要自定义绘制来实现完全的圆角
                    # 这里只是设置颜色
                    child.SetBackgroundColour(MacStyle.COLORS['toolbar_bg'])
            
            return True
        except Exception as e:
            print(f"应用工具栏 Mac 风格时发生错误: {e}")
            return False
    
    @staticmethod
    def apply_to_notebook(notebook):
        """应用 Mac 风格到标签页控件"""
        if platform.system() != 'Darwin':
            return False
            
        try:
            # 设置标签页头部样式
            notebook.SetBackgroundColour(MacStyle.COLORS['window_bg'])
            
            # 如果是 AUI 类型的标签页
            if isinstance(notebook, aui.AuiNotebook):
                # 设置现代样式的标签页
                notebook.SetArtProvider(aui.AuiSimpleTabArt())
                # 可以根据需要自定义更多风格
            
            return True
        except Exception as e:
            print(f"应用标签页 Mac 风格时发生错误: {e}")
            return False
    
    @staticmethod
    def get_mac_icon_path(icon_name):
        """获取适用于 Mac 的图标路径"""
        # 这里可以返回专门为 Mac 设计的高分辨率图标
        return None


class MacAuiDockArt(aui.AuiDefaultDockArt):
    """自定义 AUI Dock 样式，使其更符合 Mac 风格"""
    def __init__(self):
        aui.AuiDefaultDockArt.__init__(self)
        
        # 设置颜色和细节以匹配现代 Mac 风格
        self.SetColour(aui.AUI_DOCKART_BACKGROUND_COLOUR, MacStyle.COLORS['window_bg'])
        self.SetColour(aui.AUI_DOCKART_SASH_COLOUR, MacStyle.COLORS['separator'])
        self.SetColour(aui.AUI_DOCKART_ACTIVE_CAPTION_COLOUR, MacStyle.COLORS['selection_bg'])
        self.SetColour(aui.AUI_DOCKART_ACTIVE_CAPTION_TEXT_COLOUR, wx.WHITE)
        self.SetColour(aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR, wx.Colour(230, 230, 230))
        self.SetColour(aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR, MacStyle.COLORS['text_color'])
        self.SetColour(aui.AUI_DOCKART_BORDER_COLOUR, MacStyle.COLORS['separator'])
        
        # 设置边框宽度和其他尺寸
        self.SetMetric(aui.AUI_DOCKART_PANE_BORDER_SIZE, 1)
        self.SetMetric(aui.AUI_DOCKART_SASH_SIZE, 2)  # 更窄的分隔线
        self.SetMetric(aui.AUI_DOCKART_CAPTION_SIZE, 24)  # 标准高度
        self.SetMetric(aui.AUI_DOCKART_GRADIENT_TYPE, aui.AUI_GRADIENT_NONE)  # 无渐变，扁平样式
        
        # 设置标题字体
        caption_font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(aui.AUI_DOCKART_CAPTION_FONT, caption_font)
