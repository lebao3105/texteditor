import wx
import wx.xrc
import wx.richtext
import wx.lib.agw.labelbook as LB

import webbrowser

from textworker import DEVS, ARTISTS, DOCWRITERS, LICENSE, icons
from textworker import HOMEPAGE, _, ICON
from textworker import branch, __version__
from textworker.generic import clrCall

class AboutDialog(wx.Dialog):

	def __init__(this, parent):
		wx.Dialog.__init__(this, parent, size=(600, 600), title=_("About this application"))

		mainsz = wx.BoxSizer(wx.VERTICAL)
		this.book = LB.LabelBook(this, agwStyle=LB.INB_SHOW_ONLY_TEXT | LB.INB_DRAW_SHADOW
			   						| LB.INB_BOLD_TAB_SELECTION | LB.INB_LEFT)
		
		this.m_panel1 = wx.Panel( this.book )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer3.Add(wx.StaticText(this.m_panel1, label=f"TextWorker {branch.capitalize()}", style=wx.ALIGN_LEFT), 1, wx.ALL, 5 )

		this.m_bitmap1 = wx.StaticBitmap(this.m_panel1)
		this.m_bitmap1.SetIcon(wx.Icon(wx.Bitmap(icons.icon.GetImage().Scale(32, 32))))
		this.m_bitmap1.SetToolTip(_("Click to view in full size"))
	
		def fullImage(evt):
			new = wx.Dialog(this, title="Textworker icon")
			ico = wx.StaticBitmap(new)
			ico.SetIcon(ICON)
			new.ShowModal()

		this.m_bitmap1.Bind(wx.EVT_LEFT_DOWN, fullImage)
		bSizer3.Add( this.m_bitmap1, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer2.Add( bSizer3, 0, wx.EXPAND, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		this.m_staticText3 = wx.StaticText( this.m_panel1, label=_("Project version"))

		bSizer4.Add( this.m_staticText3, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		this.version = wx.StaticText( this.m_panel1, label=__version__)

		bSizer4.Add( this.version, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		this.m_staticText5 = wx.StaticText( this.m_panel1, label=_("Home page"))

		bSizer10.Add( this.m_staticText5, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		this.progURL = wx.StaticText( this.m_panel1, label=HOMEPAGE)
		this.progURL.SetToolTip(_("Click to open"))
		this.progURL.Bind(wx.EVT_LEFT_DOWN, lambda evt: webbrowser.open(HOMEPAGE))

		bSizer10.Add( this.progURL, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer2.Add( bSizer10, 0, wx.EXPAND, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		this.descriptionbox = wx.CollapsiblePane( this.m_panel1, label=_("Description"), style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
		this.descriptionbox.Collapse( False )

		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		this.description = wx.StaticText(
			this.descriptionbox.GetPane(),
			label=
				_("A simple and small text editor.\n"
            	  "Textworker allows its users to write many things they want, "
              	  "with gradually added new and cool features.\n"
              	  "Free and open source!")
		)

		bSizer14.Add( this.description, 1, wx.ALL|wx.EXPAND, 5 )


		this.descriptionbox.GetPane().SetSizer( bSizer14 )
		this.descriptionbox.GetPane().Layout()
		bSizer14.Fit( this.descriptionbox.GetPane() )
		bSizer11.Add( this.descriptionbox, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer2.Add( bSizer11, 1, wx.EXPAND, 5 )


		this.m_panel1.SetSizer( bSizer2 )
		this.m_panel1.Layout()
		bSizer2.Fit( this.m_panel1 )
		this.book.AddPage( this.m_panel1, _("About"), True )
		this.m_panel2 = wx.Panel( this.book, style=wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		this.m_staticText4 = wx.StaticText( this.m_panel2, label=_("This program is made possible thanks to:"))

		bSizer5.Add( this.m_staticText4, 0, wx.ALL, 5 )

		this.developers = wx.CollapsiblePane( this.m_panel2, label=_("Developers"), style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
		this.developers.Collapse( False )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		this.m_richText1 = wx.richtext.RichTextCtrl( this.developers.GetPane(), style=wx.TE_AUTO_URL|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer6.Add( this.m_richText1, 1, wx.ALL|wx.EXPAND, 5 )


		this.developers.GetPane().SetSizer( bSizer6 )
		this.developers.GetPane().Layout()
		bSizer6.Fit( this.developers.GetPane() )
		bSizer5.Add( this.developers, 1, wx.ALL|wx.EXPAND, 5 )

		this.artists = wx.CollapsiblePane( this.m_panel2, label=_("Artists"), style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
		this.artists.Collapse( False )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		this.m_richText2 = wx.richtext.RichTextCtrl( this.artists.GetPane(), style=wx.TE_AUTO_URL|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer8.Add( this.m_richText2, 1, wx.ALL|wx.EXPAND, 5 )


		this.artists.GetPane().SetSizer( bSizer8 )
		this.artists.GetPane().Layout()
		bSizer8.Fit( this.artists.GetPane() )
		bSizer5.Add( this.artists, 1, wx.ALL|wx.EXPAND, 5 )

		this.docwriters = wx.CollapsiblePane( this.m_panel2, label=_("Documentation writers"), style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
		this.docwriters.Collapse( False )

		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		this.document_writers = wx.richtext.RichTextCtrl( this.docwriters.GetPane(), style=wx.TE_AUTO_URL|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer9.Add( this.document_writers, 1, wx.ALL|wx.EXPAND, 5 )


		this.docwriters.GetPane().SetSizer( bSizer9 )
		this.docwriters.GetPane().Layout()
		bSizer9.Fit( this.docwriters.GetPane() )
		bSizer5.Add( this.docwriters, 1, wx.ALL|wx.EXPAND, 5 )


		this.m_panel2.SetSizer( bSizer5 )
		this.m_panel2.Layout()
		bSizer5.Fit( this.m_panel2 )
		this.book.AddPage( this.m_panel2, _("Developers"), False )
		this.m_panel3 = wx.Panel( this.book, style=wx.TAB_TRAVERSAL )
		bSizer121 = wx.BoxSizer( wx.VERTICAL )

		def writeCredits(dicti, target):
			for name in dicti:
				target.WriteText(name + " ")
				if dicti[name]:
					target.BeginBold()
					target.BeginURL(dicti[name])
					target.WriteText(f"<{dicti[name]}>")
					target.EndURL()
					target.EndBold()
				target.Newline()
			target.SetInsertionPoint(0)
			target.SetEditable(False)

		for dicti, target, parent in [(DEVS, this.m_richText1, this.developers),
									  (ARTISTS, this.m_richText2, this.artists),
									  (DOCWRITERS, this.document_writers, this.docwriters)]:
			writeCredits(dicti, target)
			parent.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, lambda evt: parent.Layout())

		this.m_textCtrl1 = wx.TextCtrl( this.m_panel3, value=open(LICENSE, "r").read(), style=wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY )
		this.m_textCtrl1.SetInsertionPoint(0)
		bSizer121.Add( this.m_textCtrl1, 1, wx.ALL|wx.EXPAND, 5 )


		this.m_panel3.SetSizer( bSizer121 )
		this.m_panel3.Layout()
		bSizer121.Fit( this.m_panel3 )
		this.book.AddPage( this.m_panel3, _("License"), False )

		mainsz.Add( this.book, 1, wx.EXPAND |wx.ALL, 5 )

		m_sdbSizer1 = wx.StdDialogButtonSizer()
		this.m_sdbSizer1OK = wx.Button( this, wx.ID_OK )
		m_sdbSizer1.AddButton( this.m_sdbSizer1OK )
		m_sdbSizer1.Realize()

		mainsz.Add( m_sdbSizer1, 0, wx.EXPAND, 5 )

		this.Bind(wx.EVT_TEXT_URL, lambda evt: webbrowser.open(evt.GetString()))
		this.SetSizer( mainsz )
		this.Layout()

		this.Centre( wx.BOTH )

		clrCall.configure(this)
		clrCall.autocolor_run(this)
