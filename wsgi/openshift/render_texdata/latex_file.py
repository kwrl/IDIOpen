#coding:utf8
""" The latex to be rendered
"""


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
