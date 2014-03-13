#!/usr/bin/python
# -*- coding:utf-8

from seqdiag import parser, builder, drawer
import sys;
sys.path.append("..");


diagram_definition = u"""
   seqdiag {
       "c:Contestant" -> ":WebServer" [label = "GET /IDIOpen/accounts/register/"];
       ":WebServer" -> "
   }
"""
tree = parser.parse_string(diagram_definition)
diagram = builder.ScreenNodeBuilder.build(tree)
draw = drawer.DiagramDraw('PNG', diagram, filename="RegisterContestantSeq.png")
draw.draw()
draw.save()

# EOF