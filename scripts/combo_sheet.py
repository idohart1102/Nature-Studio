"""Combo results workbook: stdlib .xlsx writer/reader and Drive sync through rclone.

The Google Sheet is round-tripped as .xlsx: export the live sheet, read user edits, merge, rebuild and
upload as a new revision of the same file (same ID). Formatting (dropdowns, red rows) is rebuilt each time.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import json
import re
import subprocess
import tempfile
import zipfile
import xml.etree.ElementTree as ET

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
RID = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def col_name(index):
    name = ''
    index += 1
    while index:
        index, rem = divmod(index - 1, 26)
        name = chr(65 + rem) + name
    return name


def _cell(ref, value, style):
    if value is None or value == '':
        return f'<c r="{ref}" s="{style}"/>'
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f'<c r="{ref}" s="{style}"><v>{value}</v></c>'
    text = escape(str(value)).replace('"', '&quot;')
    return f'<c r="{ref}" s="{style}" t="inlineStr"><is><t xml:space="preserve">{text}</t></is></c>'


def _sheet_xml(sheet):
    rows, widths = sheet['rows'], sheet.get('widths', [])
    cols = ''.join(f'<col min="{i + 1}" max="{i + 1}" width="{w}" customWidth="1"/>' for i, w in enumerate(widths))
    body = []
    for r, row in enumerate(rows, 1):
        style = 1 if r == 1 else 2
        cells = ''.join(_cell(f'{col_name(c)}{r}', v, style) for c, v in enumerate(row))
        body.append(f'<row r="{r}">{cells}</row>')
    last = f'{col_name(max(len(sheet["rows"][0]) - 1, 0))}{max(len(rows), sheet.get("min_rows", 0) + 1, 2)}'
    parts = [f'<worksheet xmlns="{NS["m"]}" xmlns:r="{RID}">',
             '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>',
             f'<cols>{cols}</cols>' if cols else '', f'<sheetData>{"".join(body)}</sheetData>']
    for priority, rule in enumerate(sheet.get('highlights', []), 1):  # {'column': 'X', 'contains': '...', 'color': 'red'|'yellow'}
        formula = escape(f'ISNUMBER(SEARCH("{rule["contains"]}",${rule["column"]}2))')
        parts.append(f'<conditionalFormatting sqref="A2:{last}"><cfRule type="expression" dxfId="{DXF[rule.get("color", "red")]}" '
                     f'priority="{priority}"><formula>{formula}</formula></cfRule></conditionalFormatting>')
    validations = sheet.get('dropdowns', [])  # {'range': 'I2:I500', 'options': [...]}
    if validations:
        items = ''.join(
            f'<dataValidation type="list" allowBlank="1" showDropDown="0" sqref="{v["range"]}">'
            f'<formula1>"{escape(",".join(v["options"]))}"</formula1></dataValidation>' for v in validations)
        parts.append(f'<dataValidations count="{len(validations)}">{items}</dataValidations>')
    parts.append('</worksheet>')
    return ''.join(parts)


DXF = {'red': 0, 'yellow': 1}
STYLES = (f'<styleSheet xmlns="{NS["m"]}">'
          '<fonts count="2"><font><sz val="10"/><name val="Arial"/></font><font><b/><sz val="10"/><name val="Arial"/></font></fonts>'
          '<fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill>'
          '<fill><patternFill patternType="solid"><fgColor rgb="FFD9EAD3"/></patternFill></fill></fills>'
          '<borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs>'
          '<cellXfs count="3"><xf/>'
          '<xf fontId="1" fillId="2" applyFont="1" applyFill="1" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>'
          '<xf applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf></cellXfs>'
          '<dxfs count="2"><dxf><font><color rgb="FF9C0006"/></font><fill><patternFill><bgColor rgb="FFF4C7C3"/></patternFill></fill></dxf>'
          '<dxf><fill><patternFill><bgColor rgb="FFFFF2CC"/></patternFill></fill></dxf></dxfs>'
          '</styleSheet>')


def write_xlsx(path, sheets):
    """sheets: list of {'name', 'rows', 'widths'?, 'dropdowns'?, 'highlights'?, 'min_rows'?}."""
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',
                   '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                   '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
                   + ''.join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                             for i in range(1, len(sheets) + 1)) + '</Types>')
        z.writestr('_rels/.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        z.writestr('xl/workbook.xml', f'<workbook xmlns="{NS["m"]}" xmlns:r="{RID}"><sheets>'
                   + ''.join(f'<sheet name="{escape(s["name"])}" sheetId="{i}" r:id="rId{i}"/>' for i, s in enumerate(sheets, 1))
                   + '</sheets></workbook>')
        z.writestr('xl/_rels/workbook.xml.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   + ''.join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
                             for i in range(1, len(sheets) + 1))
                   + f'<Relationship Id="rId{len(sheets) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
        z.writestr('xl/styles.xml', STYLES)
        for i, sheet in enumerate(sheets, 1):
            z.writestr(f'xl/worksheets/sheet{i}.xml', _sheet_xml(sheet))


def _col_index(ref):
    letters = re.match(r'[A-Z]+', ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def read_xlsx(path):
    """Return {sheet name: list of rows (lists of strings)} from any .xlsx, including Google exports."""
    with zipfile.ZipFile(path) as z:
        shared = []
        if 'xl/sharedStrings.xml' in z.namelist():
            for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', NS):
                shared.append(''.join(t.text or '' for t in si.iter(f'{{{NS["m"]}}}t')))
        wb = ET.fromstring(z.read('xl/workbook.xml'))
        rels = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        targets = {r.get('Id'): r.get('Target') for r in rels}
        out = {}
        for s in wb.find('m:sheets', NS):
            target = targets[s.get(f'{{{RID}}}id')].lstrip('/')
            target = target if target.startswith('xl/') else 'xl/' + target
            rows = []
            for row in ET.fromstring(z.read(target)).iter(f'{{{NS["m"]}}}row'):
                values = {}
                for c in row.findall('m:c', NS):
                    kind, v = c.get('t'), c.find('m:v', NS)
                    if kind == 's':
                        text = shared[int(v.text)] if v is not None else ''
                    elif kind == 'inlineStr':
                        text = ''.join(t.text or '' for t in c.iter(f'{{{NS["m"]}}}t'))
                    else:
                        text = v.text if v is not None else ''
                    values[_col_index(c.get('r'))] = text
                index = int(row.get('r')) - 1
                while len(rows) < index:
                    rows.append([])
                rows.append([values.get(i, '') for i in range(max(values) + 1)] if values else [])
            while rows and not any(cell.strip() for cell in rows[-1]):
                rows.pop()
            out[s.get('name')] = rows
    return out


class Drive:
    """Minimal rclone wrapper scoped to one Drive folder ID."""

    def __init__(self, remote, folder_id):
        self.remote, self.folder = remote, folder_id

    def _run(self, *args):
        result = subprocess.run(['rclone', *args, '--drive-root-folder-id', self.folder], capture_output=True, text=True)
        errors = [l for l in result.stderr.splitlines() if 'ERROR' in l]
        if result.returncode or errors:
            raise RuntimeError('\n'.join(errors) or result.stderr[-500:])
        return result.stdout

    def list(self):
        return json.loads(self._run('lsjson', f'{self.remote}:', '--drive-export-formats', 'xlsx'))

    def download_sheet(self, name, dest):
        self._run('copyto', f'{self.remote}:{name}.xlsx', str(dest), '--drive-export-formats', 'xlsx')

    def upload_sheet(self, local, name):
        """Create or update the Google Sheet `name` from a local .xlsx (same file ID when it exists)."""
        self._run('copyto', str(local), f'{self.remote}:{name}.xlsx',
                  '--drive-import-formats', 'xlsx', '--drive-export-formats', 'xlsx')

    def upload_files(self, folder):
        self._run('copy', str(folder), f'{self.remote}:')

    def check(self, folder):
        self._run('check', str(folder), f'{self.remote}:', '--one-way')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['read'])
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    print(json.dumps(read_xlsx(args.path), ensure_ascii=False, indent=1))
