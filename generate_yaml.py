import os
import re

files = sorted([
    f for f in os.listdir(".")
    if f.endswith(".h") and f not in ("animations.h", "animation_types.h")
])

def extract_array(txt):
    m = re.search(
        r"static\s+const\s+uint16_t\s+PROGMEM\s+(\w+Frames)\s*\[\]\s*=\s*\{",
        txt
    )
    if not m:
        return None, None

    name = m.group(1)

    start = m.end()
    level = 1
    i = start

    while i < len(txt):
        if txt[i] == "{":
            level += 1
        elif txt[i] == "}":
            level -= 1
            if level == 0:
                body = txt[start:i]
                return name, body
        i += 1

    return None, None


print(
"""esphome:
  name: matrix-led

esp32:
  board: esp32-s3-devkitc-1
  framework:
    type: arduino

wifi:
  ssid: "changeme"
  password: "changeme"

logger:

api:

ota:
  platform: esphome

light:
  - platform: neopixelbus
    id: matrix
    name: "Matrix panel"
    type: GRB
    variant: WS2812
    pin: 33
    num_leds: 256
    internal: true

    effects:
"""
)

for f in files:
    with open(f, "r") as fh:
        txt = fh.read()

    arr_name, body = extract_array(txt)

    if not body:
        print("      # ERROR parsing " + f)
        continue

    effect = os.path.splitext(f)[0]

    print(f"""      - addressable_lambda:
          name: "{effect}"
          update_interval: 80ms
          lambda: |-
""")

    code = f"""
static const uint16_t {arr_name}[] PROGMEM = {{{body}}};

const int PIXELS = 256;
const int FRAMES = sizeof({arr_name}) / sizeof(uint16_t) / PIXELS;

static int frame = 0;

auto xy = [](int x, int y) {{
  if (y % 2 == 0)
    return y * 16 + x;
  else
    return y * 16 + (15 - x);
}};

auto rgb565 = [](uint16_t c) -> Color {{
  uint8_t r = ((c >> 11) & 0x1F) << 3;
  uint8_t g = ((c >> 5)  & 0x3F) << 2;
  uint8_t b = ( c        & 0x1F) << 3;
  return Color(r, g, b);
}};

for (int y = 0; y < 16; y++) {{
  for (int x = 0; x < 16; x++) {{

    int p = y * 16 + x;

    uint16_t col =
      pgm_read_word(&{arr_name}[frame * PIXELS + p]);

    it[ xy(x,y) ] = rgb565(col);
  }}
}}

frame++;
if (frame >= FRAMES) frame = 0;
"""

    for line in code.splitlines():
        print("            " + line)

