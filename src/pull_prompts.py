"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from datetime import date
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def extract_system_and_user_prompts(prompt) -> tuple[str, str]:
    """
    Extrai o system_prompt e o user_prompt de um template do LangChain.

    Suporta:
    - ChatPromptTemplate (messages como MessagePromptTemplate ou tuplas)
    - PromptTemplate simples (sem role)
    """
    system_prompt = ""
    user_prompt = ""

    if isinstance(prompt, ChatPromptTemplate):
        for msg in prompt.messages:
            role = None
            template = ""

            # MessagePromptTemplate (ex: SystemMessagePromptTemplate)
            if hasattr(msg, "prompt") and hasattr(msg.prompt, "template"):
                template = msg.prompt.template
            elif hasattr(msg, "content"):
                template = msg.content

            if isinstance(msg, SystemMessagePromptTemplate):
                role = "system"
            elif isinstance(msg, HumanMessagePromptTemplate):
                role = "human"

            # Mensagens em formato de tupla: ("system", "...")
            if role is None and isinstance(msg, (tuple, list)) and len(msg) == 2:
                role, template = msg[0], msg[1]

            if role == "system":
                system_prompt = template
            elif role == "human":
                user_prompt = template

    elif isinstance(prompt, PromptTemplate):
        system_prompt = prompt.template

    return system_prompt, user_prompt


def convert_prompt_to_dict(prompt, handle: str) -> dict:
    """
    Converte o objeto retornado pelo hub.pull para o formato YAML customizado
    usado pelo projeto (ver prompts/bug_to_user_story_v1.yml).
    """
    prompt_name = handle.split("/")[-1]
    system_prompt, user_prompt = extract_system_and_user_prompts(prompt)

    metadata = getattr(prompt, "metadata", None) or {}
    description = metadata.get("description", "") or (
        "Prompt para converter relatos de bugs em User Stories"
    )

    tags = metadata.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]
    tags = [t for t in tags if t] or ["bug-analysis", "user-story", "product-management"]

    return {
        prompt_name: {
            "description": description,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "version": "v1",
            "created_at": date.today().isoformat(),
            "tags": tags,
        }
    }


def pull_prompts_from_langsmith() -> dict:
    """Faz pull do prompt inicial do LangSmith Prompt Hub e retorna como dict."""
    handle = os.getenv("V1_PROMPT_HANDLE", "leonanluppi/bug_to_user_story_v1")

    print(f"Puxando prompt do LangSmith Hub: {handle}")
    prompt = hub.pull(handle)
    print("✓ Prompt carregado com sucesso")

    data = convert_prompt_to_dict(prompt, handle)
    return data


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH PROMPT HUB")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        print("Configure a LANGSMITH_API_KEY no .env antes de continuar.")
        return 1

    output_path = os.getenv("V1_OUTPUT_PATH", "prompts/bug_to_user_story_v1.yml")

    try:
        data = pull_prompts_from_langsmith()
    except Exception as e:
        print(f"❌ Erro ao fazer pull do prompt: {e}")
        return 1

    if not data:
        print("❌ Nenhum dado obtido do LangSmith Prompt Hub.")
        return 1

    if save_yaml(data, output_path):
        print(f"\n✓ Prompt salvo localmente em {output_path}")
        return 0

    print("❌ Falha ao salvar o prompt localmente.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
