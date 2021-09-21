# SCRU-160: Sortable, Clock and Random number-based Unique identifier

SCRU-160 ID is yet another attempt to supersede [UUID] in the use cases that
need decentralized, globally unique time-ordered identifiers. SCRU-160 is
inspired by [ULID] and [KSUID] and has the following features:

- 160-bit length
- Sortable by generation time (in binary and in text)
- Two case-insensitive encodings: 32-character base32hex and 40-character hex
- More than 32,768 unique, time-ordered but unpredictable IDs per millisecond
- Nearly 111-bit randomness for collision resistance

```python
from scru160 import scru160, scru160f

print(scru160())  # e.g. "05TVFQQ8UGDNKHDJ79AEGPHU7QP7996H"
print(scru160())  # e.g. "05TVFQQ8UGDNNVCCNUH0Q8JDD3IPHB8R"

print(scru160f())  # e.g. "017bf7eb48f41b7d6bd295bc5adc43436bc969df"
print(scru160f())  # e.g. "017bf7eb48f41b7e1bc98aec348dfa1539b41288"
```

[uuid]: https://en.wikipedia.org/wiki/Universally_unique_identifier
[ulid]: https://github.com/ulid/spec
[ksuid]: https://github.com/segmentio/ksuid

## Command-line interface

`scru160` generates SCRU-160 IDs.

```bash
$ scru160
05U0G9S45SUOL4C8FNQFKQ5M6VEROV9J
$ scru160 -f
017c08279e9f4e32b6f58d023b9fc41a22302750
$ scru160 -n 4
05U0G9TQQ8FONQQCC655GMBTBBHUIKK7
05U0G9TQQ8FOOJ7IR79Q6QFJ3OSNRF92
05U0G9TQQ8FORTQU0K5OOSANILGP72HO
05U0G9TQQ8FOTV6SEJVMV6OJQDP15MHC
```

`scru160-inspect` prints the components of given SCRU-160 IDs as human- and
machine-readable JSON objects.

```bash
$ scru160 -fn 2 | scru160-inspect
{
  "input":        "017c083c130732153679e83c4fc65664e6a964a1",
  "canonical":    "05U0GF0J0SP1ADJPT0U4VHIMCJJAIP51",
  "timestamputc": "2021-09-21 12:02:07.239+00:00",
  "timestamp":    "1632225727239",
  "counter":      "12821",
  "random16":     "13945",
  "random80":     "1096701577047146014270625",
  "hexfields":    ["017c083c1307", "3215", "3679", "e83c4fc65664e6a964a1"]
}
{
  "input":        "017c083c13073216a2ab5d302cebfca0916625a0",
  "canonical":    "05U0GF0J0SP1D8LBBKO2PQVSK28MC9D0",
  "timestamputc": "2021-09-21 12:02:07.239+00:00",
  "timestamp":    "1632225727239",
  "counter":      "12822",
  "random16":     "41643",
  "random80":     "440068763580938823542176",
  "hexfields":    ["017c083c1307", "3216", "a2ab", "5d302cebfca0916625a0"]
}
```

## License

Copyright 2021 LiosK

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
