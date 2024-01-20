import webbrowser
from . import about
from textworker import DEVS, ARTISTS, DOCWRITERS, LICENSE
from textworker import HOMEPAGE, _, ICON
from textworker import branch, __version__, icon
from wx import EVT_LEFT_DOWN, EVT_TEXT_URL, Icon, Bitmap, Dialog, StaticBitmap
from wx import EVT_COLLAPSIBLEPANE_CHANGED

class AboutDialog(about.AboutDialog):

    def Customize(this):
        """
        Add contents to the dialog.
        """

        this.SetTitle(_("About this application"))
        this.progName.SetLabel("Textworker") # Project name

        # Project icon
        this.m_bitmap1.SetIcon(Icon(Bitmap(getattr(icon, branch).GetImage().Scale(32, 32))))
        this.m_bitmap1.SetToolTip(_("Click to view in full size"))
        
        def fullImage(evt):
            new = Dialog(this, title=_("Textworker icon"))
            ico = StaticBitmap(new)
            ico.SetIcon(ICON)
            new.ShowModal()

        this.m_bitmap1.Bind(EVT_LEFT_DOWN, fullImage)

        this.version.SetLabel(__version__) # Project version
        
        # Project home page
        this.progURL.SetLabel(HOMEPAGE)
        this.progURL.SetToolTip(_("Click to open"))
        this.progURL.Bind(EVT_LEFT_DOWN, lambda evt: webbrowser.open(HOMEPAGE))
        this.description.SetLabel(
            _("A simple and small text editor.\n"
              "Textworker allows its users to write many things they want, "
              "with gradually added new and cool features.\n"
              "Free and open source!")
        )

        # Credits page
        def writeCredits(dicti, target):
            for name in dicti:
                target.WriteText(name)
                if dicti[name]:
                    target.BeginBold()
                    target.BeginURL(dicti[name])
                    target.WriteText(f"<{dicti[name]}>")
                    target.EndURL()
                    target.EndBold()
                target.Newline()
            target.SetInsertionPoint(0)
            target.SetEditable(false)

        for dicti, target, parent in [(DEVS, this.m_richText1, this.developers),
                              (ARTISTS, this.m_richText2, this.artists),
                              (DOCWRITERS, this.document_writers, this.docwriters)]:
            writeCredits(dicti, target)
            parent.Bind(EVT_COLLAPSIBLEPANE_CHANGED, lambda evt: parent.Layout())
        
        this.m_textCtrl1.AppendText(open(LICENSE, "r").read())
        this.m_textCtrl1.SetInsertionPoint(0)

        this.Bind(EVT_TEXT_URL, lambda evt: webbrowser.open(evt.GetString()))