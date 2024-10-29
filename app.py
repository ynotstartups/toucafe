from chalice import Chalice, Response
from base64 import b64encode

app = Chalice(app_name="helloworld")
app.debug = True


def to_id(title: str) -> str:
    return b64encode(title.encode("utf-8")).decode("utf-8")


def recipe_to_html(recipe) -> str:
    tags_lis_html = "".join(
        [
            f"<li><a href='/api/tag/{to_id(tag)}'>{tag}</a></li>"
            for tag in recipe.get("tags", [])
        ]
    )
    ingredients_lis_html = "".join(
        [f"<li>{i}</li>" for i in recipe.get("ingredients", [])]
    )
    instructions_lis_html = "".join(
        [f"<li>{i}</li>" for i in recipe.get("instructions", [])]
    )
    webpage_body = f"""
        <body>
            <h1>{recipe["title"]}</h1>
            <h2>Tags</h2>
            <ul>
                {tags_lis_html}
            </ul>
            <h2>Ingredients</h2>
            <ul>
                {ingredients_lis_html}
            </ul>
            <h2>Instructions</h2>
            <ul>
                {instructions_lis_html}
            </ul>
        </body>
    """
    return WEBPAGE_START + webpage_body + WEBPAGE_END


def recipes_to_html(recipes) -> str:
    recipes_lis = []
    for recipe in recipes:
        title = recipe["title"]
        link = f"/api/recipe/{to_id(recipe['title'])}"
        recipes_lis.append(f"<li><a href='{link}'>{title}</a></li>")
    recipes_lis_html = "".join(recipes_lis)
    webpage_body = f"""
        <body>
            <h1>Recipes</h1>
            <ul>
                {recipes_lis_html}
            </ul>
        </body>
    """
    return WEBPAGE_START + webpage_body + WEBPAGE_END


def recipes_to_menu_page(recipes) -> str:
    menu_html = ""

    menu_category = None
    menu_subcategory = None
    for recipe in recipes:
        # handle category logic
        last_menu_category = menu_category
        menu_category = recipe["menu_category"]
        if menu_category != last_menu_category:
            # New Category
            menu_html += f"<h1>{menu_category}</h1>"
            menu_subcategory = None

        # handle sub_category logic
        last_menu_subcategory = menu_subcategory
        menu_subcategory = recipe.get("menu_subcategory", None)
        if menu_subcategory != last_menu_subcategory:
            menu_html += f"<h2>{menu_subcategory}</h2>"

        title = recipe["title"]
        link = f"/api/recipe/{to_id(recipe['title'])}"
        # menu_html += f"<li><a href='{link}'>{title}</a></li>"
        menu_html += f"<li>{title}</li>"
    webpage_body = f"""
        <body>
            <h1>Menu</h1>
            {menu_html}
        </body>
    """
    return WEBPAGE_START + webpage_body + WEBPAGE_END


@app.route("/")
def index():
    html = recipes_to_menu_page(RECIPES)
    return response_html(html)


# TODO: implement me
@app.route("/recipe/{title_id}")
def recipe(title_id):
    for recipe in RECIPES:
        if to_id(recipe["title"]) == title_id:
            html = recipe_to_html(recipe)
            return response_html(html)


# TODO: implement me
@app.route("/tag/{tag_id}")
def tag(tag_id):
    recipes = []
    for recipe in RECIPES:
        for tag in recipe["tags"]:
            if to_id(tag) == tag_id:
                recipes.append(recipe)
    html = recipes_to_html(recipes)
    return response_html(html)


def response_html(html):
    return Response(
        html,
        status_code=200,
        headers={
            "Content-Type": "text/html",
            "Access-Control-Allow-Origin": "*",
        },
    )


