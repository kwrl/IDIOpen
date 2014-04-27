""" The latex to be rendered
"""

CONTESTANT_PARSELINE = "%(contestant_line)s"
TEAM_PARSELINE = "%(team)s"

LATEX_PARSE = r"""
\documentclass{article}
\begin{document}
\textbf{\huge """ + \
TEAM_PARSELINE + r""" \\}
\vspace{1cm}
""" + \
CONTESTANT_PARSELINE + r"""
\end{document}
"""

# EOF
