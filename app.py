from chalice import Chalice, Response

app = Chalice(app_name="helloworld")
app.debug = True


def to_id(title: str) -> str:
    return title.replace(" ", "_").lower()


# def recipe_to_title_and_link(recipe) -> dict[str, str]:
#     return {
#         "title": recipe["title"],
#         "link": f"/api/recipe/{to_id(recipe['title'])}",
#     }


def recipe_to_html(recipe) -> str:
    # TODO a link to tag
    tags_lis_html = "".join(
        [
            f"<li><a href='/api/tag/{to_id(tag)}'>{tag}</a></li>"
            for tag in recipe["tags"]
        ]
    )
    ingredients_lis_html = "".join([f"<li>{i}</li>" for i in recipe["ingredients"]])
    instructions_lis_html = "".join([f"<li>{i}</li>" for i in recipe["instructions"]])
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


@app.route("/")
def index():
    html = recipes_to_html(RECIPES)
    return response_html(html)


@app.route("/recipe/{title_id}")
def recipe(title_id):
    for recipe in RECIPES:
        if to_id(recipe["title"]) == title_id:
            html = recipe_to_html(recipe)
            return response_html(html)


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
            ul {
                list-style-type: none;
                padding: 0;
            }
            ul li::before {
                content: "• ";
                color: #FF6347;
            }
        </style>
    </head>
    """
WEBPAGE_END = "</html>"

RECIPES = [
    {
        "title": "Spaghetti Carbonara",
        "tags": ["Italian", "Pasta", "Quick", "Dinner"],
        "ingredients": [
            "200g spaghetti",
            "100g pancetta",
            "2 large eggs",
            "50g grated Parmesan",
            "Salt",
            "Pepper",
        ],
        "instructions": [
            "Boil spaghetti in salted water according to package instructions.",
            "In a pan, cook pancetta until crisp.",
            "Whisk eggs and Parmesan together in a bowl.",
            "Drain spaghetti and combine with pancetta.",
            "Remove from heat, add egg mixture, and stir quickly.",
            "Season with salt and pepper, serve immediately.",
        ],
    },
    {
        "title": "Chicken Stir-Fry",
        "tags": ["Asian", "Quick", "Healthy", "Gluten-Free"],
        "ingredients": [
            "1 lb chicken breast, sliced",
            "1 bell pepper, sliced",
            "1 onion, sliced",
            "2 cups broccoli florets",
            "2 tbsp soy sauce",
            "1 tbsp olive oil",
            "1 clove garlic, minced",
        ],
        "instructions": [
            "Heat oil in a pan, add garlic and cook until fragrant.",
            "Add chicken and cook until browned.",
            "Add bell pepper, onion, and broccoli; stir-fry until vegetables are tender.",
            "Add soy sauce and stir to coat evenly.",
            "Serve hot.",
        ],
    },
    {
        "title": "Vegetable Soup",
        "tags": ["Vegan", "Healthy", "Gluten-Free", "Soup"],
        "ingredients": [
            "1 tbsp olive oil",
            "1 onion, diced",
            "2 carrots, diced",
            "2 celery stalks, diced",
            "3 cups vegetable broth",
            "1 can diced tomatoes",
            "1 cup green beans",
            "Salt and pepper",
        ],
        "instructions": [
            "Heat oil in a pot and add onion, carrots, and celery; cook until softened.",
            "Add broth, tomatoes, and green beans; bring to a boil.",
            "Simmer for 20 minutes until vegetables are tender.",
            "Season with salt and pepper and serve hot.",
        ],
    },
    {
        "title": "Pancakes",
        "tags": ["Breakfast", "Sweet", "Quick", "Vegetarian"],
        "ingredients": [
            "1 cup flour",
            "1 tbsp sugar",
            "1 tsp baking powder",
            "1/2 tsp salt",
            "3/4 cup milk",
            "1 egg",
            "2 tbsp melted butter",
        ],
        "instructions": [
            "Mix flour, sugar, baking powder, and salt in a bowl.",
            "In another bowl, whisk milk, egg, and melted butter.",
            "Combine wet and dry ingredients until smooth.",
            "Pour batter onto a hot griddle and cook until bubbles form, then flip.",
            "Serve warm with syrup or toppings of choice.",
        ],
    },
    {
        "title": "Avocado Toast",
        "tags": ["Breakfast", "Quick", "Vegetarian", "Healthy"],
        "ingredients": [
            "1 ripe avocado",
            "2 slices of bread",
            "Salt",
            "Pepper",
            "Red chili flakes",
        ],
        "instructions": [
            "Toast the bread slices to your liking.",
            "Mash avocado in a bowl, and season with salt and pepper.",
            "Spread avocado on toast and sprinkle with red chili flakes.",
            "Serve immediately.",
        ],
    },
    {
        "title": "Chocolate Chip Cookies",
        "tags": ["Dessert", "Baking", "Sweet", "Vegetarian"],
        "ingredients": [
            "1 cup butter, softened",
            "1 cup sugar",
            "1 cup brown sugar",
            "2 eggs",
            "2 tsp vanilla extract",
            "3 cups flour",
            "1 tsp baking soda",
            "1/2 tsp salt",
            "2 cups chocolate chips",
        ],
        "instructions": [
            "Preheat oven to 350°F (175°C).",
            "Cream butter and sugars together.",
            "Add eggs and vanilla, mix well.",
            "Add flour, baking soda, and salt, mix until combined.",
            "Fold in chocolate chips.",
            "Drop spoonfuls of dough onto baking sheet and bake for 10-12 minutes.",
            "Cool on a wire rack.",
        ],
    },
    {
        "title": "Grilled Cheese Sandwich",
        "tags": ["Lunch", "Quick", "Comfort Food", "Vegetarian"],
        "ingredients": ["2 slices of bread", "2 slices of cheese", "1 tbsp butter"],
        "instructions": [
            "Butter one side of each bread slice.",
            "Place cheese between the unbuttered sides of the bread.",
            "Cook in a skillet over medium heat until golden on both sides and cheese is melted.",
            "Serve warm.",
        ],
    },
    {
        "title": "Caesar Salad",
        "tags": ["Salad", "Healthy", "Lunch", "Gluten-Free"],
        "ingredients": [
            "1 head of romaine lettuce, chopped",
            "1/4 cup grated Parmesan",
            "1/2 cup croutons",
            "Caesar dressing to taste",
        ],
        "instructions": [
            "In a large bowl, combine lettuce, Parmesan, and croutons.",
            "Drizzle with Caesar dressing and toss to coat.",
            "Serve chilled.",
        ],
    },
    {
        "title": "Banana Smoothie",
        "tags": ["Drink", "Healthy", "Quick", "Vegan"],
        "ingredients": [
            "1 banana",
            "1 cup almond milk",
            "1 tbsp peanut butter",
            "1 tsp honey (optional)",
        ],
        "instructions": [
            "Combine all ingredients in a blender.",
            "Blend until smooth.",
            "Pour into a glass and serve immediately.",
        ],
    },
    {
        "title": "Tacos",
        "tags": ["Mexican", "Quick", "Dinner", "Gluten-Free"],
        "ingredients": [
            "8 small corn tortillas",
            "1 lb ground beef or turkey",
            "1 packet taco seasoning",
            "1 cup shredded lettuce",
            "1/2 cup diced tomatoes",
            "1/2 cup shredded cheese",
        ],
        "instructions": [
            "Cook ground meat in a pan over medium heat, add taco seasoning according to packet instructions.",
            "Warm tortillas in a separate pan.",
            "Assemble tacos with meat, lettuce, tomatoes, and cheese.",
            "Serve immediately.",
        ],
    },
]
