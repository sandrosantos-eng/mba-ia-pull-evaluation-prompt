"""
Testes automatizados para validação de prompts.
"""
import json
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

V2_PATH = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


@pytest.fixture
def prompt_data():
    """Carrega os dados do prompt otimizado (v2)."""
    data = load_prompts(V2_PATH)
    # O YAML tem uma chave raiz (ex: bug_to_user_story_v2:)
    return data.get("bug_to_user_story_v2", data)


class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt_data):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in prompt_data, "campo system_prompt ausente"
        assert prompt_data["system_prompt"].strip(), "system_prompt está vazio"

    def test_prompt_has_role_definition(self, prompt_data):
        """Verifica se o prompt define uma persona (ex: 'Você é um Product Manager')."""
        system_prompt = prompt_data["system_prompt"]
        assert (
            "Product Manager" in system_prompt or "Você é" in system_prompt
        ), "o prompt não define uma persona/role"

    def test_prompt_mentions_format(self, prompt_data):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        text = (
            prompt_data["system_prompt"] + "\n" + prompt_data.get("user_prompt", "")
        ).lower()
        assert any(
            token in text for token in ("markdown", "user story", "como um")
        ), "o prompt não exige formato Markdown ou User Story"

    def test_prompt_has_few_shot_examples(self, prompt_data):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = prompt_data["system_prompt"]
        assert any(
            token in system_prompt.lower() for token in ("exemplo", "entrada", "saída")
        ), "o prompt não contém exemplos few-shot"

    def test_prompt_no_todos(self, prompt_data):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        full_text = json.dumps(prompt_data, ensure_ascii=False)
        assert "[TODO]" not in full_text, "o prompt ainda contém [TODO]"

    def test_minimum_techniques(self, prompt_data):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt_data.get("techniques_applied", [])
        assert len(techniques) >= 2, (
            f"menos de 2 técnicas listadas: {techniques}"
        )

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
