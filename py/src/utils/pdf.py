"""
digest :: [str]
digest_pdf :: file_path -> digest
"""

from functools import partial, reduce
from operator import add
from pdfplumber import open as open_pdf
from pdfplumber.page import Page
from re import compile
from utils.fn import branch, ifilter, group_by, group_value_lens, imap, ipick, join_str, pick, pipe, sort_by, strip_str
from utils.ranges import number_in_number_ranges

mul = lambda x: lambda y: x * y
pts_to_mm = pipe(mul(1/72 * 2.54 * 10), round)

number_with_spaces_pattern = compile(r'[\s\d,]+')
normalize_number = lambda text: text.replace(' ', '') if number_with_spaces_pattern.fullmatch(text) else text

extract_page_words = partial(Page.extract_words, keep_blank_chars=True, y_tolerance=0, x_tolerance=1)

word_dimention = lambda key: pipe(pick(key), pts_to_mm)
word_top = word_dimention('top')
word_left = word_dimention('x0')
word_right = word_dimention('x1')
word_top_left = lambda word: (word_top(word), word_left(word))
word_text = pipe(pick('text'), strip_str(), normalize_number)

word_to_label = pipe(branch(word_top, word_left, word_right, word_text), tuple)
label_top = pick(0)
label_left = pick(1)
label_right = pick(2)
label_top_left = pipe(ipick(0, 1), tuple)
label_text = pick(3)
label_text_is_not_empty = lambda label: len(label_text(label)) > 0

extract_page_labels = pipe(
  extract_page_words,
  imap(word_to_label),
  ifilter(label_text_is_not_empty)
)

sort_labels_by_top_left = sort_by(label_top_left)
group_labels_in_lines_by_top = pipe(group_by(label_top), imap(group_value_lens.view))

def group_labels_next_to_each_other(labels, distance=1):
  rs = []
  prev_label = None
  for label in labels:
    if prev_label is None or label_left(label) - label_right(prev_label) > distance:
      rs.append([label])
    else:
      rs[-1].append(label)
    prev_label = label
  return rs

collate_labels_text = pipe(imap(label_text), join_str(' '))
line_labels_to_text = pipe(
  group_labels_next_to_each_other,
  imap(collate_labels_text), 
  join_str(' ___ ')
)
transform_lines_labels_to_text = imap(line_labels_to_text)

digest_page = pipe(
  extract_page_labels,
  sort_labels_by_top_left,
  group_labels_in_lines_by_top,
  transform_lines_labels_to_text,
  list
)

digest_pdf_pages = pipe(imap(digest_page), partial(reduce, add))

page_number = lambda page: page.page_number
is_page_in_pages_ranges = lambda pages_ranges: (
  pipe(page_number, partial(number_in_number_ranges, pages_ranges)) if pages_ranges
  else lambda _: True
)
digest_pdf_pages_ranges = lambda pages_ranges: (
  pipe(ifilter(is_page_in_pages_ranges(pages_ranges)), digest_pdf_pages)
)

def digest_pdf(file_path, pages_ranges=None):
  with open_pdf(file_path) as pdf:
    return digest_pdf_pages_ranges(pages_ranges)(pdf.pages)
