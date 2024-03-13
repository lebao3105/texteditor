import wx
import wx.xrc
import wx.richtext
import wx.lib.agw.labelbook as LB

class AboutDialog(wx.Dialog):
	horizontalSzFlags = wx.ALL | wx.EXPAND

	def __init__(this, parent):
		wx.Dialog.__init__(this, parent, size=(600, 600))

		mainsz = wx.BoxSizer(wx.VERTICAL)
		this.book = LB.LabelBook(this, agwStyle=LB.INB_SHOW_ONLY_TEXT | LB.INB_DRAW_SHADOW
			   						| LB.INB_BOLD_TAB_SELECTION | LB.INB_LEFT)
		
		this.m_panel1 = wx.Panel( this.book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		this.progName = wx.StaticText( this.m_panel1, wx.ID_ANY, u"Name here", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		this.progName.Wrap( -1 )

		bSizer3.Add( this.progName, 1, wx.ALL|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )

		this.m_bitmap1 = wx.StaticBitmap( this.m_panel1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( this.m_bitmap1, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )


		bSizer2.Add( bSizer3, 0, wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		this.m_staticText3 = wx.StaticText( this.m_panel1, wx.ID_ANY, u"Project version", wx.DefaultPosition, wx.DefaultSize, 0 )
		this.m_staticText3.Wrap( -1 )

		bSizer4.Add( this.m_staticText3, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		this.version = wx.StaticText( this.m_panel1, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		this.version.Wrap( -1 )

		bSizer4.Add( this.version, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		this.m_staticText5 = wx.StaticText( this.m_panel1, wx.ID_ANY, u"Home page", wx.DefaultPosition, wx.DefaultSize, 0 )
		this.m_staticText5.Wrap( -1 )

		bSizer10.Add( this.m_staticText5, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		this.progURL = wx.StaticText( this.m_panel1, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		this.progURL.Wrap( -1 )

		bSizer10.Add( this.progURL, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer2.Add( bSizer10, 0, wx.EXPAND, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		this.descriptionbox = wx.CollapsiblePane( this.m_panel1, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
		this.descriptionbox.Collapse( False )

		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		this.description = wx.StaticText( this.descriptionbox.GetPane(), wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		this.description.Wrap( 1 )

		bSizer14.Add( this.description, 1, wx.ALL|wx.EXPAND, 5 )


		this.descriptionbox.GetPane().SetSizer( bSizer14 )
		this.descriptionbox.GetPane().Layout()
		bSizer14.Fit( this.descriptionbox.GetPane() )
		bSizer11.Add( this.descriptionbox, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )


		bSizer2.Add( bSizer11, 1, wx.EXPAND, 5 )


		this.m_panel1.SetSizer( bSizer2 )
		this.m_panel1.Layout()
		bSizer2.Fit( this.m_panel1 )
		this.book.AddPage( this.m_panel1, u"About", True )
		this.m_panel2 = wx.Panel( this.book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		this.m_staticText4 = wx.StaticText( this.m_panel2, wx.ID_ANY, u"This program is made possible thanks to:", wx.DefaultPosition, wx.DefaultSize, 0 )
		this.m_staticText4.Wrap( -1 )

		bSizer5.Add( this.m_staticText4, 0, wx.ALL, 5 )

		this.developers = wx.CollapsiblePane( this.m_panel2, wx.ID_ANY, u"Developers", wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
		this.developers.Collapse( False )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		this.m_richText1 = wx.richtext.RichTextCtrl( this.developers.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_AUTO_URL|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer6.Add( this.m_richText1, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )


		this.developers.GetPane().SetSizer( bSizer6 )
		this.developers.GetPane().Layout()
		bSizer6.Fit( this.developers.GetPane() )
		bSizer5.Add( this.developers, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )

		this.artists = wx.CollapsiblePane( this.m_panel2, wx.ID_ANY, u"Artists", wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
		this.artists.Collapse( False )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		this.m_richText2 = wx.richtext.RichTextCtrl( this.artists.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_AUTO_URL|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer8.Add( this.m_richText2, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )


		this.artists.GetPane().SetSizer( bSizer8 )
		this.artists.GetPane().Layout()
		bSizer8.Fit( this.artists.GetPane() )
		bSizer5.Add( this.artists, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )

		this.docwriters = wx.CollapsiblePane( this.m_panel2, wx.ID_ANY, u"Documentation writers", wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
		this.docwriters.Collapse( False )

		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		this.document_writers = wx.richtext.RichTextCtrl( this.docwriters.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_AUTO_URL|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer9.Add( this.document_writers, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )


		this.docwriters.GetPane().SetSizer( bSizer9 )
		this.docwriters.GetPane().Layout()
		bSizer9.Fit( this.docwriters.GetPane() )
		bSizer5.Add( this.docwriters, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )


		this.m_panel2.SetSizer( bSizer5 )
		this.m_panel2.Layout()
		bSizer5.Fit( this.m_panel2 )
		this.book.AddPage( this.m_panel2, u"Developers", False )
		this.m_panel3 = wx.Panel( this.book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer121 = wx.BoxSizer( wx.VERTICAL )

		this.m_textCtrl1 = wx.TextCtrl( this.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer121.Add( this.m_textCtrl1, 1, wx.ALL|wx.EXPAND, 5 )


		this.m_panel3.SetSizer( bSizer121 )
		this.m_panel3.Layout()
		bSizer121.Fit( this.m_panel3 )
		this.book.AddPage( this.m_panel3, u"License", False )

		mainsz.Add( this.book, 1, wx.EXPAND |wx.ALL, 5 )

		m_sdbSizer1 = wx.StdDialogButtonSizer()
		this.m_sdbSizer1OK = wx.Button( this, wx.ID_OK )
		m_sdbSizer1.AddButton( this.m_sdbSizer1OK )
		m_sdbSizer1.Realize()

		mainsz.Add( m_sdbSizer1, 0, wx.EXPAND, 5 )


		this.SetSizer( mainsz )
		this.Layout()

		this.Centre( wx.BOTH )
