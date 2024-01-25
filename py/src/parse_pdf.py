def parse_and_validate_digest_table(table, digest):
  errors = []
  for format_label, parse_and_validate_digest in table.items():
    error, data = parse_and_validate_digest(digest)
    if data: return (None, data)
    else: errors.append({ format_label: error })

  return (errors, None)
