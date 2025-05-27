from typing import List, Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from category_tree import CategoryTree


class CategoryChildrenInput(BaseModel):
    category_path: str = Field(
        ..., description="The category path to get children for. Use 'root' for top-level categories."
    )


class CategoryChildrenTool(BaseTool):
    name: str = "get_category_children"
    description: str = "Get all children of a given category path. Use 'root' to get top-level categories."
    args_schema: Type[BaseModel] = CategoryChildrenInput
    category_tree: CategoryTree

    def __init__(self, category_tree: CategoryTree):
        """Initialize the tool.

        Args:
            category_tree: The category tree to use for lookups
        """
        super().__init__(category_tree=category_tree)

    def _run(self, category_path: str) -> List[str]:
        """Get all children of a given category path.

        Args:
            category_path: The category path to get children for. Use 'root' for top-level categories.

        Returns:
            List of child category paths
        """
        if category_path == "root":
            # Get all top-level categories
            category = self.category_tree.root.get_children()
        else:
            category = self.category_tree.get_children(category_path)

        return category


class AllCategoriesTool(BaseTool):
    name: str = "get_all_categories"
    description: str = "Get all possible category paths in the tree."
    category_tree: CategoryTree

    def __init__(self, category_tree: CategoryTree):
        """Initialize the tool.

        Args:
            category_tree: The category tree to use for lookups
        """
        super().__init__(category_tree=category_tree)

    def _run(self) -> List[str]:
        """Get all possible category paths in the tree.

        Returns:
            List of all category paths
        """
        return self.category_tree.get_all_categories()


def test_tools():
    """Test the category tools with sample data."""
    # Create a sample category tree
    tree = CategoryTree()
    sample_categories = [
        "Beverages > Fruit & Vegetable Juices > Wellness Shots",
        "Beverages > Fruit & Vegetable Juices > Other Juices",
        "Apparel & Accessories > Clothing > Underwear & Socks",
        "Pantry > Packaged Fruit & Applesauce",
    ]

    for category in sample_categories:
        tree.add_category_path(category)

    # Test CategoryChildrenTool
    children_tool = CategoryChildrenTool(tree)

    # Test root level categories
    root_categories = children_tool._run("root")
    print("Root level categories:", root_categories)
    assert len(root_categories) == 3, "Should have 3 root categories"

    # Test getting children of a specific category
    beverage_children = children_tool._run("Beverages")
    print("Beverages children:", beverage_children)
    assert len(beverage_children) == 1, "Should have 1 child category for Beverages"

    # Test AllCategoriesTool
    all_categories_tool = AllCategoriesTool(tree)
    all_categories = all_categories_tool._run()
    print("All categories:", all_categories)
    assert len(all_categories) == 4, "Should have 4 total categories"

    print("All tests passed successfully!")


if __name__ == "__main__":
    test_tools()
