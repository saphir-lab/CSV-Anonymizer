# CSV Anonymizer Roadmap

Roadmap is not yet fully established. Instead, let's present backlog of possible improvements.

## Backlog

- Possibility to hash part of field value. Use cases:
  - e-mail : keep e-mail domain unhashed (xxxxx@gmail.com)
  - phone : keep country code part in clear text but hash the rest (+32 xxxx)
  - IBAN : keep country code part in clear text but hash the rest (BExxxxx)
- YAML validation using Schema (see pyKwalify or Yamale)
- Different level of debugging information displayed in the console during execution.
- All Parameters from command line ?
- Possibility to be fully interactive ?
