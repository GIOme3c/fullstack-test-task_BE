import json
import os
from random import randint

from database import DB_PATH, get_connection, select

JSON_DIR = "mock_data/"


def init_db():

    if os.path.exists(DB_PATH):
        return

    connection = get_connection()
    cursor = connection.cursor()


    def read_json(file_name):
        with open(JSON_DIR+file_name, 'r', encoding='utf-8') as file:
            text = file.read()
            return json.loads(text)

    def to_str(smth):
        if smth is None:
            smth = ''
        return repr(smth)

    def fill_table(tab_name):
        data = read_json(f"{tab_name}.json")
        fields = data[0].keys()

        for row in data:
            values = [to_str(x) for x in row.values()]
            cursor.execute(f"""
                insert into {tab_name}
                ({','.join(fields)})
                values
                ({','.join(values)})
            """)


    def create_relations(setting_name, products, settings):
        # products = select("select product_id from products")
        # settings = select(f"select {setting_name}_id from {setting_name}s")
        tab_size = len(settings)

        for prod_id in products:
            is_used = [0]*tab_size

            for _ in range(0,10):
                while True:
                    new_relation = randint(0, tab_size-1)
                    if not is_used[new_relation]:
                        is_used[new_relation] = True
                        cursor.execute(f"""
                            insert into products_to_{setting_name}s
                            (product_id, {setting_name}_id)
                            values
                            ({prod_id},{settings[new_relation]})
                        """)
                        break


    def create_many_to_many(setting_name):
        #PRODUCTS to <setting_name> (MtM)
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS products_to_{setting_name}s(
            {setting_name}_id INT,
            product_id INT,
            PRIMARY KEY ({setting_name}_id, product_id),
            FOREIGN KEY({setting_name}_id) REFERENCES {setting_name}s({setting_name}_id),
            FOREIGN KEY(product_id) REFERENCES products(product_id));
        """)


    #CREATE PRODUCTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products(
        product_id INT PRIMARY KEY,
        image TEXT,
        title TEXT,
        price REAL,
        slug TEXT);
    """)

    #CREATE SIZES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sizes(
        size_id INT PRIMARY KEY,
        length INT,
        width INT,
        percent_price INT);
    """)
    
    #CREATE OPTIONS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS options(
        option_id INT PRIMARY KEY,
        title TEXT,
        price INT,
        image TEXT);
    """)
    
    #CREATE MATERIALS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materials(
        material_id INT PRIMARY KEY,
        title TEXT,
        slug TEXT,
        price INT,
        image TEXT);
    """)
    
    #CREATE BASE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bases(
        base_id INT PRIMARY KEY,
        title TEXT,
        price INT,
        image TEXT);
    """)

    #FILL TABLES
    for tab_name in ['sizes','options','materials','bases','products']:
        fill_table(tab_name)

    #CREATE RELATIONS & FILL RELATIONS
    products = [x["product_id"] for x in read_json("products.json")]
    for setting_name in ['size','option','material','base']:
        create_many_to_many(setting_name)
        sub_data = [x[setting_name+'_id'] for x in read_json(setting_name+'s.json')]
        create_relations(setting_name, products, sub_data)

    connection.commit()