import wx

from wx.lib.agw.aui.dockart import AuiDefaultDockArt
from wx.lib.agw.aui.tabart import AuiDefaultTabArt, ChromeTabArt
from wx.lib.agw.aui.aui_utilities import GetBaseColour
from wx.lib.agw.aui.aui_constants import *

from ..generic import clrCall
from textworker import assets
from libtextworker.interface import manager

class AuiFlatDockArt(AuiDefaultDockArt):

    def __init__(this):
        AuiDefaultDockArt.__init__(this)

        bg, fg = clrCall.GetColor()
        bg = wx.Colour(*manager.hextorgb(bg))
        fg = wx.Colour(*manager.hextorgb(fg))

        # Window caption
        ## Active
        this._active_caption_gradient_colour = bg
        this._active_caption_colour = bg
        this._active_caption_text_colour = fg

        ## Text
        this._caption_font = clrCall.GetFont()
        this._caption_font.SetWeight(wx.FONTWEIGHT_BOLD)

        ## Inactive
        this._inactive_caption_colour = bg
        this._inactive_caption_gradient_colour = bg
        this._inactive_caption_text_colour = fg

        ## Bitmaps
        this._inactive_close_bitmap = assets.close.GetBitmap()
        this._inactive_minimize_bitmap = assets.minimize.GetBitmap()
        this._inactive_pin_bitmap = assets.pin.GetBitmap()

        this._active_close_bitmap = assets.close_white.GetBitmap()

        # Background
        this._background_colour = bg
        this._background_gradient_colour = bg


class AuiFlatTabArt(ChromeTabArt):

    def __init__(this):
        ChromeTabArt.__init__(this)

        newfont = clrCall.GetFont()
        newfont.SetWeight(wx.FONTWEIGHT_NORMAL)
        this._normal_font = this._selected_font = this._measuring_font = newfont

        closeBmp = closeHBmp = closePBmp = assets.close.GetBitmap()
        this.SetCustomButton(AUI_BUTTON_CLOSE, AUI_BUTTON_STATE_NORMAL, closeBmp)
        this.SetCustomButton(AUI_BUTTON_CLOSE, AUI_BUTTON_STATE_HOVER, closeHBmp)
        this.SetCustomButton(AUI_BUTTON_CLOSE, AUI_BUTTON_STATE_PRESSED, closePBmp)


    def SetDefaultColours(this, base_colour=None):

        bg, fg = clrCall.GetColor()
        bg = wx.Colour(*manager.hextorgb(bg))
        fg = wx.Colour(*manager.hextorgb(fg))
        this.SetBaseColour(bg)

        this._border_colour = wx.WHITE
        this._border_pen = wx.Pen(this._border_colour)

        this._background_top_colour = bg
        this._background_bottom_colour = bg

        this._tab_bottom_colour = this._tab_gradient_highlight_colour = wx.WHITE
        this._tab_text_colour = lambda page: fg

        this._tab_inactive_top_colour = this._tab_inactive_bottom_colour = bg


    def GetTabSize(this, dc: wx.DC, wnd: wx.Window, caption: str, bitmap: wx.Bitmap, active: bool, close_button_state:int, control: wx.Window):
        tabsize, xextent = ChromeTabArt.GetTabSize(this, dc, wnd, caption, bitmap, active, close_button_state, control)
        
        tab_width, tab_height = tabsize

        if AUI_NB_TAB_FIXED_WIDTH & this.GetAGWFlags():
            tab_width = 150
        else:
            tab_width += 15

        return (tab_width, tab_height), xextent
