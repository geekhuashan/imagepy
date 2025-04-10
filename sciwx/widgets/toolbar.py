import wx
import platform
from .paradialog import ParaDialog

def make_logo(obj):
    bmp = None
    if isinstance(obj, str) and len(obj)>1:
        bmp = wx.Bitmap(obj)
    if isinstance(obj, str) and len(obj)==1:
        bmp = wx.Bitmap(16, 16)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush((255,255,255)))
        dc.Clear()
        dc.SetTextForeground((0,0,150))
        font = dc.GetFont()
        font.SetPointSize(12)
        dc.SetFont(font)
        w, h = dc.GetTextExtent(obj)
        dc.DrawText(obj, 8-w//2, 8-h//2)
        rgb = bytes(768)
        dc.SelectObject(wx.NullBitmap)
        bmp.CopyToBuffer(rgb)
        a = memoryview(rgb[::3]).tolist()
        a = bytes([255-i for i in a])
        bmp = wx.Bitmap.FromBufferAndAlpha(16, 16, rgb, a)
    # img = bmp.ConvertToImage()
    # img.Resize((20,20), (2,2))
    # return img.ConvertToBitmap()
    return bmp

class ToolBar(wx.Panel):
    def __init__(self, parent, vertical=False):
        wx.Panel.__init__( self, parent, wx.ID_ANY,  wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizer = wx.BoxSizer( (wx.HORIZONTAL, wx.VERTICAL)[vertical] )
        self.SetSizer( sizer )
        self.app = parent
        self.toolset = []
        self.curbtn = None

    def on_tool(self, evt, tol):
        tol.start(self.app)
        # evt.Skip()
        btn = evt.GetEventObject()
        
        # 重置之前选中的按钮
        if not self.curbtn is None:
            self.curbtn.SetBackgroundColour(self.GetBackgroundColour())
            if hasattr(self.curbtn, 'selected'):
                self.curbtn.selected = False
            self.curbtn.Refresh()
            
        # 设置当前按钮为选中状态
        self.curbtn = btn
        
        # 为 Mac 系统提供更明显的选中状态
        if platform.system() == 'Darwin':
            # 使用更适合 Mac 的灰色高亮
            btn.SetBackgroundColour(wx.Colour(225, 225, 225))
            btn.selected = True
        else:
            # 其他系统使用默认的高亮颜色
            btn.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
            
        btn.Refresh()

    def on_config(self, evt, tol):
        if not hasattr(tol, 'view'): return
        self.app.show_para(tol.title, tol.para, tol.view)
        tol.config()

    def on_help(self, evt, tol): pass

    def on_info(self, event, tol): 
        self.app.info(tol.title)

    def bind(self, btn, tol):
        obj = tol()
        btn.SetBackgroundColour(self.GetBackgroundColour())
        btn.selected = False  # 添加选中状态标记
        
        # 添加自定义绘制以显示选中状态
        if platform.system() == 'Darwin':
            # 为 Mac 添加自定义绘制
            def on_paint(evt, b=btn):
                dc = wx.PaintDC(b)
                width, height = b.GetSize()
                if hasattr(b, 'selected') and b.selected:
                    # 画一个灰色边框表示选中状态 - 保证是矩形
                    dc.SetPen(wx.Pen(wx.Colour(120, 120, 120), 1))
                    dc.SetBrush(wx.TRANSPARENT_BRUSH)
                    dc.DrawRectangle(0, 0, width, height)
                evt.Skip()
            btn.Bind(wx.EVT_PAINT, on_paint)
        
        btn.Bind(wx.EVT_LEFT_DOWN, lambda e, obj=obj: self.on_tool(e, obj))
        btn.Bind(wx.EVT_RIGHT_DOWN, lambda e, obj=obj: self.on_help(e, obj))
        btn.Bind(wx.EVT_ENTER_WINDOW, lambda e, obj=obj: self.on_info(e, obj))
        #if not isinstance(data[0], Macros) and issubclass(data[0], Tool):
        btn.Bind(wx.EVT_LEFT_DCLICK, lambda e, obj=obj: self.on_config(e, obj))

    def clear(self):
        del self.toolset[:]
        self.GetSizer().Clear()
        self.DestroyChildren()

    def add_tool(self, logo, tool):
        btn = wx.BitmapButton(self, wx.ID_ANY, make_logo(logo), 
            wx.DefaultPosition, (32,32), wx.BU_AUTODRAW|wx.BORDER_NONE )
        self.bind(btn, tool)
        # 移除按钮间的空隙
        self.GetSizer().Add(btn, 0, wx.ALL, 0)

    def add_tools(self, name, tools, fixed=True):
        if not fixed: self.toolset.append((name, []))
        for logo, tool in tools:
            btn = wx.BitmapButton(self, wx.ID_ANY, make_logo(logo), 
                wx.DefaultPosition, (32,32), wx.BU_AUTODRAW|wx.BORDER_NONE )
            self.bind(btn, tool)
            # 移除按钮间的空隙
            self.GetSizer().Add(btn, 0, wx.ALL, 0)
            if not fixed: self.toolset[-1][1].append(btn)
        if fixed:
            line = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
            # 调整分隔线间距
            self.GetSizer().Add( line, 0, wx.ALL|wx.EXPAND, 0 )

    def active_set(self, name):
        for n, tools in self.toolset:
            for btn in tools:
                if n==name: btn.Show()
                if n!=name: btn.Hide()
        self.Layout()
        
    def add_pop(self, logo, default):
        self.GetSizer().AddStretchSpacer(1)
        btn = wx.BitmapButton(self, wx.ID_ANY, make_logo(logo), 
                wx.DefaultPosition, (32,32), wx.BU_AUTODRAW|wx.BORDER_NONE )
        btn.Bind(wx.EVT_LEFT_DOWN, self.menu_drop)
        btn.SetBackgroundColour(self.GetBackgroundColour())
        # 移除按钮间的空隙
        self.GetSizer().Add(btn, 0, wx.ALL, 0)
        self.active_set(default)

    def menu_drop(self, event):
        menu = wx.Menu()
        for name, item in self.toolset:
            item = wx.MenuItem(menu, wx.ID_ANY, name, wx.EmptyString, wx.ITEM_NORMAL )
            menu.Append(item)
            f = lambda e, name=name:self.active_set(name)
            menu.Bind(wx.EVT_MENU, f, id=item.GetId())
        self.PopupMenu( menu )
        menu.Destroy()
        
if __name__ == '__main__':
    path = 'C:/Users/54631/Documents/projects/imagepy/imagepy/tools/drop.gif'
    app = wx.App()
    frame = wx.Frame(None)
    tool = ToolBar(frame, vertical=True)
    path = 'C:/Users/54631/Documents/projects/imagepy2/fucai/imgs/_help.png'
    tool.add_tools('A', [('A', None)] * 3)
    tool.add_tools('B', [('B', None)] * 3)
    tool.add_tools('C', [('C', None)] * 3)
    tool.add_pop('P', 'B')
    tool.Layout()
    frame.Fit()
    frame.Show()
    app.MainLoop()
