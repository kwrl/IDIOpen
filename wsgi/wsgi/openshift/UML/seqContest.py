#!/usr/bin/python
# -*- coding:utf-8

from seqdiag import parser, builder, drawer


diagram_definition = u"""
   seqdiag {
       "a:Admin" -> ":WebServer" [label = "[Logged in] GET /admin/contestslist/contest/add/"];
       ":WebServer" -> ":WebServer" [label = "POST /admin/contestlist/contest/add/"];
       ":WebServer" -> "cf:ContestForm" [label = "init()" ];
       === [is_valid()] ===
       "cf:ContestForm" -> "cf:ContestForm" [label = "save()" ];
       "cf:ContestForm" -> ":Database" [label = "saveForm()", note = "save data to DB"]
       "cf:ContestForm" <-- ":Database"
       === [! is_valid() ] ===
       "cf:ContestForm" --> ":WebServer" [ label  = "Error message", ]
    }
"""
tree = parser.parse_string(diagram_definition)
diagram = builder.ScreenNodeBuilder.build(tree)
draw = drawer.DiagramDraw('PNG', diagram, filename="CreateContestSeq.png")
draw.draw()
draw.save()



# EOF