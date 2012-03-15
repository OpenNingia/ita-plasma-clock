#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Copyright Daniele Simonetti 2012

from PyQt4.QtGui   import *
from PyQt4.QtCore  import *
from PyKDE4.plasma import Plasma
from PyKDE4        import plasmascript

import sys
import os

from datetime import datetime

MATRIX = \
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
"""

HOURS = [
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
]

APP_NAME    = 'ItaPlasmaClock'
APP_ORG     = 'openningia'
APP_VERSION = '1.6'

def gimme_time():
    toks  = []
    now   = datetime.now()

    tell_hour = now.hour
    if now.minute >= 35:
        tell_hour += 1

    tell_hour = tell_hour % 12

    if tell_hour == 1:
        toks.append(u'È ĹUNA')
    else:
        toks.append(u'SONO LE ORE {0}'.format(HOURS[tell_hour]))

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


class ItaPlasmaClock(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

        self.to_render     = []
        self.old_to_render = []
        self.static_texts = [ x for x in MATRIX.split() ]
        self.update_clock()
        self.bg_color = QBrush(
                        QColor(0xA8, 0xD1, 0x1D, 200))
        self.normal_pen = QPen()
        self.normal_pen.setColor(QColor(0x99,0x99,0x99))
        self.highl_pen  = QPen()
        self.highl_pen.setColor(QColor(255,255,255))

    def init(self):
        self.setHasConfigurationInterface(True)
        self.setAspectRatioMode(Plasma.Square)

        # read configuration
        config = self.config()
        font_nm = config.readEntry('tx_font_nm', "").toString()
        font_sz = config.readEntry('tx_font_sz', 14).toInt()[0]
        self.tx_font = QFont(font_nm, font_sz)

        r = config.readEntry('bg_color_r', 0xA8).toInt()[0]
        g = config.readEntry('bg_color_g', 0xD1).toInt()[0]
        b = config.readEntry('bg_color_b', 0x1D).toInt()[0]
        a = config.readEntry('bg_color_a', 200).toInt()[0]
        self.bg_color = QBrush(QColor(r, g, b, a))

        w = font_sz * 21 + 40
        h = font_sz * 17 + 80
        self.resize(w, h)

        # create timer
        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.connect(self.timer, SIGNAL("timeout()"), self.on_timeout)
        self.timer.start()

    def on_timeout(self):
        self.update_clock()
        if self.old_to_render != self.to_render:
          self.update()

    def update_clock(self):
        toks = gimme_time().split()
        self.old_to_render = self.to_render
        self.to_render     = []
        idx = 0
        off = 0
        for t in toks:
            idx = MATRIX.find(t, off)
            if idx < 0:
                idx = 0
            for i in xrange(idx, idx+len(t)):
                self.to_render.append( i )
            off = idx + len(t)
        print self.to_render

    def paintInterface(self, painter, option, rect):
        painter.save()

        # PENS
        painter.setPen(self.normal_pen)
        painter.fillRect(rect, self.bg_color)
        painter.setFont(self.tx_font)

        # DRAW THE BASE
        top  = 40
        left = 20
        idx  = 0
        for st in MATRIX:
            if st == '\n':
                top += self.tx_font.pointSize()*2
                left = 20
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
        self.bt_font = QPushButton("Cambia...", widget)
        h1.addWidget(self.lb_font)
        h1.addSpacing(50)
        h1.addWidget(self.bt_font)

        grp_2 = QGroupBox("Background Color", widget)
        h2    = QHBoxLayout(grp_2)
        self.lb_bgcol = QLabel("", widget)
        self.bt_bgcol = QPushButton("Cambia...", widget)
        h2.addWidget(self.lb_bgcol)
        h2.addSpacing(50)
        h2.addWidget(self.bt_bgcol)
        self.lb_bgcol.setMinimumSize(QSize(48, 24))

        grp_3 = QGroupBox("Opacita'", widget)
        h3    = QHBoxLayout(grp_3)
        self.sl_alpha = QSlider(Qt.Horizontal, widget)
        self.sl_alpha.setMinimum(0)
        self.sl_alpha.setMaximum(255)
        h3.addWidget(self.sl_alpha)

        self.update_color_label ()
        self.update_font_label  ()
        self.update_alpha_slider()

        vbox.addWidget(grp_1)
        vbox.addWidget(grp_2)
        vbox.addWidget(grp_3)

        self.connect(self.bt_font , SIGNAL('clicked()'), self.on_font_select   )
        self.connect(self.bt_bgcol, SIGNAL('clicked()'), self.on_bgcolor_select)
        self.connect(self.sl_alpha, SIGNAL('valueChanged(int)'), self.on_alpha_changed)
        self.connect(parent, SIGNAL("accepted()"), self.save_config)

        # free widget
        self.connect(parent, SIGNAL("accepted()"), widget.deleteLater)
        self.connect(parent, SIGNAL("rejected()"), widget.deleteLater)

        parent.addPage(widget, "Orologio Italiano", "clock");
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

    def save_config(self):
        config = self.config()
        fnt_info = QFontInfo(self.tx_font)
        config.writeEntry('tx_font_nm', fnt_info.family())
        config.writeEntry('tx_font_sz', fnt_info.pointSize())
        config.writeEntry('bg_color_r', self.bg_color.color().red())
        config.writeEntry('bg_color_g', self.bg_color.color().green())
        config.writeEntry('bg_color_b', self.bg_color.color().blue())
        config.writeEntry('bg_color_a', self.bg_color.color().alpha())
        config.sync()
        self.update()

def CreateApplet(parent):
    return ItaPlasmaClock(parent)