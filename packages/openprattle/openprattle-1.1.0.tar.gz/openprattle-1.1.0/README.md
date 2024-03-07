# OpenPrattle

A command-line tool and python library that provides a seamless interface to both the [Pybel library](https://github.com/openbabel/openbabel/tree/master/scripts/python) and [obabel](https://github.com/openbabel/openbabel) command-line tool.

## Dependencies

### Required

Openbabel >= 3.0.0

Python >= 3.9

### Optional

JSON (for printing in JSON format with the --readable and --writable options)

pytest (for running the unit tests)

## Usage

OpenPrattle provides both a python library and command-line tool.

### Library

Files are interconverted using converter objects, each of which represents a supported backend.
To automatically get a suitable converter object, use `openprattle.Openbabel_converter.from_file()`:

```python
from openprattle import Openbabel_converter

my_file = "Benzene.xyz"
converter = Openbabel_converter.from_file(input_file_path = my_file)
```

By default, the format of the input file is determined automatically from its extension. The format
can be explicitly specified with `input_file_type`:

```python
converter = Openbabel_converter.from_file(input_file_path = my_file, input_file_type = "xyz")
```

`Openbabel_converter.from_file()` will favour the Pybel backend if it is available, except when
converting files in formats that are not supported by Pybel. To explicitly choose a backend, use
the `backend` option:

```python
converter = Openbabel_converter.from_file(
    input_file_path = my_file,
    input_file_type = "xyz",
    backend = "Pybel" # Either 'Pybel', 'Obabel', or 'Auto'
)
```

Or use the appropriate class directly.

```python
from openprattle import Obabel_converter, Pybel_converter

my_file = "Benzene.xyz"
obabel = Obabel_converter(
    input_file_path = my_file
)
pybel = Pybel_converter(
    input_file_path = my_file
)
```

In addition to reading from a file path, all the converters can read from an open file descriptor
using `input_file`:

```python
with open("Benzene.xyz") as my_file:
    converter = Openbabel_converter.from_file(
        input_file = my_file,
        input_file_type = "xyz",
    )
```

Or from a memory buffer using `input_file_buffer`:

```python
with open("Benzene.xyz") as my_file:
    buffer = my_file.read()

converter = Openbabel_converter.from_file(
    input_file_buffer = buffer,
    input_file_type = "xyz",
)
```

Whenever the `input_file` or `input_file_buffer` options are used, the file type must be specified
with `input_file_type`.

Once an appropriate converter object has been obtained, the file can be converted by calling `convert()`:

```python
converter = Openbabel_converter.from_file(input_file_path = "Benzene.xyz")
converter.convert("cml", "Benzene.cml")
```

`convert()` can either write to a file (using `output_file`), or return the converted file as a buffer
(if `output_file` is omitted):

```python
converter = Openbabel_converter.from_file(input_file_path = "Benzene.xyz")
output_file = converter.convert("cml")
print(output_file)
```

A limited subset of formats support molecular charge and multiplicity information. These can be set
using the ``charge`` and ``multiplicity`` options:

```python
converter = Openbabel_converter.from_file(input_file_path = "Benzene.xyz")
converter.convert("cml", "Benzene.cml", charge = 1, multiplicity = 2)
```

The following is a non-exhaustive list of formats that do support charge and multiplicity:
 - com (Gaussian input)
 - dalmol (DALTON input)
 - gau (Gaussian input)
 - gjc (Gaussian input)
 - gjf (Gaussian input)
 - gzmat (Gaussian Z-Matrix Input)

Of these, only dalmol is both a readable and writable format.

> [!IMPORTANT]
> Currently, OpenPrattle is not aware of which formats will preserve the specified charge
> and multiplicity. If an unsupported format is chosen, any charge and multiplicity information
> will be silently discarded.

Charge and multiplicity are only supported with the `Pybel_converter` backend. This means that to
convert from a format that is not supported by Pybel (most noticeably ChemDraw's .cdx), two
conversions should be performed in sequence:

```python
from openprattle import Openbabel_converter, Pybel_converter

intermediate = Openbabel_converter.from_file(input_file_path = "Benzene.cdx").convert("xyz")
final = Pybel_converter(input_file_buffer = "intermediate", input_file_type = "xyz").convert(
    "com",
    charge = 1,
    multiplicity = 2
)
```

1D (eg, SMILES) and 2D (eg, ChemDraw) can be converted to 3D structures using Openbabel's
[`gen3D` option](https://open-babel.readthedocs.io/en/latest/3DStructureGen/SingleConformer.html#gen3d).
Gen3D performs a rapid geometry optimisation using a molecular force field. While this is normally useful
for generating a good starting geometry for further optimisations, it is rarely desirable for coordinates
that are already in three-dimensions.

The default behaviour in OpenPrattle (`gen3D = 'auto'`) is to convert geometries to three-dimensions so
long as the coordinates are not already in 3D. The function to determine the input geometry dimensions
is exposed by Pybel, but not by the obabel command-line tool. This means that automatic conversion with
gen3D will only occur when using the Pybel backend, unless the input format is exclusively non-3D (such
as ChemDraw's cdx).

The 3D conversion can be explicitly requested or disabled by using `gen3D = True` or `gen3D = False`
respectively.

```python
output = Openbabel_converter.from_file(input_file_path = "Benzene.cdx").convert(
    "xyz",
    gen3D = True
)
```

### Command-line

The oprattle command-line tool has the following main syntax:

```shell
$ oprattle input_file [-i INPUT_FORMAT] [-o OUTPUT_FORMAT] -O OUTPUT_FILE
```

For example:

```shell
$ oprattle Benzene.xyz -O Benzene.cml
```

Explicit input and output formats can be specified using `[-i INPUT_FORMAT]` and 
`[-o OUTPUT_FORMAT]` respectively.

```shell
$ oprattle Benzene.file1 -i xyz -o cml -O Benzene.file2
```

Either (or both) of the input file and output file can be omitted to read from
stdin or to write to stdout:

```shell
$ cat Benzene.xyz | oprattle i xyz -o cml
```

The backend can be chosen with the ``--backend`` option:
```shell
$ oprattle Benzene.cdx -O Benzene.cml --backend Obabel
```

Charge, multiplicity, and 3D conversion can be set using ``--charge``,
``--multiplicity``, and ``--gen3D`` respectively.

```shell
$ oprattle Benzene.cdx -O Benzene.cml --charge 1 --multiplicity 2 --gen3D True
```

The same caveats for charge, multiplicity, and gen3D apply as for the OpenPrattle library
(see above).

To see a list of supported input and output formats, use the ``--readable`` and ``--writable`` options:

```bash
$ oprattle --readable
abinit     : ABINIT Output Format
acesout    : ACES output format
acr        : ACR format
...
```

```bash
$ oprattle --writable
acesin     : ACES input format
adf        : ADF cartesian input format
alc        : Alchemy format
...
```

Either `--readable` or `--writable` can be combined with `--json` (if the JSON library is available)
to print the list of formats in JSON format:

```bash
$ oprattle --readable --json
"abinit": "ABINIT Output Format", "acesout": "ACES output format", "acr": "ACR format"...
```


## Why?

On the surface, the pybel library and obabel tool appear to offer the same functionality. However, there are important instances where each offers functionality over the other. For example, pybel allows for the molecular charge and multiplicity to be set in some output formats, obabel does not.
Conversely, obabel can read from ChemDraw (.cdx) files, while pybel cannot.

In addition, the programmer may not know ahead of time whether pybel and/or obabel will be available on the target system.
OpenPrattle allows for this scenario.

## Name?

A light-hearted pun; 'prattle' and 'babel' are approximate synonyms.

## Licensing

[OpenBabel](https://github.com/openbabel/openbabel) is licensed under GPL 2.0. Because OpenPrattle depends on the pybel library, it too must be licensed under the GPL.
