import database

def add_order(data):
    ...

def get_products():
    raw_products = database.select("""
    select product_id, image, title, price, slug 
    from products""")
    
    response = []
    for row in raw_products:
        response.append({
            "product_id":row[0],
            "image":row[1],
            "title":row[2],
            "price":row[3],
            "slug":row[4],
        })
    
    return response


def get_product(product_id):

    def generate_subdata(setting_name, fields):
        sub_data = database.select(f"""
        select products_to_{setting_name}s.{','.join(fields)}
        from products_to_{setting_name}s
        join {setting_name}s on {setting_name}s.{setting_name}_id = products_to_{setting_name}s.{setting_name}_id
        where product_id = {repr(product_id)}""")

        response = []
        for row in sub_data:
            response.append({
                field:row[idx] for idx, field in enumerate(fields)
            })
        
        return response


    product_data = database.select(f"""
    select product_id, image, title, price, slug 
    from products
    where product_id = {repr(product_id)}""")[0]

    product_json = {
        'product_id':product_data[0],
        'image':product_data[1],
        'title':product_data[2],
        'price':product_data[3],
        'slug':product_data[4],
        'sizes':generate_subdata('size',["size_id","length","width","percent_price"]),
        'options':generate_subdata('option',["option_id","title","price","image"]),
        'materials':generate_subdata('material',["material_id","title","slug","price","image"]),
        'bases':generate_subdata('base',["base_id","title","price","image"]),
    }

    return product_json