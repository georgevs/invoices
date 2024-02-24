import itertools
import pdfplumber
import re


class Pdf:
  def __init__(self, stream=None, file_path=None):
    assert stream or file_path
    self.stream = stream
    self.file_path = file_path

  def __iter__(self):
    with pdfplumber.open(path_or_fp=self.stream or self.file_path) as pdf:
      for page in pdf.pages:
        yield from Pdf.__get_page_lines(page)

  def __get_page_lines(page):  
    words = page.extract_words(keep_blank_chars=True, y_tolerance=0, x_tolerance=0)
    def update_word(word):
      word.update(
        top=pts_to_mm(word.get('top')), 
        x0=pts_to_mm_10(word.get('x0')),
        x1=pts_to_mm_10(word.get('x1')),
      )
      return word
    words = map(update_word, words)
    words = filter(lambda it: len(it.get('text')) > 0 and it.get('upright'), words)
    words = sorted(words, key=lambda it: (it.get('top'), it.get('x0')))
    for line_top, line_words in itertools.groupby(words, key=lambda it: it.get('top')):
      line_words = Pdf.__join_overlapping_words(line_words, distance=5)
      line_words = map(lambda it: it.get('text'), line_words)
      text = ' '.join(line_words)
      yield text

  def __join_overlapping_words(words, distance=0):
    joined_words = [word] if (word := next(words)) is not None else []
    for word in words:
      last_word = joined_words[-1]
      if last_word.get('x1') + distance < word.get('x0'):
        joined_words.append(word)
      else:
        x1 = word.get('x1')
        text = last_word.get('text') + word.get('text')
        last_word.update(x1=x1, text=text)
    return joined_words


def pts_to_mm(x):
  return round(1/72 * 2.54 * 10 * x)

def pts_to_mm_10(x):
  return int(1/72 * 2.54 * 100 * x)
