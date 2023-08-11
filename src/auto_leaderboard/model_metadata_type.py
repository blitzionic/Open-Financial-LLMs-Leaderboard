from dataclasses import dataclass
from enum import Enum
import glob
import json
import os
from typing import Dict, List

from ..utils_display import AutoEvalColumn

@dataclass
class ModelInfo:
    name: str
    symbol: str # emoji

model_type_symbols = {
    "fine-tuned": "🔶",
    "pretrained": "🟢",
    "RL-tuned": "🟦",
    "instruction-tuned": "⭕",
}

class ModelType(Enum):
    PT = ModelInfo(name="pretrained", symbol="🟢")
    FT = ModelInfo(name="fine-tuned", symbol="🔶")
    IFT = ModelInfo(name="instruction-tuned", symbol="⭕")
    RL = ModelInfo(name="RL-tuned", symbol="🟦")

    def to_str(self, separator = " "):
        return f"{self.value.symbol}{separator}{self.value.name}" 


TYPE_METADATA: Dict[str, ModelType] = {
    'notstoic/PygmalionCoT-7b': ModelType.IFT,
    'aisquared/dlite-v1-355m': ModelType.IFT,
    'aisquared/dlite-v1-1_5b': ModelType.IFT,
    'aisquared/dlite-v1-774m': ModelType.IFT,
    'aisquared/dlite-v1-124m': ModelType.IFT,
    'aisquared/chopt-2_7b': ModelType.IFT,
    'aisquared/dlite-v2-124m': ModelType.IFT,
    'aisquared/dlite-v2-774m': ModelType.IFT,
    'aisquared/dlite-v2-1_5b': ModelType.IFT,
    'aisquared/chopt-1_3b': ModelType.IFT,
    'aisquared/dlite-v2-355m': ModelType.IFT,
    'augtoma/qCammel-13': ModelType.IFT,
    'Aspik101/Llama-2-7b-hf-instruct-pl-lora_unload': ModelType.IFT,
    'Aspik101/vicuna-7b-v1.3-instruct-pl-lora_unload': ModelType.IFT,
    'TheBloke/alpaca-lora-65B-HF': ModelType.FT,
    'TheBloke/tulu-7B-fp16': ModelType.IFT,
    'TheBloke/guanaco-7B-HF': ModelType.FT,
    'TheBloke/koala-7B-HF': ModelType.FT,
    'TheBloke/wizardLM-7B-HF': ModelType.IFT,
    'TheBloke/airoboros-13B-HF': ModelType.IFT,
    'TheBloke/koala-13B-HF': ModelType.FT,
    'TheBloke/Wizard-Vicuna-7B-Uncensored-HF': ModelType.FT,
    'TheBloke/dromedary-65b-lora-HF': ModelType.IFT,
    'TheBloke/wizardLM-13B-1.0-fp16': ModelType.IFT,
    'TheBloke/WizardLM-13B-V1-1-SuperHOT-8K-fp16': ModelType.FT,
    'TheBloke/Wizard-Vicuna-30B-Uncensored-fp16': ModelType.FT,
    'TheBloke/wizard-vicuna-13B-HF': ModelType.IFT,
    'TheBloke/UltraLM-13B-fp16': ModelType.IFT,
    'TheBloke/OpenAssistant-FT-7-Llama-30B-HF': ModelType.FT,
    'TheBloke/vicuna-13B-1.1-HF': ModelType.IFT,
    'TheBloke/guanaco-13B-HF': ModelType.FT,
    'TheBloke/guanaco-65B-HF': ModelType.FT,
    'TheBloke/airoboros-7b-gpt4-fp16': ModelType.IFT,
    'TheBloke/llama-30b-supercot-SuperHOT-8K-fp16': ModelType.IFT,
    'TheBloke/Llama-2-13B-fp16': ModelType.PT,
    'TheBloke/llama-2-70b-Guanaco-QLoRA-fp16': ModelType.FT,
    'TheBloke/landmark-attention-llama7b-fp16': ModelType.IFT,
    'TheBloke/Planner-7B-fp16': ModelType.IFT,
    'TheBloke/Wizard-Vicuna-13B-Uncensored-HF': ModelType.FT,
    'TheBloke/gpt4-alpaca-lora-13B-HF': ModelType.IFT,
    'TheBloke/gpt4-x-vicuna-13B-HF': ModelType.IFT,
    'TheBloke/gpt4-alpaca-lora_mlp-65B-HF': ModelType.IFT,
    'TheBloke/tulu-13B-fp16': ModelType.IFT,
    'TheBloke/VicUnlocked-alpaca-65B-QLoRA-fp16': ModelType.IFT,
    'TheBloke/Llama-2-70B-fp16': ModelType.IFT,
    'TheBloke/WizardLM-30B-fp16': ModelType.IFT,
    'TheBloke/robin-13B-v2-fp16': ModelType.FT,
    'TheBloke/robin-33B-v2-fp16': ModelType.FT,
    'TheBloke/Vicuna-13B-CoT-fp16': ModelType.IFT,
    'TheBloke/Vicuna-33B-1-3-SuperHOT-8K-fp16': ModelType.IFT,
    'TheBloke/Wizard-Vicuna-30B-Superhot-8K-fp16': ModelType.FT,
    'TheBloke/Nous-Hermes-13B-SuperHOT-8K-fp16': ModelType.IFT,
    'TheBloke/GPlatty-30B-SuperHOT-8K-fp16': ModelType.FT,
    'TheBloke/CAMEL-33B-Combined-Data-SuperHOT-8K-fp16': ModelType.IFT,
    'TheBloke/Chinese-Alpaca-33B-SuperHOT-8K-fp16': ModelType.IFT,
    'jphme/orca_mini_v2_ger_7b': ModelType.IFT,
    'Ejafa/vicuna_7B_vanilla_1.1': ModelType.FT,
    'kevinpro/Vicuna-13B-CoT': ModelType.IFT,
    'AlekseyKorshuk/pygmalion-6b-vicuna-chatml': ModelType.FT,
    'AlekseyKorshuk/chatml-pyg-v1': ModelType.FT,
    'concedo/Vicuzard-30B-Uncensored': ModelType.FT,
    'concedo/OPT-19M-ChatSalad': ModelType.FT,
    'concedo/Pythia-70M-ChatSalad': ModelType.FT,
    'digitous/13B-HyperMantis': ModelType.IFT,
    'digitous/Adventien-GPTJ': ModelType.FT,
    'digitous/Alpacino13b': ModelType.IFT,
    'digitous/GPT-R': ModelType.IFT,
    'digitous/Javelin-R': ModelType.IFT,
    'digitous/Javalion-GPTJ': ModelType.IFT,
    'digitous/Javalion-R': ModelType.IFT,
    'digitous/Skegma-GPTJ': ModelType.FT,
    'digitous/Alpacino30b': ModelType.IFT,
    'digitous/Janin-GPTJ': ModelType.FT,
    'digitous/Janin-R': ModelType.FT,
    'digitous/Javelin-GPTJ': ModelType.FT,
    'SaylorTwift/gpt2_test': ModelType.PT,
    'anton-l/gpt-j-tiny-random': ModelType.FT,
    'Andron00e/YetAnother_Open-Llama-3B-LoRA-OpenOrca': ModelType.FT,
    'Lazycuber/pyg-instruct-wizardlm': ModelType.FT,
    'Lazycuber/Janemalion-6B': ModelType.FT,
    'IDEA-CCNL/Ziya-LLaMA-13B-Pretrain-v1': ModelType.FT,
    'IDEA-CCNL/Ziya-LLaMA-13B-v1': ModelType.IFT,
    'dsvv-cair/alpaca-cleaned-llama-30b-bf16': ModelType.FT,
    'gpt2-medium': ModelType.PT,
    'camel-ai/CAMEL-13B-Combined-Data': ModelType.IFT,
    'camel-ai/CAMEL-13B-Role-Playing-Data': ModelType.FT,
    'camel-ai/CAMEL-33B-Combined-Data': ModelType.IFT,
    'PygmalionAI/pygmalion-6b': ModelType.FT,
    'PygmalionAI/metharme-1.3b': ModelType.IFT,
    'PygmalionAI/pygmalion-1.3b': ModelType.FT,
    'PygmalionAI/pygmalion-350m': ModelType.FT,
    'PygmalionAI/pygmalion-2.7b': ModelType.FT,
    'medalpaca/medalpaca-7b': ModelType.FT,
    'lilloukas/Platypus-30B': ModelType.IFT,
    'lilloukas/GPlatty-30B': ModelType.FT,
    'mncai/chatdoctor': ModelType.FT,
    'chaoyi-wu/MedLLaMA_13B': ModelType.FT,
    'LoupGarou/WizardCoder-Guanaco-15B-V1.0': ModelType.IFT,
    'LoupGarou/WizardCoder-Guanaco-15B-V1.1': ModelType.FT,
    'hakurei/instruct-12b': ModelType.IFT,
    'hakurei/lotus-12B': ModelType.FT,
    'shibing624/chinese-llama-plus-13b-hf': ModelType.IFT,
    'shibing624/chinese-alpaca-plus-7b-hf': ModelType.IFT,
    'shibing624/chinese-alpaca-plus-13b-hf': ModelType.IFT,
    'mosaicml/mpt-7b-instruct': ModelType.IFT,
    'mosaicml/mpt-30b-chat': ModelType.IFT,
    'mosaicml/mpt-7b-storywriter': ModelType.FT,
    'mosaicml/mpt-30b-instruct': ModelType.IFT,
    'mosaicml/mpt-7b-chat': ModelType.IFT,
    'mosaicml/mpt-30b': ModelType.PT,
    'Corianas/111m': ModelType.IFT,
    'Corianas/Quokka_1.3b': ModelType.IFT,
    'Corianas/256_5epoch': ModelType.FT,
    'Corianas/Quokka_256m': ModelType.IFT,
    'Corianas/Quokka_590m': ModelType.IFT,
    'Corianas/gpt-j-6B-Dolly': ModelType.FT,
    'Corianas/Quokka_2.7b': ModelType.IFT,
    'cyberagent/open-calm-7b': ModelType.FT,
    'Aspik101/Nous-Hermes-13b-pl-lora_unload': ModelType.IFT,
    'THUDM/chatglm2-6b': ModelType.IFT,
    'MetaIX/GPT4-X-Alpasta-30b': ModelType.IFT,
    'NYTK/PULI-GPTrio': ModelType.PT,
    'EleutherAI/pythia-1.3b': ModelType.PT,
    'EleutherAI/pythia-2.8b-deduped': ModelType.PT,
    'EleutherAI/gpt-neo-125m': ModelType.PT,
    'EleutherAI/pythia-160m': ModelType.PT,
    'EleutherAI/gpt-neo-2.7B': ModelType.PT,
    'EleutherAI/pythia-1b-deduped': ModelType.PT,
    'EleutherAI/pythia-6.7b': ModelType.PT,
    'EleutherAI/pythia-70m-deduped': ModelType.PT,
    'EleutherAI/gpt-neox-20b': ModelType.PT,
    'EleutherAI/pythia-1.4b-deduped': ModelType.PT,
    'EleutherAI/pythia-2.7b': ModelType.PT,
    'EleutherAI/pythia-6.9b-deduped': ModelType.PT,
    'EleutherAI/pythia-70m': ModelType.PT,
    'EleutherAI/gpt-j-6b': ModelType.PT,
    'EleutherAI/pythia-12b-deduped': ModelType.PT,
    'EleutherAI/gpt-neo-1.3B': ModelType.PT,
    'EleutherAI/pythia-410m-deduped': ModelType.PT,
    'EleutherAI/pythia-160m-deduped': ModelType.PT,
    'EleutherAI/polyglot-ko-12.8b': ModelType.PT,
    'EleutherAI/pythia-12b': ModelType.PT,
    'roneneldan/TinyStories-33M': ModelType.PT,
    'roneneldan/TinyStories-28M': ModelType.PT,
    'roneneldan/TinyStories-1M': ModelType.PT,
    'roneneldan/TinyStories-8M': ModelType.PT,
    'roneneldan/TinyStories-3M': ModelType.PT,
    'jerryjalapeno/nart-100k-7b': ModelType.FT,
    'lmsys/vicuna-13b-v1.3': ModelType.IFT,
    'lmsys/vicuna-7b-v1.3': ModelType.IFT,
    'lmsys/vicuna-13b-v1.1': ModelType.IFT,
    'lmsys/vicuna-13b-delta-v1.1': ModelType.IFT,
    'lmsys/vicuna-7b-delta-v1.1': ModelType.IFT,
    'abhiramtirumala/DialoGPT-sarcastic-medium': ModelType.FT,
    'haonan-li/bactrian-x-llama-13b-merged': ModelType.IFT,
    'Gryphe/MythoLogic-13b': ModelType.IFT,
    'Gryphe/MythoBoros-13b': ModelType.IFT,
    'pillowtalks-ai/delta13b': ModelType.FT,
    'wannaphong/openthaigpt-0.1.0-beta-full-model_for_open_llm_leaderboard': ModelType.FT,
    'bigscience/bloom-7b1': ModelType.PT,
    'bigcode/tiny_starcoder_py': ModelType.PT,
    'bigcode/starcoderplus': ModelType.FT,
    'bigcode/gpt_bigcode-santacoder': ModelType.PT,
    'bigcode/starcoder': ModelType.PT,
    'Open-Orca/OpenOrca-Preview1-13B': ModelType.IFT,
    'microsoft/DialoGPT-large': ModelType.FT,
    'microsoft/DialoGPT-small': ModelType.FT,
    'microsoft/DialoGPT-medium': ModelType.FT,
    'microsoft/CodeGPT-small-py': ModelType.FT,
    'Tincando/fiction_story_generator': ModelType.FT,
    'Pirr/pythia-13b-deduped-green_devil': ModelType.FT,
    'Aeala/GPT4-x-AlpacaDente2-30b': ModelType.FT,
    'Aeala/GPT4-x-AlpacaDente-30b': ModelType.FT,
    'Aeala/GPT4-x-Alpasta-13b': ModelType.FT,
    'Aeala/VicUnlocked-alpaca-30b': ModelType.IFT,
    'Tap-M/Luna-AI-Llama2-Uncensored': ModelType.FT,
    'illuin/test-custom-llama': ModelType.FT,
    'dvruette/oasst-llama-13b-2-epochs': ModelType.FT,
    'dvruette/oasst-gpt-neox-20b-1000-steps': ModelType.FT,
    'dvruette/llama-13b-pretrained-dropout': ModelType.PT,
    'dvruette/llama-13b-pretrained': ModelType.PT,
    'dvruette/llama-13b-pretrained-sft-epoch-1': ModelType.PT,
    'dvruette/llama-13b-pretrained-sft-do2': ModelType.PT,
    'dvruette/oasst-gpt-neox-20b-3000-steps': ModelType.FT,
    'dvruette/oasst-pythia-12b-pretrained-sft': ModelType.PT,
    'dvruette/oasst-pythia-6.9b-4000-steps': ModelType.FT,
    'dvruette/gpt-neox-20b-full-precision': ModelType.FT,
    'dvruette/oasst-llama-13b-1000-steps': ModelType.FT,
    'openlm-research/open_llama_7b_700bt_preview': ModelType.PT,
    'openlm-research/open_llama_7b': ModelType.PT,
    'openlm-research/open_llama_7b_v2': ModelType.PT,
    'openlm-research/open_llama_3b': ModelType.PT,
    'openlm-research/open_llama_13b': ModelType.PT,
    'openlm-research/open_llama_3b_v2': ModelType.PT,
    'PocketDoc/Dans-PileOfSets-Mk1-llama-13b-merged': ModelType.IFT,
    'GeorgiaTechResearchInstitute/galpaca-30b': ModelType.IFT,
    'GeorgiaTechResearchInstitute/starcoder-gpteacher-code-instruct': ModelType.IFT,
    'databricks/dolly-v2-7b': ModelType.IFT,
    'databricks/dolly-v2-3b': ModelType.IFT,
    'databricks/dolly-v2-12b': ModelType.IFT,
    'Rachneet/gpt2-xl-alpaca': ModelType.FT,
    'Locutusque/gpt2-conversational-or-qa': ModelType.FT,
    'psyche/kogpt': ModelType.FT,
    'NbAiLab/nb-gpt-j-6B-alpaca': ModelType.IFT,
    'Mikael110/llama-2-7b-guanaco-fp16': ModelType.FT,
    'Mikael110/llama-2-13b-guanaco-fp16': ModelType.FT,
    'Fredithefish/CrimsonPajama': ModelType.IFT,
    'Fredithefish/RedPajama-INCITE-Chat-3B-ShareGPT-11K': ModelType.FT,
    'Fredithefish/ScarletPajama-3B-HF': ModelType.FT,
    'Fredithefish/RedPajama-INCITE-Chat-3B-Instruction-Tuning-with-GPT-4': ModelType.IFT,
    'acrastt/RedPajama-INCITE-Chat-Instruct-3B-V1': ModelType.IFT,
    'eachadea/vicuna-13b-1.1': ModelType.FT,
    'eachadea/vicuna-7b-1.1': ModelType.FT,
    'eachadea/vicuna-13b': ModelType.FT,
    'openaccess-ai-collective/wizard-mega-13b': ModelType.IFT,
    'openaccess-ai-collective/manticore-13b': ModelType.IFT,
    'openaccess-ai-collective/manticore-30b-chat-pyg-alpha': ModelType.IFT,
    'openaccess-ai-collective/minotaur-13b': ModelType.IFT,
    'openaccess-ai-collective/minotaur-13b-fixed': ModelType.IFT,
    'openaccess-ai-collective/hippogriff-30b-chat': ModelType.IFT,
    'openaccess-ai-collective/manticore-13b-chat-pyg': ModelType.IFT,
    'pythainlp/wangchanglm-7.5B-sft-enth': ModelType.IFT,
    'pythainlp/wangchanglm-7.5B-sft-en-sharded': ModelType.IFT,
    'euclaise/gpt-neox-122m-minipile-digits': ModelType.FT,
    'stabilityai/StableBeluga1-Delta': ModelType.IFT,
    'stabilityai/stablelm-tuned-alpha-7b': ModelType.IFT,
    'stabilityai/StableBeluga2': ModelType.IFT,
    'stabilityai/StableBeluga-13B': ModelType.IFT,
    'stabilityai/StableBeluga-7B': ModelType.IFT,
    'stabilityai/stablelm-base-alpha-7b': ModelType.PT,
    'stabilityai/stablelm-base-alpha-3b': ModelType.PT,
    'stabilityai/stablelm-tuned-alpha-3b': ModelType.IFT,
    'alibidaran/medical_transcription_generator': ModelType.FT,
    'CalderaAI/30B-Lazarus': ModelType.IFT,
    'CalderaAI/13B-BlueMethod': ModelType.IFT,
    'CalderaAI/13B-Ouroboros': ModelType.IFT,
    'KoboldAI/OPT-13B-Erebus': ModelType.FT,
    'KoboldAI/GPT-J-6B-Janeway': ModelType.FT,
    'KoboldAI/GPT-J-6B-Shinen': ModelType.FT,
    'KoboldAI/fairseq-dense-2.7B': ModelType.PT,
    'KoboldAI/OPT-6B-nerys-v2': ModelType.FT,
    'KoboldAI/GPT-NeoX-20B-Skein': ModelType.FT,
    'KoboldAI/PPO_Pygway-6b-Mix': ModelType.FT,
    'KoboldAI/fairseq-dense-6.7B': ModelType.PT,
    'KoboldAI/fairseq-dense-125M': ModelType.PT,
    'KoboldAI/OPT-13B-Nerybus-Mix': ModelType.FT,
    'KoboldAI/OPT-2.7B-Erebus': ModelType.FT,
    'KoboldAI/OPT-350M-Nerys-v2': ModelType.FT,
    'KoboldAI/OPT-2.7B-Nerys-v2': ModelType.FT,
    'KoboldAI/OPT-2.7B-Nerybus-Mix': ModelType.FT,
    'KoboldAI/OPT-13B-Nerys-v2': ModelType.FT,
    'KoboldAI/GPT-NeoX-20B-Erebus': ModelType.FT,
    'KoboldAI/OPT-6.7B-Erebus': ModelType.FT,
    'KoboldAI/fairseq-dense-355M': ModelType.PT,
    'KoboldAI/OPT-6.7B-Nerybus-Mix': ModelType.FT,
    'KoboldAI/GPT-J-6B-Adventure': ModelType.FT,
    'KoboldAI/OPT-350M-Erebus': ModelType.FT,
    'KoboldAI/GPT-J-6B-Skein': ModelType.FT,
    'KoboldAI/OPT-30B-Erebus': ModelType.FT,
    'klosax/pythia-160m-deduped-step92k-193bt': ModelType.PT,
    'klosax/open_llama_3b_350bt_preview': ModelType.PT,
    'klosax/openllama-3b-350bt': ModelType.PT,
    'klosax/pythia-70m-deduped-step44k-92bt': ModelType.PT,
    'klosax/open_llama_13b_600bt_preview': ModelType.PT,
    'klosax/open_llama_7b_400bt_preview': ModelType.PT,
    'kfkas/Llama-2-ko-7b-Chat': ModelType.IFT,
    'WeOpenML/Alpaca-7B-v1': ModelType.IFT,
    'WeOpenML/PandaLM-Alpaca-7B-v1': ModelType.IFT,
    'TFLai/gpt2-turkish-uncased': ModelType.FT,
    'ehartford/WizardLM-13B-Uncensored': ModelType.IFT,
    'ehartford/dolphin-llama-13b': ModelType.IFT,
    'ehartford/Wizard-Vicuna-30B-Uncensored': ModelType.FT,
    'ehartford/WizardLM-30B-Uncensored': ModelType.IFT,
    'ehartford/Wizard-Vicuna-13B-Uncensored': ModelType.FT,
    'ehartford/WizardLM-7B-Uncensored': ModelType.IFT,
    'ehartford/based-30b': ModelType.FT,
    'ehartford/Wizard-Vicuna-7B-Uncensored': ModelType.FT,
    'wahaha1987/llama_7b_sharegpt94k_fastchat': ModelType.FT,
    'wahaha1987/llama_13b_sharegpt94k_fastchat': ModelType.FT,
    'OpenAssistant/oasst-sft-1-pythia-12b': ModelType.FT,
    'OpenAssistant/stablelm-7b-sft-v7-epoch-3': ModelType.IFT,
    'OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5': ModelType.FT,
    'OpenAssistant/pythia-12b-sft-v8-2.5k-steps': ModelType.IFT,
    'OpenAssistant/pythia-12b-sft-v8-7k-steps': ModelType.IFT,
    'OpenAssistant/pythia-12b-pre-v8-12.5k-steps': ModelType.IFT,
    'OpenAssistant/llama2-13b-orca-8k-3319': ModelType.IFT,
    'junelee/wizard-vicuna-13b': ModelType.FT,
    'BreadAi/gpt-YA-1-1_160M': ModelType.PT,
    'BreadAi/MuseCan': ModelType.PT,
    'BreadAi/MusePy-1-2': ModelType.PT,
    'BreadAi/DiscordPy': ModelType.PT,
    'BreadAi/PM_modelV2': ModelType.PT,
    'BreadAi/gpt-Youtube': ModelType.PT,
    'BreadAi/StoryPy': ModelType.FT,
    'julianweng/Llama-2-7b-chat-orcah': ModelType.FT,
    'AGI-inc/lora_moe_7b_baseline': ModelType.FT,
    'AGI-inc/lora_moe_7b': ModelType.FT,
    'togethercomputer/GPT-NeoXT-Chat-Base-20B': ModelType.IFT,
    'togethercomputer/RedPajama-INCITE-Chat-7B-v0.1': ModelType.IFT,
    'togethercomputer/RedPajama-INCITE-Instruct-7B-v0.1': ModelType.IFT,
    'togethercomputer/RedPajama-INCITE-7B-Base': ModelType.PT,
    'togethercomputer/RedPajama-INCITE-7B-Instruct': ModelType.IFT,
    'togethercomputer/RedPajama-INCITE-Base-3B-v1': ModelType.PT,
    'togethercomputer/Pythia-Chat-Base-7B': ModelType.IFT,
    'togethercomputer/RedPajama-INCITE-Base-7B-v0.1': ModelType.PT,
    'togethercomputer/GPT-JT-6B-v1': ModelType.IFT,
    'togethercomputer/GPT-JT-6B-v0': ModelType.IFT,
    'togethercomputer/RedPajama-INCITE-Chat-3B-v1': ModelType.IFT,
    'togethercomputer/RedPajama-INCITE-7B-Chat': ModelType.IFT,
    'togethercomputer/RedPajama-INCITE-Instruct-3B-v1': ModelType.IFT,
    'Writer/camel-5b-hf': ModelType.IFT,
    'Writer/palmyra-base': ModelType.PT,
    'MBZUAI/LaMini-GPT-1.5B': ModelType.IFT,
    'MBZUAI/lamini-cerebras-111m': ModelType.IFT,
    'MBZUAI/lamini-neo-1.3b': ModelType.IFT,
    'MBZUAI/lamini-cerebras-1.3b': ModelType.IFT,
    'MBZUAI/lamini-cerebras-256m': ModelType.IFT,
    'MBZUAI/LaMini-GPT-124M': ModelType.IFT,
    'MBZUAI/lamini-neo-125m': ModelType.IFT,
    'TehVenom/DiffMerge-DollyGPT-Pygmalion': ModelType.FT,
    'TehVenom/PPO_Shygmalion-6b': ModelType.FT,
    'TehVenom/Dolly_Shygmalion-6b-Dev_V8P2': ModelType.FT,
    'TehVenom/Pygmalion_AlpacaLora-7b': ModelType.FT,
    'TehVenom/PPO_Pygway-V8p4_Dev-6b': ModelType.FT,
    'TehVenom/Dolly_Malion-6b': ModelType.FT,
    'TehVenom/PPO_Shygmalion-V8p4_Dev-6b': ModelType.FT,
    'TehVenom/ChanMalion': ModelType.FT,
    'TehVenom/GPT-J-Pyg_PPO-6B': ModelType.IFT,
    'TehVenom/Pygmalion-13b-Merged': ModelType.FT,
    'TehVenom/Metharme-13b-Merged': ModelType.IFT,
    'TehVenom/Dolly_Shygmalion-6b': ModelType.FT,
    'TehVenom/GPT-J-Pyg_PPO-6B-Dev-V8p4': ModelType.IFT,
    'georgesung/llama2_7b_chat_uncensored': ModelType.FT,
    'vicgalle/gpt2-alpaca': ModelType.IFT,
    'vicgalle/alpaca-7b': ModelType.FT,
    'vicgalle/gpt2-alpaca-gpt4': ModelType.IFT,
    'facebook/opt-350m': ModelType.PT,
    'facebook/opt-125m': ModelType.PT,
    'facebook/xglm-4.5B': ModelType.PT,
    'facebook/opt-2.7b': ModelType.PT,
    'facebook/opt-6.7b': ModelType.PT,
    'facebook/galactica-30b': ModelType.PT,
    'facebook/opt-13b': ModelType.PT,
    'facebook/opt-66b': ModelType.PT,
    'facebook/xglm-7.5B': ModelType.PT,
    'facebook/xglm-564M': ModelType.PT,
    'facebook/opt-30b': ModelType.PT,
    'golaxy/gogpt-7b': ModelType.FT,
    'golaxy/gogpt2-7b': ModelType.FT,
    'golaxy/gogpt-7b-bloom': ModelType.FT,
    'golaxy/gogpt-3b-bloom': ModelType.FT,
    'psmathur/orca_mini_v2_7b': ModelType.IFT,
    'psmathur/orca_mini_7b': ModelType.IFT,
    'psmathur/orca_mini_3b': ModelType.IFT,
    'psmathur/orca_mini_v2_13b': ModelType.IFT,
    'gpt2-xl': ModelType.PT,
    'lxe/Cerebras-GPT-2.7B-Alpaca-SP': ModelType.FT,
    'Monero/Manticore-13b-Chat-Pyg-Guanaco': ModelType.FT,
    'Monero/WizardLM-Uncensored-SuperCOT-StoryTelling-30b': ModelType.IFT,
    'Monero/WizardLM-13b-OpenAssistant-Uncensored': ModelType.IFT,
    'Monero/WizardLM-30B-Uncensored-Guanaco-SuperCOT-30b': ModelType.IFT,
    'jzjiao/opt-1.3b-rlhf': ModelType.FT,
    'HuggingFaceH4/starchat-beta': ModelType.IFT,
    'KnutJaegersberg/gpt-2-xl-EvolInstruct': ModelType.IFT,
    'KnutJaegersberg/megatron-GPT-2-345m-EvolInstruct': ModelType.IFT,
    'KnutJaegersberg/galactica-orca-wizardlm-1.3b': ModelType.IFT,
    'openchat/openchat_8192': ModelType.IFT,
    'openchat/openchat_v2': ModelType.IFT,
    'openchat/openchat_v2_w': ModelType.IFT,
    'ausboss/llama-13b-supercot': ModelType.IFT,
    'ausboss/llama-30b-supercot': ModelType.IFT,
    'Neko-Institute-of-Science/metharme-7b': ModelType.IFT,
    'Neko-Institute-of-Science/pygmalion-7b': ModelType.FT,
    'SebastianSchramm/Cerebras-GPT-111M-instruction': ModelType.IFT,
    'victor123/WizardLM-13B-1.0': ModelType.IFT,
    'OpenBuddy/openbuddy-openllama-13b-v7-fp16': ModelType.FT,
    'OpenBuddy/openbuddy-llama2-13b-v8.1-fp16': ModelType.FT,
    'OpenBuddyEA/openbuddy-llama-30b-v7.1-bf16': ModelType.FT,
    'baichuan-inc/Baichuan-7B': ModelType.PT,
    'tiiuae/falcon-40b-instruct': ModelType.IFT,
    'tiiuae/falcon-40b': ModelType.PT,
    'tiiuae/falcon-7b': ModelType.PT,
    'YeungNLP/firefly-llama-13b': ModelType.FT,
    'YeungNLP/firefly-llama-13b-v1.2': ModelType.FT,
    'YeungNLP/firefly-llama2-13b': ModelType.FT,
    'YeungNLP/firefly-ziya-13b': ModelType.FT,
    'shaohang/Sparse0.5_OPT-1.3': ModelType.FT,
    'xzuyn/Alpacino-SuperCOT-13B': ModelType.IFT,
    'xzuyn/MedicWizard-7B': ModelType.FT,
    'xDAN-AI/xDAN_13b_l2_lora': ModelType.FT,
    'beomi/KoAlpaca-Polyglot-5.8B': ModelType.FT,
    'beomi/llama-2-ko-7b': ModelType.IFT,
    'Salesforce/codegen-6B-multi': ModelType.PT,
    'Salesforce/codegen-16B-nl': ModelType.PT,
    'Salesforce/codegen-6B-nl': ModelType.PT,
    'ai-forever/rugpt3large_based_on_gpt2': ModelType.FT,
    'gpt2-large': ModelType.PT,
    'frank098/orca_mini_3b_juniper': ModelType.FT,
    'frank098/WizardLM_13B_juniper': ModelType.FT,
    'FPHam/Free_Sydney_13b_HF': ModelType.FT,
    'huggingface/llama-13b': ModelType.PT,
    'huggingface/llama-7b': ModelType.PT,
    'huggingface/llama-65b': ModelType.PT,
    'huggingface/llama-30b': ModelType.PT,
    'Henk717/chronoboros-33B': ModelType.IFT,
    'jondurbin/airoboros-13b-gpt4-1.4': ModelType.IFT,
    'jondurbin/airoboros-7b': ModelType.IFT,
    'jondurbin/airoboros-7b-gpt4': ModelType.IFT,
    'jondurbin/airoboros-7b-gpt4-1.1': ModelType.IFT,
    'jondurbin/airoboros-7b-gpt4-1.2': ModelType.IFT,
    'jondurbin/airoboros-7b-gpt4-1.3': ModelType.IFT,
    'jondurbin/airoboros-7b-gpt4-1.4': ModelType.IFT,
    'jondurbin/airoboros-l2-7b-gpt4-1.4.1': ModelType.IFT,
    'jondurbin/airoboros-l2-13b-gpt4-1.4.1': ModelType.IFT,
    'jondurbin/airoboros-l2-70b-gpt4-1.4.1': ModelType.IFT,
    'jondurbin/airoboros-13b': ModelType.IFT,
    'jondurbin/airoboros-33b-gpt4-1.4': ModelType.IFT,
    'jondurbin/airoboros-33b-gpt4-1.2': ModelType.IFT,
    'jondurbin/airoboros-65b-gpt4-1.2': ModelType.IFT,
    'ariellee/SuperPlatty-30B': ModelType.IFT,
    'danielhanchen/open_llama_3b_600bt_preview': ModelType.FT,
    'cerebras/Cerebras-GPT-256M': ModelType.PT,
    'cerebras/Cerebras-GPT-1.3B': ModelType.PT,
    'cerebras/Cerebras-GPT-13B': ModelType.PT,
    'cerebras/Cerebras-GPT-2.7B': ModelType.PT,
    'cerebras/Cerebras-GPT-111M': ModelType.PT,
    'cerebras/Cerebras-GPT-6.7B': ModelType.PT,
    'Yhyu13/oasst-rlhf-2-llama-30b-7k-steps-hf': ModelType.RL,
    'Yhyu13/llama-30B-hf-openassitant': ModelType.FT,
    'NousResearch/Nous-Hermes-Llama2-13b': ModelType.IFT,
    'NousResearch/Nous-Hermes-llama-2-7b': ModelType.IFT,
    'NousResearch/Redmond-Puffin-13B': ModelType.IFT,
    'NousResearch/Nous-Hermes-13b': ModelType.IFT,
    'project-baize/baize-v2-7b': ModelType.IFT,
    'project-baize/baize-v2-13b': ModelType.IFT,
    'LLMs/WizardLM-13B-V1.0': ModelType.FT,
    'LLMs/AlpacaGPT4-7B-elina': ModelType.FT,
    'wenge-research/yayi-7b': ModelType.FT,
    'wenge-research/yayi-7b-llama2': ModelType.FT,
    'wenge-research/yayi-13b-llama2': ModelType.FT,
    'yhyhy3/open_llama_7b_v2_med_instruct': ModelType.IFT,
    'llama-anon/instruct-13b': ModelType.IFT,
    'huggingtweets/jerma985': ModelType.FT,
    'huggingtweets/gladosystem': ModelType.FT,
    'huggingtweets/bladeecity-jerma985': ModelType.FT,
    'huggyllama/llama-13b': ModelType.PT,
    'huggyllama/llama-65b': ModelType.PT,
    'FabbriSimo01/Facebook_opt_1.3b_Quantized': ModelType.PT,
    'upstage/Llama-2-70b-instruct': ModelType.IFT,
    'upstage/Llama-2-70b-instruct-1024': ModelType.IFT,
    'upstage/llama-65b-instruct': ModelType.IFT,
    'upstage/llama-30b-instruct-2048': ModelType.IFT,
    'upstage/llama-30b-instruct': ModelType.IFT,
    'WizardLM/WizardLM-13B-1.0': ModelType.IFT,
    'WizardLM/WizardLM-13B-V1.1': ModelType.IFT,
    'WizardLM/WizardLM-13B-V1.2': ModelType.IFT,
    'WizardLM/WizardLM-30B-V1.0': ModelType.IFT,
    'WizardLM/WizardCoder-15B-V1.0': ModelType.IFT,
    'gpt2': ModelType.PT,
    'keyfan/vicuna-chinese-replication-v1.1': ModelType.IFT,
    'nthngdy/pythia-owt2-70m-100k': ModelType.FT,
    'nthngdy/pythia-owt2-70m-50k': ModelType.FT,
    'quantumaikr/KoreanLM-hf': ModelType.FT,
    'quantumaikr/open_llama_7b_hf': ModelType.FT,
    'quantumaikr/QuantumLM-70B-hf': ModelType.IFT,
    'MayaPH/FinOPT-Lincoln': ModelType.FT,
    'MayaPH/FinOPT-Franklin': ModelType.FT,
    'MayaPH/GodziLLa-30B': ModelType.IFT,
    'MayaPH/GodziLLa-30B-plus': ModelType.IFT,
    'MayaPH/FinOPT-Washington': ModelType.FT,
    'ogimgio/gpt-neo-125m-neurallinguisticpioneers': ModelType.FT,
    'layoric/llama-2-13b-code-alpaca': ModelType.FT,
    'CobraMamba/mamba-gpt-3b': ModelType.FT,
    'CobraMamba/mamba-gpt-3b-v2': ModelType.FT,
    'CobraMamba/mamba-gpt-3b-v3': ModelType.FT,
    'timdettmers/guanaco-33b-merged': ModelType.FT,
    'elinas/chronos-33b': ModelType.IFT,
    'heegyu/RedTulu-Uncensored-3B-0719': ModelType.IFT,
    'heegyu/WizardVicuna-Uncensored-3B-0719': ModelType.IFT,
    'heegyu/WizardVicuna-3B-0719': ModelType.IFT,
    'meta-llama/Llama-2-7b-chat-hf': ModelType.RL,
    'meta-llama/Llama-2-7b-hf': ModelType.PT,
    'meta-llama/Llama-2-13b-chat-hf': ModelType.RL,
    'meta-llama/Llama-2-13b-hf': ModelType.PT,
    'meta-llama/Llama-2-70b-chat-hf': ModelType.RL,
    'meta-llama/Llama-2-70b-hf': ModelType.PT,
    'xhyi/PT_GPTNEO350_ATG': ModelType.FT,
    'h2oai/h2ogpt-gm-oasst1-en-1024-20b': ModelType.FT,
    'h2oai/h2ogpt-gm-oasst1-en-1024-open-llama-7b-preview-400bt': ModelType.FT,
    'h2oai/h2ogpt-oig-oasst1-512-6_9b': ModelType.IFT,
    'h2oai/h2ogpt-oasst1-512-12b': ModelType.IFT,
    'h2oai/h2ogpt-oig-oasst1-256-6_9b': ModelType.IFT,
    'h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-7b-preview-300bt': ModelType.FT,
    'h2oai/h2ogpt-oasst1-512-20b': ModelType.IFT,
    'h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-7b-preview-300bt-v2': ModelType.FT,
    'h2oai/h2ogpt-gm-oasst1-en-1024-12b': ModelType.FT,
    'h2oai/h2ogpt-gm-oasst1-multilang-1024-20b': ModelType.FT,
    'bofenghuang/vigogne-13b-instruct': ModelType.IFT,
    'bofenghuang/vigogne-13b-chat': ModelType.FT,
    'bofenghuang/vigogne-2-7b-instruct': ModelType.IFT,
    'bofenghuang/vigogne-7b-instruct': ModelType.IFT,
    'bofenghuang/vigogne-7b-chat': ModelType.FT,
    'Vmware/open-llama-7b-v2-open-instruct': ModelType.IFT,
    'VMware/open-llama-0.7T-7B-open-instruct-v1.1': ModelType.IFT,
    'ewof/koishi-instruct-3b': ModelType.IFT,
    'gywy/llama2-13b-chinese-v1': ModelType.FT,
    'GOAT-AI/GOAT-7B-Community': ModelType.FT,
    'psyche/kollama2-7b': ModelType.FT,
    'TheTravellingEngineer/llama2-7b-hf-guanaco': ModelType.FT,
    'beaugogh/pythia-1.4b-deduped-sharegpt': ModelType.FT,
    'augtoma/qCammel-70-x': ModelType.IFT,
    'Lajonbot/Llama-2-7b-chat-hf-instruct-pl-lora_unload': ModelType.IFT,
    'anhnv125/pygmalion-6b-roleplay': ModelType.FT,
    '64bits/LexPodLM-13B': ModelType.FT,
}


def get_model_type(leaderboard_data: List[dict]):
    for model_data in leaderboard_data:
        # Todo @clefourrier once requests are connected with results 
        # Stored information
        request_file = os.path.join("eval-queue", model_data["model_name_for_query"] + "_eval_request_*" + ".json")
        request_file = glob.glob(request_file)

        if len(request_file) == 0:
            model_data[AutoEvalColumn.model_type.name] = ""
            model_data[AutoEvalColumn.model_type_symbol.name] = ""
            continue

        request_file = request_file[0]

        try:
            with open(request_file, "r") as f:
                request = json.load(f)
            is_delta = request["weight_type"] != "Original"
        except Exception:
            is_delta = False

        try:
            with open(request_file, "r") as f:
                request = json.load(f)
            model_type = request["model_type"]
            model_data[AutoEvalColumn.model_type.name] = model_type
            model_data[AutoEvalColumn.model_type_symbol.name] = model_type_symbols[model_type] + ("🔺" if is_delta else "")
        except Exception:
            model_data[AutoEvalColumn.model_type.name] = "Unknown, add type to request file!"
            model_data[AutoEvalColumn.model_type_symbol.name] = "?"
