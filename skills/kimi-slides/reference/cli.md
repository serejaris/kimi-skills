# kimi-slides cli

This section lists all commands supported by the kimi-slides CLI. This document is the authoritative reference! The guide returned by `kimi-slides --help` is incorrect — there is no need to run that command.

## convert

```bash
kimi-slides convert path/deck.pptx 
kimi-slides convert path/deck.pptx -o path/output/ 
```

`-o, --output`: specifies the output directory; optional. If omitted, a directory with the same name (without extension) is created next to the input:

```text
path/deck.pptx -> path/deck/
```

Output directory structure:

```text
deck/
  deck.pptd
  pages/
    page-1.page
  media/
    <hash>.png
```

> During conversion, images embedded in the PPTX are extracted into the `media/` directory, and image paths in the page files are rewritten to paths relative to the output directory:

```yaml
src: ./media/<hash>.png
```

## check

```bash
kimi-slides check path/deck 
kimi-slides check path/deck -p 1,3 -s all 
kimi-slides check path/deck -p 2-10 --level keep 
kimi-slides check path/deck --level auto 
```

The input to `check` must be a directory containing a `.pptd` file. By default it checks the main `.pptd` file and all page files.

Parameters:

- `-p, --page <spec>`: specifies page numbers, 1-based; defaults to all pages. Supports `3`, `1,2`, `2-10`.
- `-s, --severity <spec>`: specifies which issues to output. Supports `all`, `error`, `warning`, and also specific issue types, e.g. `MissingField,SrcNotFound`.
- `--level <level>`: handling level. `keep` only checks without modifying; `auto` attempts safe repairs.

The following issues are currently checked:
- `YamlParseError`: every checked file must parse correctly with a YAML parser.
- `FileReadError`: abnormal access to the input directory, the `.pptd` file, page files, or resource paths.
- `MissingField`: required fields are missing, e.g. `.pptd.pages`, `.pptd.size`, or required element fields.
- `InvalidType`: field types do not match their definitions, e.g. string, number, boolean, tuple, array, fill, border, etc.
- `OutOfRange`: field values fall outside the acceptable range, e.g. non-positive page size, non-positive bounds, illegal enum values.
- `InvalidTheme`: a referenced theme token does not exist, e.g. `$primary` is not present in `theme.colors`.
- `PageNotFound`: a `.page` file referenced by `.pptd.pages` does not exist, or a specified page number is out of range.
- `UnknownField`: a field not recognized by the current schema was found.
- `BoundsOutside`: an element's bounds exceed the page dimensions.
- `SrcNotFound`: a local resource referenced by `src` (image, image fill, custom font, etc.) does not exist.
- `TextOverflow`: text may overflow its text box.
- `TextUnderFill`: text may occupy less than 50% of the text box height.
- `TextOcclusion`: text may be occluded by elements drawn later.
- `TextDrift`: a text box may cross the boundary of an element below it.

> Text-related checks currently use a heuristic with mock text dimensions, so some deviation is possible.

`--level auto` only performs deterministic repairs:

- Simple type conversions, e.g. `"12"` to number, `12` to string, `"true"` to boolean.
- Deleting invalid optional fields.
- Deleting invalid elements that cannot be repaired safely.
- Rewriting the YAML formatting of repaired files.

`check` outputs issues in the following format:

```text
[whether deterministically fixed][issue type:issue name] file path id="element id" issue details
[fixed: false][Error:InvalidType] pages/page-1.page id="title" Expected 4 numbers for elements[0].bounds
[fixed: false][Warning:TextOverflow] pages/page-2.page id="body" Text may overflow its bounds
```

## screenshot

```bash
kimi-slides screenshot path/deck -o path/screenshots/
kimi-slides screenshot path/deck -p 1,3,5 -o path/screenshots/
kimi-slides screenshot path/deck -p 2-6 -o path/screenshots/
```

The input to `screenshot` must be a directory containing a `.pptd` file. This command renders the `.pptd` presentation into images for inspecting the visual result of the pages.

`-o, --output` is optional. If omitted, a screenshot directory is created next to the input:

```text
path/deck/ -> path/deck-screenshots/
```

The output directory structure is typically:

```text
pages/
  page-1.png
  page-2.png
  page-3.png
```

Parameters:

- `-p, --page <spec>`: specifies page numbers, 1-based; defaults to all pages. Supports `3`, `1,2`, `2-10`.
- `-o, --output <path>`: specifies the screenshot output directory.