WEBPAGE_START = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recipes</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                line-height: 1.6;
            }
            h1, h2 {
                color: #333;
            }
            li {
                list-style-type: none;
                padding: 0;
            }
            li::before {
                content: "• ";
                color: #FF6347;
            }
        </style>
    </head>
    """
WEBPAGE_END = "</html>"

RECIPES = [
    # 前菜
    {
        "title": "西班牙烘蛋",
        "menu_category": "前菜",
    },
    {
        "title": "韩式海鲜泡菜饼",
        "menu_category": "前菜",
    },
    {
        "title": "日式土豆泥沙拉",
        "menu_category": "前菜",
    },
    # 肉类
    {
        "title": "蜜汁叉烧",
        "menu_category": "肉类",
        "menu_subcategory": "猪",
    },
    {
        "title": "梅菜蒸肉饼",
        "menu_category": "肉类",
        "menu_subcategory": "猪",
    },
    {
        "title": "酸菜炖排骨",
        "menu_category": "肉类",
        "menu_subcategory": "猪",
    },
    {
        "title": "咕噜肉",
        "menu_category": "肉类",
        "menu_subcategory": "猪",
    },
    {
        "title": "炸猪扒",
        "menu_category": "肉类",
        "menu_subcategory": "猪",
    },
    {
        "title": "葱姜鸡",
        "menu_category": "肉类",
        "menu_subcategory": "鸡",
    },
    {
        "title": "口水鸡",
        "menu_category": "肉类",
        "menu_subcategory": "鸡",
    },
    {
        "title": "啤酒鸡",
        "menu_category": "肉类",
        "menu_subcategory": "鸡",
    },
    {
        "title": "钵钵鸡",
        "menu_category": "肉类",
        "menu_subcategory": "鸡",
    },
    {
        "title": "可乐鸡翅",
        "menu_category": "肉类",
        "menu_subcategory": "鸡",
    },
    {
        "title": "香菇蒸鸡",
        "menu_category": "肉类",
        "menu_subcategory": "鸡",
    },
    {
        "title": "炸鸡",
        "menu_category": "肉类",
        "menu_subcategory": "鸡",
    },
    {
        "title": "油封鸭",
        "menu_category": "肉类",
        "menu_subcategory": "鸭",
    },
    {
        "title": "土豆焖鸭",
        "menu_category": "肉类",
        "menu_subcategory": "鸭",
    },
    {
        "title": "酸梅鸭",
        "menu_category": "肉类",
        "menu_subcategory": "鸭",
    },
    {
        "title": "烤箱烧烤羊排",
        "menu_category": "肉类",
        "menu_subcategory": "羊",
    },
    {
        "title": "孜然羊肉",
        "menu_category": "肉类",
        "menu_subcategory": "羊",
    },
    {
        "title": "红烧牛肉",
        "menu_category": "肉类",
        "menu_subcategory": "牛",
    },
    {
        "title": "水煮牛肉",
        "menu_category": "肉类",
        "menu_subcategory": "牛",
    },
    {
        "title": "小炒黄牛肉",
        "menu_category": "肉类",
        "menu_subcategory": "牛",
    },
    {
        "title": "Slow bake beef short rib",
        "menu_category": "肉类",
        "menu_subcategory": "牛",
    },
    {
        "title": "土豆片炒肉",
        "menu_category": "肉类",
        "menu_subcategory": "Misc",
    },
    {
        "title": "煎香五花肉炒菜",
        "menu_category": "肉类",
        "menu_subcategory": "Misc",
    },
    # 海鲜类
    {
        "title": "广式蒸鱼",
        "menu_category": "海鲜类",
    },
    {
        "title": "剁椒蒸鱼柳",
        "menu_category": "海鲜类",
    },
    {
        "title": "酸菜鱼",
        "menu_category": "海鲜类",
    },
    {
        "title": "虾仁滑蛋",
        "menu_category": "海鲜类",
    },
    {
        "title": "蒜蓉扇贝",
        "menu_category": "海鲜类",
    },
    {
        "title": "爆炒花甲",
        "menu_category": "海鲜类",
    },
    # 蔬菜类
    {
        "title": "蒸茄子炒菜",
        "menu_category": "蔬菜类",
        "menu_subcategory": "蔬菜类",
    },
    {
        "title": "鱼香茄子",
        "menu_category": "蔬菜类",
        "menu_subcategory": "茄子",
    },
    {
        "title": "日式茄子",
        "menu_category": "蔬菜类",
        "menu_subcategory": "茄子",
    },
    {
        "title": "微波炉茄子",
        "menu_category": "蔬菜类",
        "menu_subcategory": "茄子",
    },
    {
        "title": "蒸水蛋",
        "menu_category": "蔬菜类",
        "menu_subcategory": "鸡蛋",
    },
    {
        "title": "茶叶蛋",
        "menu_category": "蔬菜类",
        "menu_subcategory": "鸡蛋",
    },
    {
        "title": "炸蛋",
        "menu_category": "蔬菜类",
        "menu_subcategory": "鸡蛋",
    },
    {
        "title": "番茄炒蛋",
        "menu_category": "蔬菜类",
        "menu_subcategory": "鸡蛋",
    },
    {
        "title": "韭黄炒蛋",
        "menu_category": "蔬菜类",
        "menu_subcategory": "鸡蛋",
    },
    {
        "title": "炸薯条",
        "menu_category": "蔬菜类",
        "menu_subcategory": "Misc",
    },
    {
        "title": "酸菜炒/炖粉条",
        "menu_category": "蔬菜类",
        "menu_subcategory": "Misc",
    },
    {
        "title": "酸笋炒/炖肉",
        "menu_category": "蔬菜类",
        "menu_subcategory": "Misc",
    },
    {
        "title": "干锅花菜",
        "menu_category": "蔬菜类",
        "menu_subcategory": "Misc",
    },
    {
        "title": "干锅卷心菜",
        "menu_category": "蔬菜类",
        "menu_subcategory": "Misc",
    },
    {
        "title": "腐乳通菜心",
        "menu_category": "蔬菜类",
        "menu_subcategory": "Misc",
    },
    {
        "title": "炒生菜",
        "menu_category": "蔬菜类",
        "menu_subcategory": "Misc",
    },
    {
        "title": "西班牙小辣椒",
        "menu_category": "蔬菜类",
        "menu_subcategory": "Misc",
    },
    {
        "title": "干煸豆角肉末",
        "menu_category": "蔬菜类",
        "menu_subcategory": "Misc",
    },
    {
        "title": "麻婆豆腐",
        "menu_category": "蔬菜类",
        "menu_subcategory": "Misc",
    },
    {
        "title": "老奶洋芋",
        "menu_category": "蔬菜类",
        "menu_subcategory": "Misc",
    },
    {
        "title": "steam artichoke",
        "menu_category": "蔬菜类",
        "menu_subcategory": "Misc",
    },
    # 汤类
    {
        "title": "土豆胡萝卜玉米排骨汤",
        "menu_category": "汤类",
    },
    {
        "title": "赤小豆猪肉汤",
        "menu_category": "汤类",
    },
    {
        "title": "鸡汤",
        "menu_category": "汤类",
    },
    {
        "title": "大酱汤",
        "menu_category": "汤类",
    },
    {
        "title": "关东煮",
        "menu_category": "汤类",
    },
    {
        "title": "鱼汤",
        "menu_category": "汤类",
    },
    {
        "title": "罗宋汤",
        "menu_category": "汤类",
    },
    {
        "title": "海鲜冬阴功汤",
        "menu_category": "汤类",
    },
    # 点心
    {
        "title": "葱油饼",
        "menu_category": "点心",
    },
    {
        "title": "伦教糕",
        "menu_category": "点心",
    },
    {
        "title": "萝卜糕",
        "menu_category": "点心",
    },
    {
        "title": "鸡蛋糕",
        "menu_category": "点心",
    },
    {
        "title": "鸡蛋肠粉",
        "menu_category": "点心",
    },
    {
        "title": "绿豆糕",
        "menu_category": "点心",
    },
    # 主食
    {
        "title": "日本咖喱饭",
        "menu_category": "主食",
    },
    {
        "title": "卤肉饭",
        "menu_category": "主食",
    },
    {
        "title": "韩国拌饭",
        "menu_category": "主食",
    },
    {
        "title": "炒米粉",
        "menu_category": "主食",
    },
    {
        "title": "越南粉",
        "menu_category": "主食",
    },
    {
        "title": "咖喱奶油乌冬",
        "menu_category": "主食",
    },
    {
        "title": "墨鱼汁意面",
        "menu_category": "主食",
    },
    {
        "title": "蚝粥",
        "menu_category": "主食",
    },
    {
        "title": "汉堡",
        "menu_category": "主食",
    },
    {
        "title": "比萨",
        "menu_category": "主食",
    },
    {
        "title": "手工面条",
        "menu_category": "主食",
    },
    {
        "title": "手工饺子",
        "menu_category": "主食",
    },
    {
        "title": "手工包子",
        "menu_category": "主食",
    },
    {
        "title": "日式面包",
        "menu_category": "主食",
    },
    # 甜品
    {
        "title": "苹果面包",
        "menu_category": "甜品",
    },
    {
        "title": "紫薯面包",
        "menu_category": "甜品",
    },
    {
        "title": "毛巾蛋糕卷",
        "menu_category": "甜品",
    },
    {
        "title": "草莓奶油蛋糕",
        "menu_category": "甜品",
    },
    {
        "title": "泡芙",
        "menu_category": "甜品",
    },
    {
        "title": "曲奇",
        "menu_category": "甜品",
    },
    # 饮品
    {
        "title": "冷萃咖啡",
        "menu_category": "饮品",
    },
    {
        "title": "手冲咖啡",
        "menu_category": "饮品",
    },
    {
        "title": "越南热咖啡",
        "menu_category": "饮品",
    },
    {
        "title": "热红酒",
        "menu_category": "饮品",
    },
    {
        "title": "奶盖奶茶",
        "menu_category": "饮品",
    },
    # 早餐
    {
        "title": "包子",
        "menu_category": "早餐",
    },
    {
        "title": "煎饺",
        "menu_category": "早餐",
    },
    {
        "title": "炒粉",
        "menu_category": "早餐",
    },
    {
        "title": "英式玛芬",
        "menu_category": "早餐",
    },
    {
        "title": "拌面",
        "menu_category": "早餐",
    },
    {
        "title": "麦当劳早餐",
        "menu_category": "早餐",
    },
    {
        "title": "土豆饼",
        "menu_category": "早餐",
    },
    {
        "title": "珍珠鸡",
        "menu_category": "早餐",
    },
    {
        "title": "方便面",
        "menu_category": "早餐",
    },
    {
        "title": "小米粥",
        "menu_category": "早餐",
    },
    {
        "title": "北非蛋",
        "menu_category": "早餐",
    },
    {
        "title": "牛油果三文鱼面包",
        "menu_category": "早餐",
    },
    {
        "title": "金枪鱼玉米法棍",
        "menu_category": "早餐",
    },
    {
        "title": "冬阴功炒粉",
        "menu_category": "早餐",
    },
]
