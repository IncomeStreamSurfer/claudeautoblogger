import os
from dotenv import load_dotenv
import anthropic

# Load variables from .env file
load_dotenv()

# Get variables from environment
brand_name = os.getenv("BRAND_NAME")
keywords_file_path = os.getenv("KEYWORDS_FILE_PATH")
sample_article_file_path = os.getenv("SAMPLE_ARTICLE_FILE_PATH")
custom_collections_file_path = os.getenv("CUSTOM_COLLECTIONS_FILE_PATH")
pages_file_path = os.getenv("PAGES_FILE_PATH")
products_file_path = os.getenv("PRODUCTS_FILE_PATH")
blogs_file_path = os.getenv("BLOGS_FILE_PATH")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Read the contents of the files
with open(keywords_file_path, "r", encoding="utf-8") as file:
    keywords = file.read().splitlines()

with open(sample_article_file_path, "r", encoding="utf-8") as file:
    sample_article = file.read()

with open(custom_collections_file_path, "r", encoding="utf-8") as file:
    custom_collections = file.read()

with open(pages_file_path, "r", encoding="utf-8") as file:
    pages = file.read()

with open(products_file_path, "r", encoding="utf-8") as file:
    products = file.read()

with open(blogs_file_path, "r", encoding="utf-8") as file:
    blogs = file.read()

def generate_article(system_prompt, user_prompt, api_key):
    client = anthropic.Client(api_key=api_key)
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )
    print("API Response:")
    print(response)
    return "".join(content.text for content in response.content)

# Iterate over each keyword and generate an article
for i, keyword in enumerate(keywords, start=1):
    # Prepare the system prompt
    system_prompt = f"""
    It must be at least 4 pages of content. Do not invent any links. You can write an article, just write generally and don't make any claims. Write a fully formatted article with tables, embeds, and much more. Write in as much detial as possible without repeating the same thing over and over. You are writing for {brand_name}. When writing for them, I want you to ensure to use this html embed with the collection ID of relevant collections to the article.

    <div class="hura-collection-embedder" data-id="296336228548" data-view="gridview" data-limit="6" data-price="1" data-label="1" data-hover="1" data-border="1" data-sh="1" data-coldk="4" data-coltl="1" data-colmb="1" ></div>

    You can change the data limit to 12 if you're doing less collections for an article.

    I have included other important pages underneath the collections. Throughout the article you're writing, please use relative internal links using the handle from this list:

    When writing the articles, "{brand_name} CANNOT make a structured function claim" - We cannot talk about any of the pharmalogical profiles that would cause "Both can improve your well-being and comfort." - We cannot make medical claims such as "helps with sleep". Make sure to follow FDA's laws and remove any structured function claims or specific medical benefit claims.

    Custom Collections:
    {custom_collections}

    Pages:
    {pages}

    Products:
    {products}

    Blogs:
    {blogs}

    Sample Article:
    {sample_article}
    """

    # Prepare the user prompt
    user_prompt = f"""
    Write a 1500 word article. Write 20 titles and 2 paragraphs per title, with formatting like tables, embeds, internal links and lists. Do not use any placeholder information. Make the content about the company - do not invent links, use at least 3 embeds and 4 collection internal links per article. Please generate an article about the keyword "{keyword}" based on the following information: Please be creative when writing. Focus on writing good e-magazine style selling content but from the perspective of the business. I have these products - I'm writing for {brand_name}. These are all products they sell, and collections of products they sell. I want you, by embedding images, to make a rankable SEO-Optimized listicle article about the keyword. You should use a lot of tables and other formatting. Do not use complicated language, you're writing for working class workers. Please use Sentence case. This is vital. Don't use crazy language, but give a lot of interesting formatting and make it like a journal style advertising the specific products. In the article, please embed some of these collections. I have included the collections in the prompt as well. Please use headers such as # h1 on the top header and then ## h2 and h3 ### throughout the article and be considerate about where you place both the collection embeds and the collection links, and that you use appropriate SEO-Optimized anchor text for internal links. Don't be repetitive. When writing the articles - GPT needs to filter/say "{brand_name} CANNOT make a structured function claim" - We cannot talk about any of the pharmalogical profiles than would cause "Both can improve your well-being and comfort." - We cannot make medical claims such as "helps with sleep". Make sure to follow FDA's laws and remove any structured function claims or specific medical benefit.
    """

    # Generate the article
    article = generate_article(system_prompt, user_prompt, anthropic_api_key)

    # Save the generated article to a file
    with open(f"generated_article_{i}.txt", "w", encoding="utf-8") as file:
        file.write(f"# {keyword}\n\n")
        file.write(article)

    print(f"Article {i} generated for keyword: {keyword}. Saved to generated_article_{i}.txt.")
