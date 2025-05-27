from typing import Dict, List
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from category_tree import CategoryTree
from category_tools import CategoryChildrenTool, AllCategoriesTool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class CategoryAssignmentAgent:
    def __init__(self, category_tree: CategoryTree, api_key: str, debug: bool = False, verbose: bool = False):
        self.category_tree = category_tree
        self.llm = ChatOpenAI(model="gpt-4.1", temperature=0, api_key=api_key)
        self.debug = debug
        self.verbose = verbose
        # Create tools for the agent
        self.tools = [CategoryChildrenTool(category_tree)]

        # Create the agent
        self.agent = create_react_agent(model=self.llm, tools=self.tools, prompt=self._get_system_prompt())

    def _get_system_prompt(self) -> str:
        return """You are a category assignment agent that helps assign products to the correct category hierarchy.
Your task is to analyze the product description and assign it to the most appropriate category path by following these steps:

1. Start at the root level:
   - Get children of the root node
   - Analyze the product description
   - Choose the most appropriate top-level category
   - If not confident, stop and return partial path

2. For each subsequent level:
   - Get children of the previously selected category
   - Analyze the product description
   - Choose the most appropriate subcategory
   - If not confident, stop and return partial path

3. Continue until:
   - You reach a leaf node (no more children)
   - Or you're not confident about the next level

Guidelines:
- Always work one level at a time
- Use get_category_children to explore available options at each level
- Be precise and specific in your category assignment
- If you're not confident about a category, stop and return the path up to that point
- Provide clear reasoning for your decisions at each level

Example output format:
{
    "category_path": "Category1 > Category2 > Category3",
    "reasoning": "Step-by-step explanation of category selection process",
    "confidence": "high/medium/low",
    "is_complete": true/false,
    "steps": [
        {
            "level": 1,
            "category": "Category1",
            "reasoning": "Why this category was chosen and the other categories were not chosen",
            "confidence": "high/medium/low"
        },
        {
            "level": 2,
            "category": "Category2",
            "reasoning": "Why this category was chosen and the other categories were not chosen",
            "confidence": "high/medium/low"
        }
    ]
}"""

    def assign_category(self, product_description: str) -> Dict:
        """Assign a category to a product description."""
        # Create the input for the agent
        agent_input = {
            "messages": [
                {
                    "role": "user",
                    "content": f"""Product Description is: "{product_description}"

Please follow these steps:
1. Start by getting children of the root node
2. Choose the most appropriate top-level category
3. For each subsequent level, get children and choose the most appropriate subcategory
4. Continue until you reach a leaf node or are not confident
5. Provide reasoning for each step

Remember to:
- Work one level at a time
- Stop if you're not confident about a category
- Provide detailed reasoning for each decision""",
                }
            ]
        }

        # Run the agent
        result = self.agent.invoke(agent_input, debug=self.verbose)

        # Add product description to the result
        result["product_description"] = product_description
        return result

    async def assign_category_async(self, product_description: str) -> Dict:
        """Asynchronously assign a category to a product description."""
        # Create the input for the agent
        agent_input = {
            "messages": [
                {
                    "role": "user",
                    "content": f"""Product Description is: "{product_description}"

Please follow these steps:
1. Start by getting children of the root node
2. Choose the most appropriate top-level category
3. For each subsequent level, get children and choose the most appropriate subcategory
4. Continue until you reach a leaf node or are not confident
5. Provide reasoning for each step

Remember to:
- Work one level at a time
- Stop if you're not confident about a category
- Provide detailed reasoning for each decision""",
                }
            ]
        }

        # Run the agent asynchronously
        result = await self.agent.ainvoke(agent_input, debug=self.verbose)

        # Add product description to the result
        result["product_description"] = product_description
        return result


def main():
    # Example categories
    categories = [
        "Beverages > Fruit & Vegetable Juices > Wellness Shots",
        "Beverages > Fruit & Vegetable Juices > Other Juices",
        "Apparel & Accessories > Clothing > Underwear & Socks > Shapewear",
        "Pantry > Packaged Fruit & Applesauce > Other Packaged Fruit",
        "Sporting Goods > Athletics > Water Sports",
        "Beverages > Drink Mixes > Energy & Hydration Mixes",
        "Household Supplies > Household Cleaning Supplies > Household Cleaning Products > Dish Soap",
        "Beverages > Drink Mixes > Protein Powder",
        "Beverages > Carbonated Drinks > Cola > Zero Sugar Cola",
        "Beverages > Soft Drinks > Cola > Zero Sugar Cola",
        "Pantry > Packaged Seafood > Other Packaged Seafood",
    ]

    # Create and populate the category tree
    tree = CategoryTree()
    for category in categories:
        tree.add_category_path(category)

    # Create the category assignment agent
    agent = CategoryAssignmentAgent(tree, os.getenv("OPENAI_API_KEY"))  # , verbose=True)

    # Example product description
    # product_description = "sourdough bread"
    product_description = "Coca-Cola Cola Original Taste Soda Pop - 6 pack"

    # Get category assignment
    result = agent.assign_category(product_description)
    print("\nCategory Assignment Result:")
    print("-" * 100)
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
