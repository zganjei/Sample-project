# -*- coding: utf-8 -*-
import json

try:
    from django.utils.datastructures import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict




class Cell(object):
    def __init__(self, name, value, width, aggregation):
        self.value = value
        self.width = width
        self.name = name
        self.aggregation = aggregation


class Row(object):
    def __init__(self):
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)

    def create_cell(self, name, value, width, aggregation):
        self.add_cell(Cell(name, value, width, aggregation))

    def get_cells_dict(self):
        cells_dict = OrderedDict()
        for cell in self.cells:
            cells_dict[cell.name] = cell.value
        return cells_dict

    def __iter__(self):
        return iter(self.cells)


class Header(object):
    def __init__(self):
        self.cells = []
        self.sums = []

    def add_cell(self, cell):
        self.cells.append(cell)

    def create_cell(self, name, value, width, aggregation):
        self.add_cell(Cell(name, value, width, aggregation))
        self.sums.append(0)

    def aggregate(self, row):
        i = 0
        for cell in row:
            if cell.aggregation:
                self.sums[i] += int(cell.value)
            i += 1

    def __iter__(self):
        return iter(self.cells)


class Table(object):
    def __init__(self):
        self.header = None
        self.rows = []

    def set_header(self, header):
        self.header = header

    def add_row(self, row):
        self.rows.append(row)
        self.header.aggregate(row)

    def get_dgrid_json(self, total_page, current_page, all_data_count, aggregation=False):
        json_dict = OrderedDict({
            "total": total_page,
            "page": current_page,
            "recordsTotal": all_data_count,
            "recordsFiltered": all_data_count
        })
        json_rows = []
        for row in self.rows:
            row_fields = row.get_cells_dict()
            row_fields.update({'DT_RowId': row_fields.get('id')})
            json_rows.append(row_fields)
        json_dict['data'] = json_rows

        footer_row = {}
        i = 0
        for cell in self.header:
            footer_row[cell.name] = self.header.sums[i]
            i += 1
        footer_row.update({self.header.cells[1].name: u"مجموع:"})

        if aggregation:
            json_dict["userdata"] = footer_row

        res = json.dumps(json_dict)

        return res

    def __iter__(self):
        return iter(self.rows)
