Retouche applied to the LaTeX source:
=====================================

- $f_h'$ is converted incorrectly by MathType (bug report sent, no reply so far)

- alignment (&) in equations is converted incorrectly

- Include LaTeX version of figures using \AsPicture{} command

  - All tables automatically use \AsPicture

- PDF images must be in PS format, convert using:

    find . -name "*.pdf" | xargs -l pdf2ps
    
  - Do not specify file extension with \includegraphics

- Placement [t] not supported, all figures automatically placed [h] regardless
  of modifier. TRR template places all figures at end.

- --- (em rule) not supported

- Formulae like $a, b$ and $FIT$ do not get converted by MathType

Conversion command:
===================

htlatex Paper_bj_FleetChoice.tex "../../../../_latexfiles/tex2word/ivt.cfg,word" 'symbol/!' "-cvalidate -e../../../../_latexfiles/tex2word/tex4ht.env"

- Verbatim math and \AsPicture command is provided by my.cfg

- Producing figures at 600 dpi is provided by tex4ht.env

Retouche required in Word after conversion:
===========================================

- Macros inside formulae are not expanded

- Hyphenation and spell check language

- \eject and \clearpage have no effect

- Rescale pictures to 14 %

- Layout: Section heading format not tied with subsequent paragraph

- Page margins and font size

- Convert embedded math using MathType

  - Optionally: Convert MathType equations to Office 2007/2010 equations using GrindEq Equation-To-Word
  
- Page headers if necessary (in TRR it seems to be)

- Embed pictures as in http://www.onemanwrites.co.uk/2011/09/13/how-to-embed-linked-images-in-word-2010/
  or http://www.onemanwrites.co.uk/2009/03/16/how-to-embed-linked-images-in-word-2007/


Not handled:
============

- Hyperlinks don't seem to work in the final document and should be removed

- Subfigures


Problems worked around:
=======================

- Uppercase section titles and figure captions do not seem to work, edit manually

- Tables: superfluous lines

  - a non-issue if tables are included as images

- algorithmic package: new line before "Ensure" is missing; incorrect indentation

  - include as image


