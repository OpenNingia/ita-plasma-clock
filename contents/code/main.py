#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Copyright Daniele Simonetti 2012
# Modded by Federico Rampazzo
# Modded by Dennis Kadioglu: 
#	- added german matrix and hours
#	- added minutes represented by 4 dots in the corners
#	- german text changes every 5 minutes
#	- default settings changed to german and black background
#	- changed color for normal pen to darker grey tone for better differentiation

from PyQt4.QtGui   import *
from PyQt4.QtCore  import *
from PyKDE4.plasma import Plasma
from PyKDE4        import plasmascript

import sys
import os

from datetime import datetime

APP_NAME    = 'PlasmaQlock'
APP_ORG     = 'openningia'
APP_VERSION = '1.0'

MATRIX = [\
    u"""\
SONORLEBORE
ÈRĹUNASDUEZ
TREOTTONOVE
DIECIUNDICI
DODICISETTE
QUATTROCSEI
CINQUESMENO
ECUNOQUARTO
VENTICINQUE
DIECIEMEZZA
    """,

    u"""\
ITLISASTIME
ACQUARTERDC
TWENTYFIVEX
HALFBTENFTO
PASTERUNINE
ONESIXTHREE
FOURFIVETWO
EIGHTELEVEN
SEVENTWELVE
TENSEOCLOCK
    """,
    
    u"""\
ESKISTAFÜNF
ZEHNZWANZIG
DREIVIERTEL
VORFUNKNACH
HALBAELFÜNF
EINSXÄMZWEI
DREIAUJVIER
SECHSNLACHT
SIEBENZWÖLF
ZEHNEUNKUHR
    """
]

HOURS = [
    [
    u"DODICI",
    u"UNA",
    u"DUE",
    u"TRE",
    u"QUATTRO",
    u"CINQUE",
    u"SEI",
    u"SETTE",
    u"OTTO",
    u"NOVE",
    u"DIECI",
    u"UNDICI"
    ],

    [
    u"TWELVE",
    u"ONE",
    u"TWO",
    u"THREE",
    u"FOUR",
    u"FIVE",
    u"SIX",
    u"SEVEN",
    u"EIGHT",
    u"NINE",
    u"TEN",
    u"ELEVEN"
    ],
    
    [
    u"ZWÖLF",
    u"EINS",
    u"ZWEI",
    u"DREI",
    u"VIER",
    u"FÜNF",
    u"SECHS",
    u"SIEBEN",
    u"ACHT",
    u"NEUN",
    u"ZEHN",
    u"ELF"
    ]
]

def gimme_time_it():
    toks  = []
    now   = datetime.now()

    tell_hour = now.hour
    if now.minute >= 35:
        tell_hour += 1

    tell_hour = tell_hour % 12

    if tell_hour == 1:
        toks.append(u'È ĹUNA')
    else:
        toks.append(u'SONO LE ORE {0}'.format(HOURS[0][tell_hour]))

    if now.minute >= 35:
        toks.append(u'MENO')
        if now.minute >= 55:
            toks.append(u'CINQUE')
        elif now.minute >= 50:
            toks.append(u'DIECI')
        elif now.minute >= 45:
            toks.append(u'UN QUARTO')
        elif now.minute >= 40:
            toks.append(u'VENTI')
        else:
            toks.append(u'VENTICINQUE')
    elif now.minute > 5:
        toks.append(u'E')
        if now.minute < 10:
            toks.append(u'CINQUE')
        elif now.minute < 15:
            toks.append(u'DIECI')
        elif now.minute < 20:
            toks.append(u'UN QUARTO')
        elif now.minute < 30:
            toks.append(u'VENTI')
        elif now.minute < 40:
            toks.append(u'MEZZA')

    return u' '.join(toks)

