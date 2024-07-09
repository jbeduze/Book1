import asyncio
from typing import List, Dict

class StoryBook:
    def __init__(self, title: str):
        self.title = title
        self.outline = None
        self.character_descriptions = []

    async def generate_outline(self) -> None:
        # Simulate an asynchronous operation, such as fetching data or processing
        await asyncio.sleep(2)  # Simulating a delay
        self.outline = f"Outline of the story: {self.title}"
        print(f"Outline generated: {self.outline}")

    async def generate_character_description(self, character_name: str) -> None:
        # Simulate an asynchronous operation, such as fetching data or processing
        await asyncio.sleep(2)  # Simulating a delay
        description = f"Description of character: {character_name}"
        self.character_descriptions.append(description)
        print(f"Character description generated: {description}")

    async def generate_story_details(self, character_names: List[str]) -> None:
        await self.generate_outline()
        await asyncio.gather(*(self.generate_character_description(name) for name in character_names))

# Example usage
async def main():
    story_book = StoryBook("The Adventure of Async")
    character_names = ["Alice", "Bob", "Charlie"]
    await story_book.generate_story_details(character_names)

# Running the example
asyncio.run(main())
