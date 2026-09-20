"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_FILE = "prompts/bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        system_prompt = prompt_data.get("system_prompt", "")
        user_prompt = prompt_data.get("user_prompt", "")

        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", user_prompt),
            ]
        )

        # Metadados do prompt (técnicas aplicadas, descrição, versão)
        prompt_template.metadata = {
            "description": prompt_data.get("description", ""),
            "version": prompt_data.get("version", "v2"),
            "techniques_applied": prompt_data.get("techniques_applied", []),
        }

        url = hub.push(
            prompt_name,
            prompt_template,
            new_repo_is_public=True,
            new_repo_description=prompt_data.get("description", ""),
            tags=prompt_data.get("tags", []),
        )

        print(f"✓ Prompt publicado com sucesso!")
        print(f"🔗 URL: {url}")
        return True

    except Exception as e:
        print(f"❌ Erro ao fazer push do prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    required_fields = ["description", "system_prompt", "version"]
    for field in required_fields:
        if field not in prompt_data:
            errors.append(f"Campo obrigatório faltando: {field}")

    system_prompt = prompt_data.get("system_prompt", "").strip()
    if not system_prompt:
        errors.append("system_prompt está vazio")

    user_prompt = prompt_data.get("user_prompt", "").strip()
    if not user_prompt:
        errors.append("user_prompt está vazio")

    if "[TODO]" in system_prompt or "[TODO]" in user_prompt:
        errors.append("prompt ainda contém TODOs")

    techniques = prompt_data.get("techniques_applied", [])
    if len(techniques) < 2:
        errors.append(f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)}")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS OTIMIZADOS PARA O LANGSMITH")

    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        print("Configure LANGSMITH_API_KEY e USERNAME_LANGSMITH_HUB no .env.")
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB", "").strip()

    data = load_yaml(PROMPT_FILE)
    if not data:
        print(f"❌ Não foi possível carregar {PROMPT_FILE}")
        return 1

    # O YAML pode ter uma chave raiz (ex: bug_to_user_story_v2:)
    prompt_data = data.get(PROMPT_KEY, data)

    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Prompt inválido:")
        for err in errors:
            print(f"   - {err}")
        return 1

    print(f"✓ Prompt validado com sucesso")

    prompt_name = f"{username}/{PROMPT_KEY}"
    print(f"Publicando prompt: {prompt_name}")

    if push_prompt_to_langsmith(prompt_name, prompt_data):
        print("\n✓ Push concluído. Verifique no dashboard:")
        print("  https://smith.langchain.com/prompts")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