def gimme_time_en():
    toks  = []
    now   = datetime.now()

    tell_hour = now.hour
    if now.minute >= 40:
        tell_hour += 1

    tell_hour = tell_hour % 12

    if tell_hour == 1:
        toks.append(u'IT IS ONE OCLOCK')
    else:
        toks.append(u'IT IS ')
        if now.minute >= 40:
            if now.minute >= 55:
                toks.append(u'FIVE')
            elif now.minute >= 50:
                toks.append(u'TEN')
            elif now.minute >= 45:
                toks.append(u'A QUARTER')
            else:
                toks.append(u'TWENTY')
            toks.append(u' TO ')
        elif now.minute >= 5:
            if now.minute < 10:
                toks.append(u'FIVE')
            elif now.minute < 15:
                toks.append(u'TEN')
            elif now.minute < 20:
                toks.append(u'A QUARTER')
            elif now.minute < 30:
                toks.append(u'TWENTY')
            elif now.minute < 40:
                toks.append(u'HALF')
            toks.append(u' PAST ')
        toks.append(HOURS[1][tell_hour])
        if now.minute <= 5:
            toks.append(u' OCLOCK')
    return u' '.join(toks)
    
def gimme_time_de():
    toks  = []
    now   = datetime.now()

    tell_hour = now.hour
    if now.minute >= 25:
        tell_hour += 1

    tell_hour = tell_hour % 12

    if now.minute < 5:
        toks.append(u'ES IST')
        toks.append(HOURS[2][tell_hour])
        toks.append(u' UHR')
    else:
        toks.append(u'ES IST ')
        if now.minute < 30 and now.minute >= 25:
	  toks.append(u'FÜNF')
	  toks.append(u'VOR')
	  toks.append(u'HALB')
	elif now.minute >= 35 and now.minute < 40:
	  toks.append(u'FÜNF')
	  toks.append(u'NACH')
	  toks.append(u'HALB')
	elif now.minute >= 30 and now.minute < 35:
	  toks.append(u'HALB')
        elif now.minute >= 40:
            if now.minute >= 55:
                toks.append(u'FÜNF')
            elif now.minute >= 50:
                toks.append(u'ZEHN')
            elif now.minute >= 45:
                toks.append(u'VIERTEL')
            else:
                toks.append(u'ZWANZIG')
            toks.append(u' VOR ')
        elif now.minute >= 5:
            if now.minute < 10:
                toks.append(u'FÜNF')
            elif now.minute < 15:
                toks.append(u'ZEHN')
            elif now.minute < 20:
                toks.append(u'VIERTEL')
            elif now.minute < 25:
                toks.append(u'ZWANZIG')
            toks.append(u' NACH ')
        toks.append(HOURS[2][tell_hour])
    return u' '.join(toks)
    
def gimme_minute():
    now = datetime.now()
    return now.minute

FUNCS = [ gimme_time_it, gimme_time_en, gimme_time_de, gimme_minute ]

