import re
import preprocessor as p


text = 'Preprocessor is #awesome 👍 https://github.com/s/preprocessor'
text = text.replace('#', '')
p.set_options(p.OPT.URL, p.OPT.EMOJI)
text = p.clean(text)
print(text)