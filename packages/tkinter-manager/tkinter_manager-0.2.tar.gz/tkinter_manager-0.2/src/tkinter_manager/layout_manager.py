class LayoutManager(object):
    def __init__(self, root):
        self.root = root

    def centre_elements(self, elements):
        self.root.grid_columnconfigure(0,weight=1)
        i = 0
        for name, element in elements.items():
            # no padding between labels and their respective elements
            pady = (0, 5)
            if 'label' in name:
                pady = (5, 0)
                
            element.element_object.grid(row=i, column=0, sticky="ew", padx=10, pady=pady)
            self.root.grid_rowconfigure(i ,weight=1)

            i += 1

    def set_layout(self, layout_schema, elements_dict):
        for row_i, row in enumerate(layout_schema):
            for column_i, value in enumerate(row):
                if value:
                    element = elements_dict[value]
                    element.element_object.grid(row=row_i, column=column_i, sticky="N", padx=1)

                self.root.grid_columnconfigure(column_i,weight=1)
            self.root.grid_rowconfigure(row_i,weight=1)

    @staticmethod
    def _return_max_row_length(input_list):
        max_length = 0
        for row in input_list:
            row_length = len(row)
            if row_length > max_length:
                max_length = row_length
        return max_length