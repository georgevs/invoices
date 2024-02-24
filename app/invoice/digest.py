
class Digest:
  def __init__(self, Parser):
    self.Parser = Parser

  def get_digest(self, lines):
    parser = self.Parser()
    try:
      for line in lines:
        parser.parse_line(line)
        if parser.is_complete():
          break
      return parser.get_digest(), None
    
    except Exception as error:
      return None, error
