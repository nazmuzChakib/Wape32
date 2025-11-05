#!/usr/bin/env python3
"""
html_to_header.py
Convert an HTML file into a gzipped C header (xxd -i style).
Usage:
    python3 html_to_header.py index.html

Output:
    Saves the generated header into the sibling folder '../pages'
    relative to where this script file lives. (e.g. if this script is
    in .../webserver/utils, output goes to .../webserver/pages)
"""

import sys
import os
import gzip
import re
from datetime import datetime

def make_c_identifier(name: str) -> str:
    # Replace non-alnum with underscore, ensure doesn't start with digit
    ident = re.sub(r'[^0-9A-Za-z_]', '_', name)
    if re.match(r'^[0-9]', ident):
        ident = '_' + ident
    return ident

def html_to_header(filepath: str):
    if not filepath:
        print("Missing argument - filename!")
        sys.exit(1)

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    # base filename without extension
    base = os.path.splitext(os.path.basename(filepath))[0]
    safe_base = make_c_identifier(base)
    guard = f"PAGE_{safe_base.upper()}_H"

    # Determine script directory and target pages directory (../pages)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pages_dir = os.path.normpath(os.path.join(script_dir, "..", "pages"))
    os.makedirs(pages_dir, exist_ok=True)

    output_filename = os.path.join(pages_dir, f"page_{base}.h")

    # Read original file and gzip-compress into memory
    with open(filepath, "rb") as f_in:
        raw = f_in.read()
    compressed = gzip.compress(raw, compresslevel=9)

    # current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create header file in pages directory
    with open(output_filename, "w", newline="\n") as out:
        out.write(f"#ifndef {guard}\n")
        out.write(f"#define {guard}\n\n")
        out.write("// This file was generated using Python script (gzip -> C array)\n")
        out.write(f"// Gzip generated on: {timestamp}\n\n")

        # Write array in xxd -i style (uppercase hex, 16 bytes per line)
        out.write(f"unsigned char page_{safe_base}[] = {{\n")
        for i, b in enumerate(compressed):
            if i % 16 == 0:
                out.write("  ")
            out.write(f"0x{b:02X}")
            if i != len(compressed) - 1:
                out.write(", ")
            if (i + 1) % 16 == 0:
                out.write("\n")
        out.write("\n};\n\n")
        out.write(f"unsigned int page_{safe_base}_len = {len(compressed)};\n\n")
        out.write("#endif\n")

    print(f"✅ Generated: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 html_to_header.py <filename.html>")
        sys.exit(1)
    html_to_header(sys.argv[1])




# #!/usr/bin/env python3
# """
# html_to_header.py
# Convert an HTML file into a gzipped C header (xxd -i style).
# Usage:
#     python3 html_to_header.py index.html
# The generated file will be named `page_<basename>.h` and placed
# in the same folder where you run the script.
# """

# import sys
# import os
# import gzip
# import re

# def make_c_identifier(name: str) -> str:
#     # Replace non-alnum with underscore, ensure doesn't start with digit
#     ident = re.sub(r'[^0-9A-Za-z_]', '_', name)
#     if re.match(r'^[0-9]', ident):
#         ident = '_' + ident
#     return ident

# def html_to_header(filepath: str):
#     if not filepath:
#         print("Missing argument - filename!")
#         sys.exit(1)

#     if not os.path.exists(filepath):
#         print(f"File not found: {filepath}")
#         sys.exit(1)

#     base = os.path.splitext(os.path.basename(filepath))[0]
#     # sanitized base for C identifiers
#     safe_base = make_c_identifier(base)
#     output_filename = f"page_{base}.h"
#     guard = f"PAGE_{safe_base.upper()}_H"

#     # temp compressed filename (match original script style: no .gz ext)
#     compressed_name = f"page_{base}"

#     # gzip compress (best)
#     with open(filepath, 'rb') as f_in, gzip.open(compressed_name, 'wb', compresslevel=9) as f_out:
#         f_out.writelines(f_in)

#     # read compressed data
#     with open(compressed_name, 'rb') as f:
#         data = f.read()

#     # create header file in current directory
#     with open(output_filename, 'w') as out:
#         out.write(f"#ifndef {guard}\n")
#         out.write(f"#define {guard}\n\n")
#         out.write("// This file was generated using Python script (gzip -> C array)\n\n")

#         # Write array in xxd -i style (uppercase hex, 16 bytes per line)
#         out.write(f"unsigned char page_{safe_base}[] = {{\n")
#         for i, b in enumerate(data):
#             if i % 16 == 0:
#                 out.write("  ")
#             out.write(f"0x{b:02X}")
#             if i != len(data) - 1:
#                 out.write(", ")
#             if (i + 1) % 16 == 0:
#                 out.write("\n")
#         out.write("\n};\n\n")
#         out.write(f"unsigned int page_{safe_base}_len = {len(data)};\n\n")
#         out.write("#endif\n")

#     # remove temp compressed file
#     try:
#         os.remove(compressed_name)
#     except OSError:
#         pass

#     print(f"✅ Generated: {os.path.abspath(output_filename)}")

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python3 html_to_header.py <filename.html>")
#         sys.exit(1)
#     html_to_header(sys.argv[1])