import flask
import sqlalchemy
from datetime import date, datetime


def render_top_marketplace_bar(template_url, **kwargs):
    """
    Provides an easy way for routing functions to pass the variables required for
    rendering the marketplace's top bar to render_template.  Basically chains
    some other arguments on to the render call.

    Arguments:
        template_url: The url which is being rendered.
        **kwargs: The variables which are used to render the rest of the page.

    Returns:
        The result of render_template(): Whatever magic Flask does to render the
                                         final page.
    """
    query = sqlalchemy.sql.select(["cat_title"]).select_from(sqlalchemy.text("marketplace_categories"))
    result = flask.g.db.execute(query)
    categories = []
    for column in result:
        categories.append(column[0])
    return flask.render_template(template_url, cats=categories, **kwargs)


def get_marketplace_items_list_data(fields=None, attrs={}):
    """
    Queries the database and returns list of member data constrained by the 
    specified attributes.

    Arguments:
        fields: The fields to return. If None specified, then default_fields
                are used.
        attrs:  The attributes of the members to filter for.
    Returns:
        result: The fields and corresponding values of members with desired
                attributes. In the form of a list of dicts with key:value of 
                columnname:columnvalue.
    """
    all_returnable_fields = ["item_id", "cat_id", "user_id", "item_title", "item_details",
                             "item_condition", "item_price", "item_timestamp", "item_active",
                             "textbook_id", "textbook_edition", "textbook_isbn"]
    default_fields = all_returnable_fields
    if fields == None:
        fields = default_fields
    else:
        if any(f not in all_returnable_fields for f in fields):
            return "Invalid field"

    # Build the SELECT and FROM clauses
    s = sqlalchemy.sql.select(fields).select_from(sqlalchemy.text("marketplace_items"))
    
    # Build the WHERE clause 
    for key, value in attrs.items():
        s = s.where(sqlalchemy.text(key + "= :" + key))

    # Execute the query
    result = flask.g.db.execute(s, attrs).fetchall()
    sanitized_res = []

    for res in result:
        temp_row = []
        for data in res:
            print(type(data))
            if isinstance(data, (datetime, date)):
                temp_row.append(data.isoformat())
            else:
                try:
                    temp_row.append(float(data))
                except:
                    temp_row.append(data)
        sanitized_res.append(temp_row)
    
    # Return the row in the form of a of dict
    result = [{ f:t for f,t in zip(fields, res) } for res in sanitized_res]
 
    return result
