# ms_utils

Build Package
-
>`python -m build `
Upload Package

> `python -m twine upload --repository pypi dist/*`


## View utils keys

- ### Generic list:
  - #### not_paginate (optional): Return model elements array if this key is True, otherwise return a "_PaginationSchema_" object
  - #### authenticated_user_only (optional): Return "_get_filter_" method for "_g.user['id']_" only if this key is True, otherwise return a regular "_get_filter_"
  - #### page (optional): specify page number, default = 1
  - #### per_page (optional): specify page elements, default = 10
