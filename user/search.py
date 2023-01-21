

def search_fields(query_param):
    if query_param is not None:
        if query_param == 'folder':
            return ['name']
        elif query_param == 'question_sheet':
            return ['questionSheets__name']
    else:
        return ['name', 'questionSheets__name']
