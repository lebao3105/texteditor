# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.0.0-0-g0efcecf)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext

###########################################################################
## Class AboutDialog
###########################################################################

class AboutDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 600,600 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP|wx.SYSTEM_MENU )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_listbook1 = wx.Listbook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LB_DEFAULT )
		self.m_panel1 = wx.Panel( self.m_listbook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.progName = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Name here", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.progName.Wrap( -1 )

		bSizer3.Add( self.progName, 1, wx.ALL|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )

		self.m_bitmap1 = wx.StaticBitmap( self.m_panel1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_bitmap1, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )


		bSizer2.Add( bSizer3, 0, wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Project version", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer4.Add( self.m_staticText3, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.version = wx.StaticText( self.m_panel1, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.version.Wrap( -1 )

		bSizer4.Add( self.version, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText5 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Home page", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer10.Add( self.m_staticText5, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.progURL = wx.StaticText( self.m_panel1, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.progURL.Wrap( -1 )

		bSizer10.Add( self.progURL, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer2.Add( bSizer10, 0, wx.EXPAND, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.descriptionbox = wx.CollapsiblePane( self.m_panel1, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
		self.descriptionbox.Collapse( False )

		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		self.description = wx.StaticText( self.descriptionbox.GetPane(), wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.description.Wrap( 1 )

		bSizer14.Add( self.description, 1, wx.ALL|wx.EXPAND, 5 )


		self.descriptionbox.GetPane().SetSizer( bSizer14 )
		self.descriptionbox.GetPane().Layout()
		bSizer14.Fit( self.descriptionbox.GetPane() )
		bSizer11.Add( self.descriptionbox, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )


		bSizer2.Add( bSizer11, 1, wx.EXPAND, 5 )


		self.m_panel1.SetSizer( bSizer2 )
		self.m_panel1.Layout()
		bSizer2.Fit( self.m_panel1 )
		self.m_listbook1.AddPage( self.m_panel1, u"About", True )
		self.m_panel2 = wx.Panel( self.m_listbook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText4 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"This program is made possible thanks to:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer5.Add( self.m_staticText4, 0, wx.ALL, 5 )

		self.developers = wx.CollapsiblePane( self.m_panel2, wx.ID_ANY, u"Developers", wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
		self.developers.Collapse( False )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		self.m_richText1 = wx.richtext.RichTextCtrl( self.developers.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_AUTO_URL|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer6.Add( self.m_richText1, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )


		self.developers.GetPane().SetSizer( bSizer6 )
		self.developers.GetPane().Layout()
		bSizer6.Fit( self.developers.GetPane() )
		bSizer5.Add( self.developers, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )

		self.artists = wx.CollapsiblePane( self.m_panel2, wx.ID_ANY, u"Artists", wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
		self.artists.Collapse( False )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_richText2 = wx.richtext.RichTextCtrl( self.artists.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_AUTO_URL|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer8.Add( self.m_richText2, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )


		self.artists.GetPane().SetSizer( bSizer8 )
		self.artists.GetPane().Layout()
		bSizer8.Fit( self.artists.GetPane() )
		bSizer5.Add( self.artists, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )

		self.docwriters = wx.CollapsiblePane( self.m_panel2, wx.ID_ANY, u"Documentation writers", wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
		self.docwriters.Collapse( False )

		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		self.document_writers = wx.richtext.RichTextCtrl( self.docwriters.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_AUTO_URL|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer9.Add( self.document_writers, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )


		self.docwriters.GetPane().SetSizer( bSizer9 )
		self.docwriters.GetPane().Layout()
		bSizer9.Fit( self.docwriters.GetPane() )
		bSizer5.Add( self.docwriters, 1, wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )


		self.m_panel2.SetSizer( bSizer5 )
		self.m_panel2.Layout()
		bSizer5.Fit( self.m_panel2 )
		self.m_listbook1.AddPage( self.m_panel2, u"Developers", False )
		self.m_panel3 = wx.Panel( self.m_listbook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer121 = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrl1 = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer121.Add( self.m_textCtrl1, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panel3.SetSizer( bSizer121 )
		self.m_panel3.Layout()
		bSizer121.Fit( self.m_panel3 )
		self.m_listbook1.AddPage( self.m_panel3, u"License", False )

		bSizer1.Add( self.m_listbook1, 1, wx.EXPAND |wx.ALL, 5 )

		m_sdbSizer1 = wx.StdDialogButtonSizer()
		self.m_sdbSizer1OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
		m_sdbSizer1.Realize();

		bSizer1.Add( m_sdbSizer1, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