class PlasmaQlock(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

        self.to_render     = []
        self.old_to_render = []
        self.minute = 0
        self.old_minute = 0

        self.bg_color = QBrush(
                        QColor(0xA8, 0xD1, 0x1D, 200))
        self.normal_pen = QPen()
        self.normal_pen.setColor(QColor(0x29,0x29,0x29))
        self.highl_pen  = QPen()
        self.highl_pen.setColor(QColor(255,255,255))
        self.language = 2

    def init(self):
        self.setHasConfigurationInterface(True)
        self.setAspectRatioMode(Plasma.Square)

        # read configuration
        config = self.config()
        font_nm = config.readEntry('tx_font_nm', "Droid Sans").toString()
        font_sz = config.readEntry('tx_font_sz', 14).toInt()[0]
        self.tx_font = QFont(font_nm, font_sz)

        r = config.readEntry('bg_color_r', 0x00).toInt()[0]
        g = config.readEntry('bg_color_g', 0x00).toInt()[0]
        b = config.readEntry('bg_color_b', 0x00).toInt()[0]
        a = config.readEntry('bg_color_a', 200).toInt()[0]
        self.bg_color = QBrush(QColor(r, g, b, a))

        self.language = config.readEntry('language', 2).toInt()[0]

        self.update_clock()

        w = font_sz * 21 + 160
        h = font_sz * 17 + 160
        self.resize(w, h)

        # create timer
        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.connect(self.timer, SIGNAL("timeout()"), self.on_timeout)
        self.timer.start()

    def on_timeout(self):
        self.update_clock()
        if self.old_to_render != self.to_render or self.old_minute != self.minute:
            self.update()

    def update_clock(self):
        toks = FUNCS[self.language]().split()
        self.old_to_render = self.to_render
        self.to_render     = []
        self.old_minute = self.minute
        self.minute = FUNCS[3]() % 10
        idx = 0
        off = 0
        for t in toks:
            idx = MATRIX[self.language].find(t, off)
            if idx < 0:
                idx = 0
            for i in xrange(idx, idx+len(t)):
                self.to_render.append( i )
            off = idx + len(t) + 1

    def paintInterface(self, painter, option, rect):
        painter.save()

        # PENS
        painter.setPen(self.normal_pen)
        painter.fillRect(rect, self.bg_color)
        painter.setFont(self.tx_font)
        
        # DRAW THE MINUTES
        #self.minute = FUNCS[3]() % 10
        size = self.size()
        w = size.width()
        h = size.height()
        if self.minute == 0 or self.minute == 5:
	  painter.setPen(self.normal_pen)
	  painter.drawText(30, 40, u"•")
	  painter.drawText(w-40, 40, u"•")
	  painter.drawText(30, h-30, u"•")
	  painter.drawText(w-40, h-30, u"•")
	elif self.minute == 1 or self.minute == 6:
	  painter.setPen(self.highl_pen)
	  painter.drawText(30, 40, u"•")
	  painter.setPen(self.normal_pen)
	  painter.drawText(w-40, 40, u"•")
	  painter.drawText(30, h-30, u"•")
	  painter.drawText(w-40, h-30, u"•")
	elif self.minute == 2 or self.minute == 7:
	  painter.setPen(self.highl_pen)
	  painter.drawText(30, 40, u"•")
	  painter.drawText(w-40, 40, u"•")
	  painter.setPen(self.normal_pen)
	  painter.drawText(30, h-30, u"•")
	  painter.drawText(w-40, h-30, u"•")
	elif self.minute == 3 or self.minute == 8:
	  painter.setPen(self.highl_pen)
	  painter.drawText(30, 40, u"•")
	  painter.drawText(w-40, 40, u"•")
	  painter.drawText(30, h-30, u"•")
	  painter.setPen(self.normal_pen)
	  painter.drawText(w-40, h-30, u"•")
	elif self.minute == 4 or self.minute == 9:
	  painter.setPen(self.highl_pen)
	  painter.drawText(30, 40, u"•")
	  painter.drawText(w-40, 40, u"•")
	  painter.drawText(30, h-30, u"•")
	  painter.drawText(w-40, h-30, u"•")
	

        # DRAW THE BASE
        top  = 80
        left = 80
        idx  = 0
        for st in MATRIX[self.language]:
            if st == '\n':
                top += self.tx_font.pointSize()*2
                left = 80
            else:
                if idx in self.to_render:
                    painter.setPen(self.highl_pen)
                else:
                    painter.setPen(self.normal_pen)
                if st == u'Ĺ':
                    painter.drawText(left, top, u"L'")
                else:
                    painter.drawText(left, top, st)
                left += self.tx_font.pointSize()*2
            idx += 1

        painter.restore()

    def createConfigurationInterface(self, parent):
        widget = QWidget(parent)
        vbox = QVBoxLayout(widget)

        grp_1 = QGroupBox("Font", widget)
        h1    = QHBoxLayout(grp_1)
        self.lb_font = QLabel(str(parent.font()), widget)
        self.bt_font = QPushButton("Change...", widget)
        h1.addWidget(self.lb_font)
        h1.addSpacing(50)
        h1.addWidget(self.bt_font)

        grp_2 = QGroupBox("Background Color", widget)
        h2    = QHBoxLayout(grp_2)
        self.lb_bgcol = QLabel("", widget)
        self.bt_bgcol = QPushButton("Change...", widget)
        h2.addWidget(self.lb_bgcol)
        h2.addSpacing(50)
        h2.addWidget(self.bt_bgcol)
        self.lb_bgcol.setMinimumSize(QSize(48, 24))

        grp_3 = QGroupBox("Opacity", widget)
        h3    = QHBoxLayout(grp_3)
        self.sl_alpha = QSlider(Qt.Horizontal, widget)
        self.sl_alpha.setMinimum(0)
        self.sl_alpha.setMaximum(255)
        h3.addWidget(self.sl_alpha)

        grp_4 = QGroupBox("Language", widget)
        h3    = QHBoxLayout(grp_4)
        self.bt_lang = QComboBox(widget)
        self.bt_lang.insertItem(0, "Italian");
        self.bt_lang.insertItem(1, "English");
        self.bt_lang.insertItem(2, "German");
        self.bt_lang.setCurrentIndex(self.language);
        h3.addWidget(self.bt_lang)

        self.update_color_label ()
        self.update_font_label  ()
        self.update_alpha_slider()
        self.update_lang_combo  ()

        vbox.addWidget(grp_1)
        vbox.addWidget(grp_2)
        vbox.addWidget(grp_3)
        vbox.addWidget(grp_4)

        self.connect(self.bt_font , SIGNAL('clicked()'), self.on_font_select   )
        self.connect(self.bt_bgcol, SIGNAL('clicked()'), self.on_bgcolor_select)
        self.connect(self.sl_alpha, SIGNAL('valueChanged(int)'), self.on_alpha_changed)
        self.connect(self.bt_lang, SIGNAL("currentIndexChanged(int)"), self.on_lang_changed)
        self.connect(parent, SIGNAL("accepted()"), self.save_config)

        # free widget
        self.connect(parent, SIGNAL("accepted()"), widget.deleteLater)
        self.connect(parent, SIGNAL("rejected()"), widget.deleteLater)

        parent.addPage(widget, "Plasma Qlock", "clock");
        return widget

    def update_color_label(self):
        r = self.bg_color.color().red()
        g = self.bg_color.color().green()
        b = self.bg_color.color().blue()
        ss = 'QLabel {{ background: rgb({0},{1},{2}); }}'.format(r, g, b)
        self.lb_bgcol.setStyleSheet(ss)

    def update_font_label(self):
        fnt_info = QFontInfo(self.tx_font)
        self.lb_font.setFont(self.tx_font)
        self.lb_font.setText(fnt_info.family())

    def update_alpha_slider(self):
        a = self.bg_color.color().alpha()
        self.sl_alpha.setValue(a)

    def update_lang_combo(self):
        self.language = self.bt_lang.currentIndex()

    def update_size(self):
        font_sz = self.tx_font.pointSize()
        w = font_sz * 21 + 40
        h = font_sz * 17 + 80
        self.resize(w, h)

    def on_font_select(self):
        font_dlg = QFontDialog(self.parent())
        font_dlg.setCurrentFont(self.tx_font)
        if font_dlg.exec_() == 1:
            self.tx_font = font_dlg.selectedFont()
            self.update_font_label()
            self.update_size()

    def on_bgcolor_select(self):
        col_dlg = QColorDialog(self.parent())
        col_dlg.setCurrentColor(self.bg_color.color())
        if col_dlg.exec_() == 1:
            col = col_dlg.selectedColor()
            col.setAlpha(self.sl_alpha.value())
            self.bg_color = QBrush(col)
            self.update_color_label()

    def on_alpha_changed(self, val):
        col = self.bg_color.color()
        col.setAlpha(self.sl_alpha.value())
        self.bg_color = QBrush(col)

    def on_lang_changed(self, val):
        self.language = val

    def save_config(self):
        config = self.config()
        fnt_info = QFontInfo(self.tx_font)
        config.writeEntry('tx_font_nm', fnt_info.family())
        config.writeEntry('tx_font_sz', fnt_info.pointSize())
        config.writeEntry('bg_color_r', self.bg_color.color().red())
        config.writeEntry('bg_color_g', self.bg_color.color().green())
        config.writeEntry('bg_color_b', self.bg_color.color().blue())
        config.writeEntry('bg_color_a', self.bg_color.color().alpha())
        config.writeEntry('language'  , self.bt_lang.currentIndex())
        config.sync()
        self.update()

def CreateApplet(parent):
    return PlasmaQlock(parent)
