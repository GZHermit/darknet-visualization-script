import wx
import os

from .. import main_gui

class UnifyScript(wx.Frame):
    """ We simply derive a new class of Frame. """

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1024, 768))
        # self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        self.createMenuBar()
        self.createStatusBar()
        self.createPanel()
        # Setting up the menu.
        self.Show(True)

    def createMenuBar(self):
        filemenu = wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        aboutItem = filemenu.Append(wx.ID_ABOUT, "About", " Information about this program")
        exitItem = filemenu.Append(wx.ID_EXIT, "Exit", " Terminate the program")
        openItem = filemenu.Append(wx.ID_OPEN, 'Open', "Open the files...")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "File")  # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnOpen, openItem)

    def createPanel(self):
        self.panel = wx.Panel(self)

        wx.StaticText(self.panel, label='CfgFilePath:', pos=(100, 60), size=(100, 100))
        self.cfgText = wx.StaticText(self.panel, label='', pos=(320, 60))
        cfgButton = wx.Button(self.panel, label='cfgFile', pos=(200, 60), size=(100, 30))

        wx.StaticText(self.panel, label='DataFilePath:', pos=(100, 120), size=(100, 100))
        self.dataText = wx.StaticText(self.panel, label='', pos=(320, 120))
        dataButton = wx.Button(self.panel, label='dataFile', pos=(200, 120), size=(100, 30))

        startButton = wx.Button(self.panel, label='start', pos=(840, 680), size=(100, 30))

        gpus = ['0', '1', '2']
        wx.StaticText(self.panel, label="Gpus:", pos=(100, 180), size=(100, 100))
        gpuComboBox = wx.ComboBox(self.panel, value='choose...', pos=(200, 180), choices=gpus, style=wx.CB_SIMPLE)

        orders = ['train', 'valid', 'draw', 'compute']
        wx.StaticText(self.panel, label="Orders:", pos=(100, 240), size=(100, 100))
        orderComboBox = wx.ComboBox(self.panel, value='choose...', pos=(200, 240), choices=orders, style=wx.CB_SIMPLE)

        self.Bind(wx.EVT_BUTTON, self.OnChooseCfg, cfgButton)
        self.Bind(wx.EVT_BUTTON, self.OnChooseData, dataButton)
        self.Bind(wx.EVT_BUTTON, self.OnStart, startButton)
        self.Bind(wx.EVT_COMBOBOX, self.OnGPUSelect, gpuComboBox)
        self.Bind(wx.EVT_COMBOBOX, self.OnOrderSelect, orderComboBox)

    def createStatusBar(self):
        self.CreateStatusBar()

    def OnChooseCfg(self, e):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose CFG file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            cfg_fp = os.path.join(self.dirname, self.filename)
        dlg.Destroy()
        self.cfgText.SetLabelText(cfg_fp)
        main_gui.set_cfg_fp(cfg_fp)

    def OnChooseData(self, e):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose Data file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            data_fp = os.path.join(self.dirname, self.filename)
        dlg.Destroy()
        self.dataText.SetLabelText(data_fp)
        main_gui.set_data_fp(data_fp)

    def OnChooseWeight(self):
        self.dirname = '~'
        dlg = wx.FileDialog(self, "Choose Weight file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            weight_fp = os.path.join(self.dirname, self.filename)
        dlg.Destroy()
        self.weightText.SetLabelText(weight_fp)
        main_gui.set_weight_fp(weight_fp)

    def OnGPUSelect(self, e):
        gpuIndex = e.GetSelection()
        main_gui.set_gpus(str(gpuIndex))

    def OnDrawOptionSelect(self, e):
        print("OnDrawOptionSelect!!!!")
        draw_options = ['mAP', 'loss', 'box']
        drawOptionIndex = e.GetSelection()
        main_gui.set_draw_option(draw_options[drawOptionIndex])

    def OnOrderSelect(self, e):
        orders = ['train', 'valid', 'draw', 'compute']
        index = e.GetSelection()
        if orders[index] == 'train':
            wx.StaticText(self.panel, label='WeightFilePath:', pos=(100, 300), size=(120, 100))
            self.weightText = wx.StaticText(self.panel, label='', pos=(220, 300))
            self.OnChooseWeight()

        elif orders[index] == 'valid':
            main_gui.set_draw_option('mAP')
            wx.StaticText(self.panel, label='ValidStep:', pos=(100, 300), size=(120, 100))
            self.validstepText = wx.StaticText(self.panel, label='All of them', pos=(200, 300))
            dlg = wx.TextEntryDialog(self, 'Enter The Valid Step List', 'Text Entry Dialog')
            if dlg.ShowModal() == wx.ID_OK:
                valid_step = dlg.GetValue().strip('\n').split(',')
                self.validstepText.SetLabelText(dlg.GetValue())
            else:
                valid_step = None
            dlg.Destroy()
            main_gui.set_valid_step(valid_step)

        elif orders[index] == 'compute':
            main_gui.set_draw_option('mAP')
            wx.StaticText(self.panel, label='ComputeStep:', pos=(100, 300), size=(120, 100))
            self.computestepText = wx.StaticText(self.panel, label='All of them', pos=(200, 300))
            dlg = wx.TextEntryDialog(self, 'Enter The Compute Step List', 'Text Entry Dialog')
            if dlg.ShowModal() == wx.ID_OK:
                compute_step = dlg.GetValue().strip('\n').split(',')
                self.computestepText.SetLabelText(dlg.GetValue())
            else:
                compute_step = None
            dlg.Destroy()
            main_gui.set_compute_step(compute_step)

        elif orders[index] == 'draw':
            draw_options = ['mAP', 'loss', 'box']
            wx.StaticText(self.panel, label='DrawOption:', pos=(100, 300), size=(120, 100))
            dopsComboBox = wx.ComboBox(self.panel, value='choose...', pos=(200, 300), choices=draw_options,
                                       style=wx.CB_SIMPLE)
            self.Bind(wx.EVT_COMBOBOX, self.OnDrawOptionSelect, dopsComboBox)

        main_gui.set_order(orders[index])

    def OnStart(self, e):
        main_gui.start()

    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "A small text editor", "About Sample Editor", wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

    def OnOpen(self, e):
        self.dirname = '~'
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()

    def OnClear(self, e):
        pass

    def OnExit(self, e):
        self.Close(True)


def startApp():
    app = wx.App(False)
    frame = UnifyScript(None, '33\'s UnifyScripts')
    app.MainLoop()


if __name__ == '__main__':
    startApp()
