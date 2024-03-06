from enum import Enum


class Origin(Enum):
    LLMChatBot = "LLM-ChatBot"
    LLMChatAssistant = "llmv213"
    StableDiffusion = "StableDiffusion"
    Txt2ImgPro = "Txt2ImgPro"
    MagicPrompt = "MagicPrompt"
    NSFWDetect = "NSFW_DETECT"
    TtsEn = "TTS-EN-VITS"
    AsrEn = "ASR-EN-WHISPER"