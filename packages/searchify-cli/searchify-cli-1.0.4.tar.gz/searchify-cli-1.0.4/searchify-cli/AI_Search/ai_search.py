import argparse
import os
from dotenv import load_dotenv
import google.generativeai as palm
from textwrap import wrap
from pathlib import Path


def load_environment_variables(env_file_path):
    """Load environment variables from the specified .env file."""
    load_dotenv(env_file_path)


def configure_api():
    """Configure API with the API key loaded from environment variables."""
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY not found in .env file")
    palm.configure(api_key=api_key)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate text based on a prompt.")
    parser.add_argument("prompt", type=str, help="The prompt for text generation")
    parser.add_argument(
        "--temp",
        type=float,
        default=0,
        help="The temperature for text generation (default: 0.5)",
    )
    parser.add_argument(
        "--max_output_tokens",
        type=int,
        default=250,
        help="The maximum number of output tokens (default: 800)",
    )
    parser.add_argument(
        "--top_k", type=int, default=1, help="Top-k sampling parameter (default: 1)"
    )
    parser.add_argument(
        "--top_p",
        type=float,
        default=0.1,
        help="Top-p sampling parameter (default: 0.1)",
    )
    parser.add_argument(
        "--page", action="store_true", help="Paginate the output (default: False)"
    )
    return parser.parse_args()


def generate_text(model, prompt, temperature, max_output_tokens, top_k, top_p):
    """Generate text based on the given prompt and parameters."""
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        top_k=top_k,
        top_p=top_p,
    )
    return completion.result


def paginate_text(text):
    """Paginate the text into rows."""
    words = text.split()
    rows = wrap(" ".join(words), width=60)
    return rows


def main():
    # Load environment variables from the specified .env file
    env_file_path = Path.home()/ ".env"
    load_environment_variables(env_file_path)

    # Configure API with the API key loaded from environment variables
    configure_api()

    # Parse command line arguments
    args = parse_arguments()

    # Generate text based on the given prompt and parameters
    generated_text = generate_text(
        model="models/text-bison-001",
        prompt=args.prompt,
        temperature=args.temp,
        max_output_tokens=args.max_output_tokens,
        top_k=args.top_k,
        top_p=args.top_p,
    )

    if args.page:
        # Paginate the generated text
        paginated_text = paginate_text(generated_text)
        for row in paginated_text:
            print(row)
    else:
        # Print the entire text at once
        print(generated_text)


if __name__ == "__main__":
    main()
